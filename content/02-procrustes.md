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

# Procrustes analysis

Procrustes analysis allows us to compares the geometry of two objects or data sets.
Specifically, for two geometries with a known one-to-one mapping,
we can consider the distance between each pair of corresponding points.
Our goal is to derive an orthogonal transformation that minimizes the distance between each pair of points, thus minimizing the total distance between the two geometries.
Named for the legend of Procrustes,
the ancient Greek innkeeper who stretched or cut off traveller's limbs so they would fit his bed,
Procrustes analysis can be seen as conforming datasets through a series of rigid-body transformations {cite}`Schonemann1966-qq`.

## Formalizing the problem

Suppose we have two data distributions, $X$ and $Y$,
which each sample a different representational geometry.
Each distribution contains a series of $n$ observations, such that
$X = \{\mathbf{x}_1, \ldots, \mathbf{x}_n\}$
where $\mathbf{x}_i \in \mathbb{R}^p$.

For fMRI data, $n$ would be the number of time points sampled,
while $p$ is the number of units considered, usually corresponding to voxels.
For this example, we'll set $p=2$ to ease visualization,
but in a real data set we may be working with many more dimensions!

```{code} python3
import numpy as np

x = np.random.rand(1, 2)
y = np.random.rand(1, 3)
```

Because we assume a known correspondence between these two distributions,
we can directly compare the $i$-th sample in $X$ and $Y$.
The goal in Procrustes is to find a single orthogonal transformation that minimizes the sum-of-squares distances between all $n$ $X$, $Y$ pairs,
thereby minimizing the total distance between the distributions:

```{math}
:label: procrustes_eq_1
\arg\min_{\mathbf{R}} \sum_{i = 1}^{n} ||\mathbf{R} \mathbf{x}_i - \mathbf{y}_i||_F^2 \\
\mathbf{R}^\intercal\mathbf{R} = \mathbf{I}
```

If we stack all of our data points into two matrices
--one for each distribution-- we can represent our two distributions as
$\mathbf{X} \in \mathbb{R}^{n \times p}$ and
$\mathbf{Y} \in \mathbb{R}^{n \times p}$.

We can then re-write our problem as:

```{math}
:label: procrustes_eq_1
\arg\min_{\mathbf{R}} ||\mathbf{R} \mathbf{X} - \mathbf{Y}||_F^2 \\
\mathbf{R}^\intercal\mathbf{R} = \mathbf{I}
```

```{bibliography} references.bib
:style: unsrt
:filter: docname in docnames
```
