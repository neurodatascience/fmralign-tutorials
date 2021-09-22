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
Procrustes analysis allows us to compares the geometry of two objects or data sets.
Although it may seem unusual to think of distributions in terms of geometry,
this makes more sense when we consider the distributions as point sets in some activation space.
Our goal, then, is to find linear transformations that minimize the total distance between the two distributions.
By further assuming that each distribution has exactly the same number of voxels $p$ measured over the same $n$ observations,
we can consider that we are comparing two shapes with a known one-to-one mapping;
i.e. the $i$-th voxel in the $X$ distribution corresponds to the same voxel index in the $Y$ distribution.
Procrustes analysis allows us to align the shapes as closely as possible through linear mapping
and to quantify how much they differ after this alignment.

```{margin}
Named for the legend of Procrustes,
the ancient Greek innkeeper who stretched or cut off traveller's limbs so they would fit his bed.
```

Because we assume a known correspondence between these two distributions,
we can directly compare the $i$-th sample across $X$ and $Y$.
The goal in Procrustes is to find a single orthogonal transformation that minimizes the sum-of-squares distances between all $n$ $X$, $Y$ pairs,
thereby minimizing the total distance between the distributions:

## Formalization

For our two distributions $\mathbf{X} \in \mathbb{R}^{n \times p}$ and
$\mathbf{Y} \in \mathbb{R}^{n \times p}$, Procrustes solves the following minimization:

```{math}
:label: procrustes_eq_1
\arg\min_{\mathbf{R}} \sum_{i = 1}^{n} ||\mathbf{R} \mathbf{x}_i - \mathbf{y}_i||_F^2 \\
\mathbf{R}^\intercal\mathbf{R} = \mathbf{I}
```

Where $|| \cdot ||_F$ indicates the Frobenius norm,
which corresponds to the elementwise Euclidean distance.
By assuming an implicit, index-based correspondence across our two distributions,
we can re-write the minimization as:

```{math}
:label: procrustes_eq_2
\arg\min_{\mathbf{R}} ||\mathbf{R} \mathbf{X} - \mathbf{Y}||_F^2 \\
\mathbf{R}^\intercal\mathbf{R} = \mathbf{I}
```

## Implementation

```{code} python3
import numpy as np

x = np.random.rand(20, 100)
y = np.random.rand(20, 100)
```

## Useful resources

https://simonensemble.github.io/2018-10/orthogonal-procrustes.html

```{bibliography} references.bib
:style: unsrt
:filter: docname in docnames
```
