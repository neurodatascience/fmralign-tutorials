import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.linalg import orthogonal_procrustes
from fmralign.alignment_methods import OptimalTransportAlignment


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

# Points generated using : https://shinao.github.io/PathToPoints/
v1 = pd.read_csv('brain_points - v1_cortex.csv', header=None)
pole = pd.read_csv('brain_points - temporal_pole.csv', header=None)

R, sc = orthogonal_procrustes(v1.T, pole.T)
# ot_alignment = OptimalTransportAlignment(reg=.1)
# ot_alignment.fit(v1.T, pole.T)

fig, ax = plt.subplots(figsize=(10,10))
plt.plot(pole[0], pole[1], 'og', ms=20)
plt.plot(v1[0], v1[1], 'og', ms=20)
# if R has some negative coeffs, plot them too in red
if not (R >= 0).all():
    _plot2D_samples_mat(v1.values, pole.values, -R, thr=0.1, c=[1, 0.2, 0.2])
    colors = ['blue', 'red']
    lines = [Line2D([0], [0], color=c, linewidth=2) for c in colors]
# Then plot R positive coeffs above a threshold in blue
_plot2D_samples_mat(v1.values, pole.values, R, thr=0.1, c=[0.2, 0.2, 1])
plt.axis('off')
plt.savefig('lines.png', transparent=True)