import taichi as ti
import os
import math
import numpy as np
import random
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
        xlist.append(data['xs'])
        ylist.append(data['ys'])
        zlist.append(data['zs'])
    
    # xlist = xlist[0: len(xlist): 10]
    # ylist = ylist[0: len(ylist): 10]
    # zlist = zlist[0: len(zlist): 10]
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")

    poses = ax.scatter(xlist[0], ylist[0], zlist[0], s=1)


    ani = FuncAnimation(fig, update, fargs=[xlist, ylist, zlist, poses], frames=range(len(xlist)), interval=1)
    ani.save('exAnimation.gif', writer='imagemagick', fps=30, dpi=100)
    plt.show()


if __name__ == '__main__':
    main()
