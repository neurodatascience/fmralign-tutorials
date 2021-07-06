import numpy as np
import pandas as pd
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.spatial import procrustes
from scipy.linalg import orthogonal_procrustes

x = np.zeros((8, 8), dtype=int)
x[1::2, ::2] = 1
x[::2, 1::2] = 1

y = np.ones((8, 8), dtype=int)
y[1::2, ::2] = 0
y[::2, 1::2] = 0

fig, ax = plt.subplots()
i = ax.imshow(x, cmap=cm.gray, interpolation='none')
fig.colorbar(i)
plt.show()

mtx1, mtx2, mm = procrustes(x, y)

fig, ax = plt.subplots()
i = ax.imshow(y, cmap=cm.gray, interpolation='none')
fig.colorbar(i)
plt.show()

ts_one = np.tile(np.stack([x, y], axis=-1), 12)
ts_two = np.tile(np.stack([y, x], axis=-1), 12)

R, scale = orthogonal_procrustes(ts_one.reshape((64, 24)),
                                 ts_two.reshape((64, 24)))
fig, ax = plt.subplots()
i = ax.imshow(ts_one.reshape((64, 24)) @ R,
              cmap=cm.gray, interpolation='none')
fig.colorbar(i)
plt.show()


def rotate(p, origin=(0, 0), degrees=0):
    """
    Taken from: https://stackoverflow.com/a/58781388
    """
    angle = np.deg2rad(degrees)
    R = np.array([[np.cos(angle), -np.sin(angle)],
                  [np.sin(angle),  np.cos(angle)]])
    o = np.atleast_2d(origin)
    p = np.atleast_2d(p)
    return np.squeeze((R @ (p.T-o.T) + o.T).T)


source = pd.read_csv('data.csv')
jitter = np.random.normal(10, 3, (165, 2))
x_jitter, y_jitter = np.hsplit(jitter, 2)

target = pd.DataFrame({'x': source['x'] + x_jitter.flatten(),
                       'y': source['y'] + y_jitter.flatten()})

origin = (500, 500)
new_points = rotate(target.values, origin=origin, degrees=40)
target['x'], target['y'] = np.hsplit(new_points, 2)

plt.scatter(source['x'], source['y'])
plt.scatter(target['x'], target['y'])
plt.show()

tick_params = {'axis': 'both', 'which': 'both', 'bottom': False, 'top': False,
               'left': False, 'labelleft': False, 'labelbottom': False}

def _plot2D_samples_mat(xs, xt, R, thr=1e-8, **kwargs):
    """ Plot matrix R in 2D with lines for coefficients above threshold thr.
    REPRODUCED FROM POT PACKAGE
    """
    if ('color' not in kwargs) and ('c' not in kwargs):
        kwargs['color'] = 'k'
    mx = R.max()
    for i in range(xs.shape[0]):
        for j in range(xt.shape[0]):
            if R[i, j] / mx > thr:
                plt.plot([xs[i, 0], xt[j, 0]], [xs[i, 1], xt[j, 1]],
                         alpha=R[i, j] / mx, **kwargs)

def _plot_distributions_and_alignment(source, target, R=None, thr=.1, title=None, tick_params=tick_params):
    fig, ax = plt.subplots()
    plt.plot(source['x'], source['y'], 'og', label='Source samples')
    plt.plot(target['x'], target['y'], 'or', label='Target samples')
    plt.legend()

    if R is not None:
        # if R has some negative coeffs, plot them too in red
        if not (R >= 0).all():
            _plot2D_samples_mat(source, target, -R, thr=thr, c=[1, 0.2, 0.2])
            colors = ['blue', 'red']
            lines = [Line2D([0], [0], color=c, linewidth=2) for c in colors]
            labels = ['Positive coeffs', 'Negative coeffs']
            leg = Legend(ax, lines, labels, loc='upper left', fontsize=10)
            ax.add_artist(leg)
            plt.legend()
        # Then plot R positive coeffs above a threshold in blue
        _plot2D_samples_mat(source, target, R, thr=thr, c=[0.2, 0.2, 1])

    plt.rcParams.update(
        {'font.size': 12, 'ytick.labelsize': 14, 'xtick.labelsize': 14, 'axes.titlesize': 14, "axes.labelsize": 12})
    plt.xlabel('Contrast 1', fontsize=14)
    plt.ylabel('Contrast 2', fontsize=14)
    plt.tick_params(**tick_params)
    plt.title(title, fontsize=16)

a, b = source, target

# translate all the data to the origin
mtx1 -= np.mean(a, 0)
mtx2 -= np.mean(b, 0)

norm1 = np.linalg.norm(a)
norm2 = np.linalg.norm(b)

# change scaling of data (in rows) such that trace(mtx*mtx') = 1
a /= norm1
b /= norm2

R, scale = orthogonal_procrustes(a, b)
