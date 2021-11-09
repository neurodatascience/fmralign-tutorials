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

# Distribution alignment

Traditionally, we would extract the activity time courses for voxels of interest,
such that we had two graphs of voxel activity over time.
We could then compare the similarity of these time courses using techniques such as correlation.
To compare across individuals or brain states, then, we would compare summary-level statistics from e.g. network analysis.

As shown in {numref}`churchland-1998-fig2-png`,
our question then is how best to find correspondence between two (or more) unique functional spaces.

```{figure} ../images/churchland-1998-fig2.png
---
height: 375px
name: churchland-1998-fig2-png
---
The locations of four protoype points within the voxelwise activation spaces of two brains.
Figure adapted from {cite:t}`Churchland1998-lw`.
```

## Formalizing the problem

Suppose we have two data distributions, $X$ and $Y$.
These distributions may come from voxel activity time series sampled from two different participants
or from the same participant in two different psychological tasks.

Each distribution contains a series of $n$ observations, such that
$X = \{\mathbf{x}_1, \ldots, \mathbf{x}_n\}$
where $\mathbf{x}_i \in \mathbb{R}^p$.

For fMRI data, then, $n$ would be the number of time points sampled,
while $p$ is the number of voxels considered.

To deal with these equations more easily, we'll need to stack the values of $x$ and $y$ into matrices.
Let's define those matrices like this:

```{math}
Y = \begin{bmatrix} y(i=1) \\\\ y(i=2) \\\\ \vdots \\\\ y(i=n) \end{bmatrix},
X = \begin{bmatrix} x(i=1) \\\\ x(i=2) \\\\ \vdots \\\\ x(i=n) \end{bmatrix}
```

Now we have our two distributions
$\mathbf{X} \in \mathbb{R}^{n \times p}$ and
$\mathbf{Y} \in \mathbb{R}^{n \times p}$.

For some methods, we will enforce that every distribution has exactly the same number of voxels $p$.
Other methods will allow the number of voxels to vary across distributions.
When variable voxels are allowed, we will denote the number of voxels as $p_1$ or $p_2$,
corresponding to the relevant distribution.

```{note}
Some _latent factor models_ reduce the number of dimensions using an initial decomposition.
The idea is that there may be several latent factors supporting voxel-level activity patterns,
and we can therefore capture relevant information even in a lower dimensional space.
```

## References

```{bibliography}
:style: unsrt
:filter: docname in docnames
```
