objects = []
springs = []
import numpy as np


def add_object(x):
    objects.append(x)
    return len(objects) - 1


def add_spring(a, b, length=None, stiffness=1, actuation=0.1):
    if length == None:
        length = ((objects[a][0] - objects[b][0])**2 +
                  (objects[a][1] - objects[b][1])**2)**0.5
    springs.append([a, b, length, stiffness, actuation])

def add_spring3D(a, b, length=None, stiffness=1, actuation=0.1):
    if length == None:
        length = ((objects[a][0] - objects[b][0])**2 +
                  (objects[a][1] - objects[b][1])**2 +
                  (objects[a][2] - objects[b][2])**2)**0.5
    springs.append([a, b, length, stiffness, actuation])


def robotA():
    add_object([0.2, 0.1])
    add_object([0.3, 0.13])
    add_object([0.4, 0.1])
    add_object([0.2, 0.2])
    add_object([0.3, 0.2])
    add_object([0.4, 0.2])

    s = 14000

    def link(a, b, actuation=0.1):
        add_spring(a, b, stiffness=s, actuation=actuation)

    link(0, 1)
    link(1, 2)
    link(3, 4)
    link(4, 5)
    link(0, 3)
    link(2, 5)
    link(0, 4)
    link(1, 4)
    link(2, 4)
    link(3, 1)
    link(5, 1)

    return objects, springs


points = []
point_id = []
mesh_springs = []


def add_mesh_point(i, j):
    if (i, j) not in points:
        id = add_object((i * 0.05 + 0.1, j * 0.05 + 0.1))
        points.append((i, j))
        point_id.append(id)
    return point_id[points.index((i, j))]


def add_mesh_spring(a, b, s, act):
    if (a, b) in mesh_springs or (b, a) in mesh_springs:
        return

    mesh_springs.append((a, b))
    add_spring(a, b, stiffness=s, actuation=act)


def add_mesh_square(i, j, actuation=0.0):
    a = add_mesh_point(i, j)
    b = add_mesh_point(i, j + 1)
    c = add_mesh_point(i + 1, j)
    d = add_mesh_point(i + 1, j + 1)

    # b d
    # a c
    add_mesh_spring(a, b, 3e4, actuation)
    add_mesh_spring(c, d, 3e4, actuation)

    for i in [a, b, c, d]:
        for j in [a, b, c, d]:
            if i != j:
                add_mesh_spring(i, j, 3e4, 0)


def add_mesh_triangle(i, j, actuation=0.0):
    a = add_mesh_point(i + 0.5, j + 0.5)
    b = add_mesh_point(i, j + 1)
    d = add_mesh_point(i + 1, j + 1)

    for i in [a, b, d]:
        for j in [a, b, d]:
            if i != j:
                add_mesh_spring(i, j, 3e4, 0)


def robotB():
    add_mesh_triangle(2, 0, actuation=0.15)
    add_mesh_triangle(0, 0, actuation=0.15)
    add_mesh_square(0, 1, actuation=0.15)
    add_mesh_square(0, 2)
    add_mesh_square(1, 2)
    add_mesh_square(2, 1, actuation=0.15)
    add_mesh_square(2, 2)
    # add_mesh_square(2, 3)
    # add_mesh_square(2, 4)

    return objects, springs


def robotC():
    add_mesh_square(2, 0, actuation=0.15)
    add_mesh_square(2, 1, actuation=0.15)
    add_mesh_square(2, 2, actuation=0.15)
    add_mesh_square(2, 3, actuation=0.15)
    add_mesh_square(2, 4, actuation=0.15)
    add_mesh_square(2, 5, actuation=0.15)
    add_mesh_square(2, 6, actuation=0.15)
    add_mesh_square(2, 7, actuation=0.15)

    return objects, springs


def robotD():
    add_mesh_square(2, 0, actuation=0.15)
    add_mesh_square(0, 0, actuation=0.15)
    add_mesh_square(0, 1, actuation=0.15)
    add_mesh_square(0, 2)
    add_mesh_square(1, 2)
    add_mesh_square(2, 1, actuation=0.15)
    add_mesh_square(2, 2)
    add_mesh_square(2, 3)
    add_mesh_square(2, 4)
    add_mesh_square(3, 1)
    add_mesh_square(4, 0, actuation=0.15)
    add_mesh_square(4, 1, actuation=0.15)

    return objects, springs



# 3d
def add_mesh_point_3d(i, j, k):
    if (i, j, k) not in points:
        id = add_object((i * 0.05 + 0.1, j * 0.05 + 0.1, k * 0.05 + 0.1))
        points.append((i, j, k))
        point_id.append(id)
        # print((i * 0.05 + 0.1, j * 0.05 + 0.1, k * 0.05 + 0.1))

    return point_id[points.index((i, j, k))]
global k
k = 0
def add_mesh_spring_3d(a, b, s, act):
    global k
    if (a, b) in mesh_springs or (b, a) in mesh_springs:
        return
    print(k, a, b, np.linalg.norm(np.array(points[a])-np.array(points[b])))
    k+=1
    mesh_springs.append((a, b))
    add_spring3D(a, b, stiffness=s, actuation=act)

def add_mesh_cube(i, j, k, actuation=0.0):
    poses = np.array([[i, j, k], [i+1, j, k], [i+1, j+1, k], [i, j+1, k], [i, j+1, k+1], [i+1, j+1, k+1], [i+1, j, k+1], [i, j, k+1]])
    p = []
    for pose in poses:
        p.append(add_mesh_point_3d(pose[0], pose[1], pose[2]))
    # a = add_mesh_point_3d(2, 2, 2)
    # b = add_mesh_point_3d(4, 2, 2)
    # c = add_mesh_point_3d(4, 4, 2)
    # d = add_mesh_point_3d(2, 4, 2)
    # e = add_mesh_point_3d(2, 4, 4)
    # f = add_mesh_point_3d(4, 4, 4)
    # g = add_mesh_point_3d(4, 2, 4)
    # h = add_mesh_point_3d(2, 2, 4)

    s = 3e4
    # e f
    # h g
    # d c
    # a b
    l = p#[a, b, c, d, e, f, g, h]
    for i in l:
        for j in l:
            if (i != j):
                dist = np.array(points[i])-np.array(points[j])
                # print(a, i, j, np.linalg.norm(dist))
                if np.linalg.norm(dist) > 1:
                    add_mesh_spring_3d(i, j, s, act=0.15)
                else:
                    add_mesh_spring_3d(i, j, s, act=0)
    


def robot3D():
    add_mesh_cube(0, 0, 0)
    add_mesh_cube(0, 0, 1)
    add_mesh_cube(0, 0, 2)
    add_mesh_cube(0, 0, 3)

    return objects, springs

robots = [robotA, robotB, robotC, robotD, robot3D]
