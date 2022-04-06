import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
steps = 1024


def main():
    print('diffmpm3d test')
    folder = 'rilab/iter{:04d}/'.format(0)
    xlist = []
    ylist = []
    zlist = []
    for s in range(0, steps, 7):
        fn = '{}{:04}.npy'.format(folder, s)
        data =np.load(fn)
        # print(type(data['xs']))
        xs = data[0][0: len(data[0])]
        ys = data[1][0: len(data[1])]
        zs = data[2][0: len(data[2])]
        # us = data[3][0: len(data[3])]
        # vs = data[4][0: len(data[4])]
        # ws = data[5][0: len(data[5])]
        # cs = data[6][0: len(data[6])]
        # zs = data['cs'][0: len(data['cs']): 10]

        xlist.append(xs)
        ylist.append(ys)
        zlist.append(zs)
    
    # xlist = xlist[0: len(xlist): 50]
    # ylist = ylist[0: len(ylist): 50]
    # zlist = zlist[0: len(zlist): 50]
    fig = plt.figure()
    plt.title(0)
    ax = fig.add_subplot(projection="3d")
    ax.set_xlim([0, 0.5])
    ax.set_ylim([0, 0.5])
    ax.set_zlim([1, 0.5])
    poses = ax.scatter(xlist[0], ylist[0], zlist[0], c=range(len(xlist[0])))
    lines = []

    # lines, = ax.plot(xlist[0], ylist[0], zlist[0])
    def update(frame, xlist, ylist, zlist, lines, poses):
        # data = np.vstack((xlist[frame], ylist[frame]))
        # poses.set_offsets(data.T)
        # poses.set_3d_offsets(zlist[frame])
        plt.title(frame)
        poses._offsets3d = (xlist[frame], ylist[frame], zlist[frame])

        return poses, lines


    ani = FuncAnimation(fig, update, fargs=[xlist, ylist, zlist, lines, poses], frames=range(len(xlist)), interval=1)
    # ani.save('exAnimation.gif', writer='imagemagick', fps=30, dpi=100)
    plt.show()


if __name__ == '__main__':
    main()
