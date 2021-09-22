import numpy as np
import matplotlib.pyplot as plt

from ott.tools import transport
from ott.geometry import geometry
from scipy.sparse import csr_matrix
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from scipy.linalg import orthogonal_procrustes, svd
from sklearn.metrics.pairwise import pairwise_distances

# num_colors = range(8)
# colors = [f"#{random.randrange(0x1000000):06x}" for n in num_colors]


def plot_matrices(A, B):
    """
    """
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(24, 24))

    ax1.matshow(A, cmap=plt.cm.rainbow)
    ax1.tick_params(left=False, labelleft=False, top=False, labeltop=False)

    for i in range(ndim):
        for j in range(ndim):
            c = int(np.round(A[j,i]))
            ax1.text(i, j, str(c), va='center', ha='center')

    ax2.matshow(B, cmap=plt.cm.rainbow)
    ax2.tick_params(left=False, labelleft=False, top=False, labeltop=False)

    for i in range(ndim):
        for j in range(ndim):
            c = int(np.round(B[j,i]))
            ax2.text(i, j, str(c), va='center', ha='center')

    fig.tight_layout()
    return fig


def _data(ndim=10, rng_seed=2021):
    """
    """
    rng = np.random.default_rng(rng_seed)
    data_mtx = np.reshape(range(100), (10, 10))

    permutation = rng.choice(range(ndim), ndim, replace=False)
    idx = np.empty_like(permutation)
    idx[permutation] = np.arange(len(permutation))
    permuted_mtx = data_mtx[idx, :]  # return a rearranged copy

    return data_mtx, permuted_mtx


def _procrustes(X, Y):
    """Compute a mixing matrix R and a scaling sc such that Frobenius norm
    ||sc RX - Y||^2 is minimized and R is an orthogonal matrix.
    SVD is done on the YX^T (primal), expecting that n_features <= n_timeframes.

    Parameters
    ----------
    X: (n_samples, n_features) nd array
        source data
    Y: (n_samples, n_features) nd array
        target data

    Returns
    ----------
    R: (n_features, n_features) nd array
        transformation matrix
    """
    A = Y.T.dot(X)
    U, s, V = svd(A, full_matrices=0)
    R = U.dot(V)

    return R.T, R.dot(X.T).T


def _ot(X, Y, metric='euclidean', reg=0.1):
    """
    Compute the optimal coupling between X and Y with entropic regularization
    using a OTT as a backend for acceleration.

    Parameters
    ----------
    metric : str(optional)
        metric used to create transport cost matrix, \
        see full list in scipy.spatial.distance.cdist doc
    reg : int (optional)
        level of entropic regularization
    Attributes
    ----------
    R : scipy.sparse.csr_matrix
        Mixing matrix containing the optimal permutation
    """
    n = len(X.T)
    cost_matrix = cdist(X.T, Y.T, metric=metric)
    geom = geometry.Geometry(cost_matrix=cost_matrix, epsilon=reg)
    P = transport.Transport(
        geom, max_iterations=1000, threshold=1e-3)
    P.solve()
    R = np.asarray(P.matrix * n)

    return R, R.dot(X.T).T


def _optimal_permutation(X, Y):
    """
    Compute the optmal permutation matrix of X toward Y

    Parameters
    ----------
    X: (n_samples, n_features) nd array
        source data
    Y: (n_samples, n_features) nd array
        target data
    Returns
    ----------
    permutation : (n_features, n_features) nd array
        transformation matrix
    """
    dist = pairwise_distances(X.T, Y.T)
    u = linear_sum_assignment(dist)
    u = np.array(list(zip(*u)))
    opt = csr_matrix(
        (np.ones(X.shape[1]), (u[:, 0], u[:, 1]))).T.toarray()

    return opt, opt.dot(X.T).T


def _srm(X, Y, n_components=5, n_iter=10, rng_seed=2021):
    """
    """
    rng = np.random.default_rng(rng_seed)

    basis = np.linalg.qr(
        rng.random((X.shape[0], n_components))
    )[0].T
    sr = X.dot(basis.T)

    for i in range(n_iter):
        cov = sr.T.dot(X)
        U, _, V = svd(cov, full_matrices=False)
        reduced_basis = U.dot(V)
        sr = X.dot(reduced_basis.T)

    corr_mat = sr.T.dot(Y)
    U, _, V = svd(corr_mat, full_matrices=False)
    subject_basis = U.dot(V)