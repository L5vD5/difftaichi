import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
steps = 512

def update(frame, xlist, ylist, zlist, poses):
    # data = np.vstack((xlist[frame], ylist[frame]))
    # poses.set_offsets(data.T)
    # poses.set_3d_offsets(zlist[frame])
    poses._offsets3d = (xlist[frame], ylist[frame], zlist[frame])
    return poses

def main():
    print('diffmpm3d test')
    folder = 'mpm3d/iter{:04d}/'.format(19)
    xlist = []
    ylist = []
    zlist = []
    for s in range(7, steps, 2):
        fn = '{}{:04}.npz'.format(folder, s)
        data =np.load(fn)
        # print(type(data['xs']))
        xs = data['xs'][0: len(data['xs']): 10]
        ys = data['ys'][0: len(data['ys']): 10]
        zs = data['zs'][0: len(data['zs']): 10]

        xlist.append(xs)
        ylist.append(ys)
        zlist.append(zs)
    
    # xlist = xlist[0: len(xlist): 50]
    # ylist = ylist[0: len(ylist): 50]
    # zlist = zlist[0: len(zlist): 50]
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    poses = ax.scatter(xlist[0], ylist[0], zlist[0])


    ani = FuncAnimation(fig, update, fargs=[xlist, ylist, zlist, poses], frames=range(len(xlist)), interval=1)
    # ani.save('exAnimation.gif', writer='imagemagick', fps=30, dpi=100)
    plt.show()


if __name__ == '__main__':
    main()
