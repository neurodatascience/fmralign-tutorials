---
jupytext:
  formats: md:myst,ipynb
  text_representation:
    extension: .md
    format_name: myst
    format_version: '0.9'
    jupytext_version: 1.5.2
kernelspec:
  display_name: Python 3
  name: python3
---

# Procrustes alignment

Originally introduced in {cite}`Schonemann1966-qq`,
Procrustes analysis is a form of statistical shape analysis which focusses on comparing the geometry of two objects or data sets.
Although it may seem unusual to think of distributions in terms of geometry,
this makes more sense when we consider the distributions as point sets in some activation space.

Because we assume a known correspondence between these two distributions,
we can directly compare the $i$-th sample across $X$ and $Y$.
The goal in Procrustes is to find a single orthogonal transformation that minimizes the sum-of-squares distances between all $n$ $X$, $Y$ pairs,
thereby minimizing the total distance between the distributions.

```{margin}
Procrustes analysis is named for the legend of Procrustes,
the ancient innkeeper from Greek mythology who stretched or cut off traveller's limbs so they would fit his bed.
```

## Orthogonal Procrustes

Our goal, then, is to find linear transformations that minimize the total distance between the two distributions.
By further assuming that each distribution has exactly the same number of voxels $p$ measured over the same $n$ observations,
we can consider that we are comparing two shapes with a known one-to-one mapping;
i.e. the $i$-th voxel in the $X$ distribution corresponds to the same voxel index in the $Y$ distribution.
Procrustes analysis allows us to align the shapes as closely as possible through linear mapping
and to quantify how much they differ after this alignment.

### Formalism

```{code-cell} python3
:tags: ["hide-input"]
import numpy as np

X = np.random.rand(20, 100)
Y = np.random.rand(20, 100)
```

For our two distributions $\mathbf{X} \in \mathbb{R}^{n \times p}$ and
$\mathbf{Y} \in \mathbb{R}^{n \times p}$, Procrustes solves the following minimization:

```{math}
:label: procrustes_eq_1
\arg\min_{\mathbf{R}} ||\mathbf{R} \mathbf{X} - \mathbf{Y}||_F^2 \\
\mathbf{R}^\intercal\mathbf{R} = \mathbf{I}
```

Where $|| \cdot ||_F$ indicates the Frobenius norm,
which corresponds to the elementwise Euclidean distance.

```{math}
:label: procrustes_eq_2
\arg\max_{\mathbf{R}} \mathrm{Tr}\hspace{1pt}(\mathbf{R} \mathbf{X} \mathbf{Y}^T) \\
\mathbf{R}^\intercal\mathbf{R} = \mathbf{I}
```

```{math}
:label: procrustes_eq_3
\arg\max_{\mathbf{R}} \mathrm{Tr}\hspace{1pt}(\mathbf{R} \mathbf{U} \Sigma \mathbf{V}^\intercal) \\
\mathbf{R}^\intercal\mathbf{R} = \mathbf{I}
```

```{code-cell} python3
from scipy.linalg import svd

A = Y.T.dot(X)
U, s, V = svd(A, full_matrices=0)
```

```{code-cell} python3
R = U.dot(V)
sc = s.sum() / (np.linalg.norm(X) ** 2)
```

### Implementation

Optimized implementations are available in `scipy.linalg.orthogonal_procrustes`.

```{code-cell} python3
from scipy.linalg import orthogonal_procrustes

R, sc = orthogonal_procrustes(X, Y)
```

## Generalized Procrustes

Generalized Procrustes analysis differs from Procrustes analysis in two ways.
First, generalized Procrustes includes both the orthogonal transformations of Procrustes (i.e., rotations and reflections),
as well as additional scaling and translation transformations.
Second, generalized Procrustes can be applied to more than two shapes through the iterative use of a reference shape.

We can formally express the generalized Procrustes problem as:

```{math}
:label: general_procrustes_eq_1
\min_{\mathbf{R}= s\mathbf{M}} ||\mathbf{R} \mathbf{X} - \mathbf{Y}||_F^2 \\
s\in\mathbb{R^+}, \enspace \mathbf{M} \in \mathbb{R}^{p \times p} \text{ s.t. } \mathbf{M}^\intercal\mathbf{M} = \mathbf{I}_p
```

### Formalism

```{math}
:label: general_procrustes_eq_2
A = B + C
```

### Implementation

Optimized implementations are available in `scipy.spatial.procrustes`.

```{code-cell} python3
from scipy.spatial import procrustes

mtx1, mtx2, disp = procrustes(X, Y)
```

## Useful resources

- [Cory Simon blog on orthogonal Procrustes](https://simonensemble.github.io/2018-10/orthogonal-procrustes.html)

```{bibliography}
:style: unsrt
:filter: docname in docnames
```
