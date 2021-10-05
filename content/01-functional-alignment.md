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

# Overview

Functional alignment directly align individual functional activity without relying on anatomical landmarks.
To do so, we learn transformations in a high-dimensional functional space,
rather than in the three-dimensional space in which we consider anatomically-based transformations.

## High-dimensional functional spaces

Usually, we think of fMRI data as voxels in a 3D space of _x_, _y_, and _z_ coordinates.
Thinking of our data this way highlights the spatial relationship of each voxel;
i.e., how near or far it is from another voxel of interest.

There are other, non-spatial ways that we can conceptualize our data, however.
At each time point, we can look at the relative activation of each voxel and create multiple, unique representations of our data.
For example, three representations of a given voxelwise activity pattern might be:

- As a **histogram** showing the distribution of activity profiles
- As a **vector** of relative activations for each voxel
- As activity points in an **_N_-dimensional activation space**, where _N_ is equal to the number of voxels

Each of these methods are illustrated in {numref}`churchland-1998-fig1-png`.

```{figure} ../images/churchland-1998-fig1.png
---
height: 375px
name: churchland-1998-fig1-png
---
Three different ways of conceptualizing a given voxelwise activity pattern:
a histogram of activation levels, an activation vector, or a point in activation space.
Figure adapted from {cite:t}`Churchland1998-lw`.
```

Importantly, there is no reason that we need to limit these non-spatial representation to only a single timepoint.
That is, we can define a new two-dimensional space,
where each dimension corresponds to one voxel's activity.
For each time point,
we then include a single data point that indexes the relative activity of each voxel at that time point.
This basic idea is illustrated in {numref}`voxel-space-gif`.

```{figure} ../images/voxel_space.gif
---
height: 375px
name: voxel-space-gif
---
Moving from anatomical space to a high-dimensional voxel space.
Here, we only consider two voxels to aid in visualization.
```

Although each of these representations equivalently summarize the data,
we focus on the _N_-dimensional activity space to highlight a more geometric intuition for these methods.
Note that as we increase the number of voxels, we also increase the number of dimensions.

```{margin}
Some _latent factor models_ reduce the number of dimensions using an initial decomposition.
The idea is that there may be several latent factors supporting voxel-level activity patterns,
and we can therefore capture relevant information even in a lower dimensional space.
We will cover one such latent factor model, the Shared Response Model, in these tutorials.
```

## Comparing across functional spaces

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

If we stack all of our data points into two matrices
--one for each distribution-- we can represent our two distributions as
$\mathbf{X} \in \mathbb{R}^{n \times p}$ and
$\mathbf{Y} \in \mathbb{R}^{n \times p}$.

For some methods, we will enforce that every distribution has exactly the same number of voxels $p$.
Other methods will allow the number of voxels to vary across distributions.
When variable voxels are allowed, we will denote the number of voxels as $p_1$ or $p_2$,
corresponding to the relevant distribution.

## Finding similarity with functional alignment

At a high-level, the goal of functional alignmentis to make two distributions of participant activity patterns look as similar as possible,
given certain constraints on the transformation.
The precise constraints differ according to the method; however, we are only interested in methods which generate linear mappings.
The resulting transformations, then, should improve functional similarity while retaining as much information as possible about individual participants or conditions.

The methods used to create these transformations can be considered as part of a broader class of "distribution alignment" methods.
Although distribution alignment is used in domain adaptation,
functional alignment is unique in that we generally have access to both the "source" and "target" distributions and are trying to learn a relationship between them,
rather than transferring a learnt relationship from one distribution to another.

The next five tutorials detail different methods for functionally aligning two (or more) high-dimensional, voxel spaces.

## Useful resources

- [3Blue1Brown video on high-dimensional spaces](https://www.youtube.com/watch?v=zwAD6dRSVyI)
- [Marc Khoury blog on counterintuitive properties of high-dimensional spaces](https://marckhoury.github.io/blog/counterintuitive-properties-of-high-dimensional-space)

```{bibliography} references.bib
:style: unsrt
:filter: docname in docnames
```
