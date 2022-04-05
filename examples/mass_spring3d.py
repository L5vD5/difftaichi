from mass_spring_robot_config import robots
import random
import sys
import matplotlib.pyplot as plt
import taichi as ti
import math
import numpy as np
import os

random.seed(0)
np.random.seed(0)

real = ti.f32
dim = 3
ti.init(default_fp=real)

max_steps = 4096
vis_interval = 256
output_vis_interval = 8
steps = 2048 // 2
assert steps * 2 <= max_steps

scalar = lambda: ti.field(dtype=real)
vec = lambda: ti.Vector.field(dim, dtype=real)

loss = scalar()

x = vec()
v = vec()
v_inc = vec()

head_id = 0
goal = vec()

n_objects = 0
# target_ball = 0
elasticity = 0.0
ground_height = 0.1
gravity = 0
friction = 0.5

gradient_clip = 1
spring_omega = 10
damping = 40

n_springs = 0
spring_anchor_a = ti.field(ti.i32)
spring_anchor_b = ti.field(ti.i32)
spring_length = scalar()
spring_stiffness = scalar()
spring_actuation = scalar()

n_sin_waves = 10
weights1 = scalar()
bias1 = scalar()

n_hidden = 32
weights2 = scalar()
bias2 = scalar()
# nn1 output
hidden = scalar()

center = vec()
# nn2 output
act = scalar()

objects = []
springs = []

def n_input_states():
    return n_sin_waves + 4 * n_objects + 2


def allocate_fields():
    ti.root.dense(ti.i, max_steps).dense(ti.l, n_objects).place(x, v, v_inc)
    ti.root.dense(ti.i, n_springs).place(spring_anchor_a, spring_anchor_b,
                                         spring_length, spring_stiffness,
                                         spring_actuation)
    ti.root.dense(ti.ij, (n_hidden, n_input_states())).place(weights1)
    ti.root.dense(ti.i, n_hidden).place(bias1)
    ti.root.dense(ti.ij, (n_springs, n_hidden)).place(weights2)
    ti.root.dense(ti.i, n_springs).place(bias2)
    ti.root.dense(ti.ij, (max_steps, n_hidden)).place(hidden)
    ti.root.dense(ti.il, (max_steps, n_springs)).place(act)
    ti.root.dense(ti.i, max_steps).place(center)
    ti.root.place(loss, goal)
    ti.root.lazy_grad()


dt = 0.002
learning_rate = 25


def actuation(t: ti.i32):
    for i in range(n_springs):
        act[t, i] = 0
        if i == 5:
            act[t, i] = -t/50
        


@ti.kernel
def apply_spring_force(t: ti.i32):
    for i in range(n_springs):
        a = spring_anchor_a[i]
        b = spring_anchor_b[i]
        pos_a = x[t, a]
        pos_b = x[t, b]
        dist = pos_a - pos_b
        # print(dist, dist.norm())
        length = dist.norm() + 1e-4

        target_length = spring_length[i] * (1.0 +
                                            spring_actuation[i] * act[t, i])
        impulse = dt * (length -
                        target_length) * spring_stiffness[i] / length * dist
        # impulse.fill(0)

        ti.atomic_add(v_inc[t + 1, a], -impulse)
        ti.atomic_add(v_inc[t + 1, b], impulse)


use_toi = False


@ti.kernel
def advance_toi(t: ti.i32):
    for i in range(n_objects):
        s = math.exp(-dt * damping)
        old_v = s * v[t - 1, i] + dt * gravity * ti.Vector([0.0, 1.0, 0.0
                                                            ]) + v_inc[t, i]
        old_x = x[t - 1, i]
        new_x = old_x + dt * old_v
        toi = 0.0
        new_v = old_v
        if new_x[1] < ground_height and old_v[1] < -1e-4:
            toi = -(old_x[1] - ground_height) / old_v[1]
            new_v = ti.Vector([0.0, 0.0])
        new_x = old_x + toi * old_v + (dt - toi) * new_v
        v[t, i] = new_v
        # x[t, i] = new_x
        if(i != 0 and i != 2):
            x[t, i] = new_x
        else:
            x[t, i] = old_x


@ti.kernel
def advance_no_toi(t: ti.i32):
    for i in range(n_objects):
        s = math.exp(-dt * damping)
        old_v = s * v[t - 1, i] + dt * gravity * ti.Vector([0.0, 1.0, 0.0
                                                            ]) + v_inc[t, i]
        old_x = x[t - 1, i]
        new_v = old_v
        depth = old_x[1] - ground_height
        if depth < 0 and new_v[1] < 0:
            # friction projection
            new_v[0] = 0
            new_v[1] = 0
        new_x = old_x + dt * new_v
        v[t, i] = new_v
        # x[t, i] = new_x
        if(i != 0 and i != 2):
            x[t, i] = new_x
        else:
            x[t, i] = old_x

