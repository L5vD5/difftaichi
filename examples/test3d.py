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
    return poses#, lines

def main():
    print('diffmpm3d test')
    folder = 'rilab/iter{:04d}/'.format(0)
    xlist = []
    ylist = []
    zlist = []
    for s in range(7, steps, 2):
        fn = '{}{:04}.npy'.format(folder, s)
        data =np.load(fn)
        # print(type(data['xs']))
        xs = data[0][0: len(data[0]): 10]
        ys = data[1][0: len(data[1]): 10]
        zs = data[2][0: len(data[2]): 10]
        # zs = data['cs'][0: len(data['cs']): 10]

        xlist.append(xs)
        ylist.append(ys)
        zlist.append(zs)
    
    # xlist = xlist[0: len(xlist): 50]
    # ylist = ylist[0: len(ylist): 50]
    # zlist = zlist[0: len(zlist): 50]
    fig = plt.figure()
    ax = fig.add_subplot(projection="3d")
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_zlim([2, 0])
    poses = ax.scatter(xlist[0], ylist[0], zlist[0], c=range(len(zlist[0])))
    # lines, = ax.plot(xlist[0], ylist[0], zlist[0])


    ani = FuncAnimation(fig, update, fargs=[xlist, ylist, zlist, poses], frames=range(len(xlist)), interval=1)
    # ani.save('exAnimation.gif', writer='imagemagick', fps=30, dpi=100)
    plt.show()


if __name__ == '__main__':
    main()
