---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Generalized Procrustes Analysis

Procrustes analysis allows us to compares the geometry of two objects or data sets.
Specifically, for two geometries with a known one-to-one mapping,
we can consider the distance between each pair of corresponding points.
Our goal is to derive an orthogonal transformation that minimizes the distance between each pair of points, thus minimizing the total distance between the two geometries.
Named for the legend of Procrustes,
the ancient Greek innkeeper who stretched or cut off traveller's limbs so they would fit his bed,
Procrustes analysis can be seen as conforming datasets through a series of rigid-body transformations {cite}`Schonemann1966-qq`.

Generalized Procrustes analysis differs from Procrustes analysis in two significant ways.
First, generalized Procrustes includes both the orthogonal transformations of Procrustes (i.e., rotations and reflections),
as well as additional scaling and translation transformations.
Second, generalized Procrustes can be applied to more than two shapes through the iterative use of a reference shape.

## Formalizing the problem

Suppose we have two data matrices
$X \in \mathbb{R}^{n \times p}$ and
$Y \in \mathbb{R}^{n \times p}$,
where $n$ is the number of samples,
and $p$ are the number of units for each network.

For this example, we'll set $p=2$ to ease visualization.
In a real data set, we may be working with many more dimensions and samples!

```{code} python3
import numpy as np

x = np.random.rand(1, 2)
y = np.random.rand(1, 3)
```

Remember that we consider these two sets of activation patterns to be paired,
we can note the $i$-th sample as two row vectors,
$(\mathbf{x}_i, \mathbf{y}_i)$ with dimensionality $p$.

We can formally express the Procrustes problem as:

```{math}
:label: procrustes_eq_1
\min_{\mathbf{R}= s\mathbf{M}} ||\mathbf{R} \mathbf{X} - \mathbf{Y}||_F^2 \\
s\in\mathbb{R^+}, \enspace \mathbf{M} \in \mathbb{R}^{p \times p} \text{ s.t. } \mathbf{M}^\intercal\mathbf{M} = \mathbf{I}_p
```

```{bibliography} references.bib
:style: unsrt
:filter: docname in docnames
```