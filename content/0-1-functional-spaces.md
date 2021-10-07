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

# Functional space

There are other, non-spatial ways that we can conceptualize our data, however.
At each time point, we can look at the relative activation of each voxel and create multiple, unique representations of our data.
For example, three representations of a given voxelwise activation pattern might be:

- As a **histogram** showing the distribution of activity profiles
- As a **vector** of relative activations for each voxel
- As activity points in an **_N_-dimensional activation space**, where _N_ is equal to the number of voxels

Each of these methods are illustrated in {numref}`churchland-1998-fig1-png`.

Usually, we think of fMRI data as voxels in a 3D space of _x_, _y_, and _z_ coordinates.
Thinking of our data this way highlights the spatial relationship of each voxel;
i.e., how near or far it is from another voxel of interest.

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

## References

```{bibliography}
:style: unsrt
:filter: docname in docnames
```

## Other useful resources

- [3Blue1Brown video on high-dimensional spaces](https://www.youtube.com/watch?v=zwAD6dRSVyI)
- [Marc Khoury blog on counterintuitive properties of high-dimensional spaces](https://marckhoury.github.io/blog/counterintuitive-properties-of-high-dimensional-space)