gui = ti.GUI("Mass Spring Robot", (512, 512), background_color=0xFFFFFF)


def forward(output=None, visualize=True):
    if random.random() > 0.5:
        goal[None] = [0.9, 0.2, 0.0]
    else:
        goal[None] = [0.1, 0.2, 0.0]
    goal[None] = [0.9, 0.2, 0.0]

    interval = vis_interval
    if output:
        interval = output_vis_interval
        os.makedirs('mass_spring/{}/'.format(output), exist_ok=True)

    total_steps = steps if not output else steps * 2

    for t in range(1, total_steps):
        actuation(t - 1)
        apply_spring_force(t - 1)
        if use_toi:
            advance_toi(t)
        else:
            advance_no_toi(t)
        # print(x.to_numpy()[t])

        # if (t + 1) % interval == 0 and visualize:

            # gui.line(begin=(0, ground_height),
            #          end=(1, ground_height),
            #          color=0x0,
            #          radius=3)

            # def circle(x, y, color):
            #     gui.circle((x, y), ti.rgb_to_hex(color), 7)

            # for i in range(n_springs):

            #     def get_pt(x):
            #         return (x[0], x[1])

            #     a = act[t - 1, i] * 0.5
            #     r = 2
            #     if spring_actuation[i] == 0:
            #         a = 0
            #         c = 0x222222
            #     else:
            #         r = 4
            #         c = ti.rgb_to_hex((0.5 + a, 0.5 - abs(a), 0.5 - a))
            #     gui.line(begin=get_pt(x[t, spring_anchor_a[i]]),
            #              end=get_pt(x[t, spring_anchor_b[i]]),
            #              radius=r,
            #              color=c)

            # for i in range(n_objects):
            #     color = (0.4, 0.6, 0.6)
            #     if i == head_id:
            #         color = (0.8, 0.2, 0.3)
            #     circle(x[t, i][0], x[t, i][1], color)
            # # circle(goal[None][0], goal[None][1], (0.6, 0.2, 0.2))

            # if output:
            #     gui.show('mass_spring/{}/{:04d}.png'.format(output, t))
            # else:
            #     gui.show()
    folder = 'mass_spring_3d/iter{:04d}'.format(1)
    os.makedirs(folder, exist_ok=True)
    x_ = x.to_numpy()
    v_ = v.to_numpy()
    for s in range(0, steps, 7):
        xs, ys, zs = [], [], []
        us, vs, ws = [], [], []
        cs, c_ = [], []
        for i in range(n_objects):
            xs.append(x_[s, i][0])
            ys.append(x_[s, i][1])
            zs.append(x_[s, i][2])
            us.append(v_[s, i][0])
            vs.append(v_[s, i][1])
            ws.append(v_[s, i][2])
        for i in range(n_springs):
            a = act[t - 1, i] * 0.5
            r = 2
            if spring_actuation[i] == 0:
                a = 0
                c = 255
            else:
                r = 4
                c = 0#ti.rgb_to_hex((0.5 + a, 0.5 - abs(a), 0.5 - a))
            c_.append(c)
        cs.append(c_)
        np.save('{}/{:04}'.format(folder, s), [xs, ys, zs, us, vs, ws])

    loss[None] = 0
    # compute_loss(steps - 1)


@ti.kernel
def clear_states():
    for t in range(0, max_steps):
        for i in range(0, n_objects):
            v_inc[t, i] = ti.Vector([0.0, 0.0, 0.0])


def clear():
    clear_states()


def setup_robot(objects, springs):
    global n_objects, n_springs
    n_objects = len(objects)
    n_springs = len(springs)
    allocate_fields()

    print('n_objects=', n_objects, '   n_springs=', n_springs)

    for i in range(n_objects):
        x[0, i] = objects[i]

    for i in range(n_springs):
        s = springs[i]
        spring_anchor_a[i] = s[0]
        spring_anchor_b[i] = s[1]
        spring_length[i] = s[2]
        spring_stiffness[i] = s[3]
        spring_actuation[i] = s[4]



robot_id = 0
if len(sys.argv) != 2:
    print(
        "Usage: python3 mass_spring.py [robot_id=0, 1, 2, ...] [task=train/plot]"
    )
    exit(-1)
else:
    robot_id = int(sys.argv[1])


def main():
    objects, springs = robots[robot_id]()
    setup_robot(objects, springs)
    clear()
    forward('final{}'.format(robot_id))


if __name__ == '__main__':
    main()
