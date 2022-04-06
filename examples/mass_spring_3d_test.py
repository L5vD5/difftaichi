import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib.animation import FuncAnimation
steps = 1024


def main():
    print('diff mass spring 3d test')
    # folder = 'rilab/iter{:04d}/'.format(0)
    folder = 'mass_spring_3d/iter{:04d}/'.format(1)
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
        us = data[3][0: len(data[3])]
        vs = data[4][0: len(data[4])]
        ws = data[5][0: len(data[5])]
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
    ax.set_zlim([0, 0.5])
    poses = ax.scatter(xlist[0], ylist[0], zlist[0], c=['k'])
    lines = []
    for i in range(len(xlist[0])):
        lines.append([])
        for j in range(len(xlist[0])):
            norm = np.linalg.norm(np.array([xlist[0][i], ylist[0][i], zlist[0][i]])-np.array([xlist[0][j], ylist[0][j], zlist[0][j]]))
            if i != j and norm < 0.06:
                lines[i].append(ax.plot([xlist[0][i], xlist[0][j]], [ylist[0][i], ylist[0][j]], [zlist[0][i], zlist[0][j]], c='k')[0])
            else:
                lines[i].append(None)

    # lines, = ax.plot(xlist[0], ylist[0], zlist[0])
    def update(frame, xlist, ylist, zlist, lines, poses):
        # data = np.vstack((xlist[frame], ylist[frame]))
        # poses.set_offsets(data.T)
        # poses.set_3d_offsets(zlist[frame])
        plt.title(frame)
        poses._offsets3d = (xlist[frame], ylist[frame], zlist[frame])
        for i in range(len(xlist[frame])):
            for j in range(len(xlist[frame])):
                if i != j:
                    norm = np.linalg.norm(np.array([xlist[0][i], ylist[0][i], zlist[0][i]])-np.array([xlist[0][j], ylist[0][j], zlist[0][j]]))
                    if(norm < 0.06):
                        # print([[xlist[frame][i], xlist[frame][j]], [ylist[frame][i], ylist[frame][j]]])
                        lines[i][j].set_data(np.array([xlist[frame][i], xlist[frame][j]]), np.array([ylist[frame][i], ylist[frame][j]]))#, [ylist[frame][i], ylist[frame][j]], [zlist[frame][i], zlist[frame][j]]
                        lines[i][j].set_3d_properties(np.array([zlist[frame][i], zlist[frame][j]]))
                        if (i == 0 and j == 5) or (i == 5 and j == 0):
                            lines[i][j].set_color([0, 1, 0])
                    # lines[i][j].set_ydata([ylist[frame][i], ylist[frame][j]])

        return poses, lines


    ani = FuncAnimation(fig, update, fargs=[xlist, ylist, zlist, lines, poses], frames=range(len(xlist)), interval=1)
    # ani.save('exAnimation.gif', writer='imagemagick', fps=30, dpi=100)
    plt.show()


if __name__ == '__main__':
    main()
