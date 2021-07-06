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

# Functional alignment

What is functional alignment—often referred to in the cognitive neuroscience literature as “hyperalignment”—is a class of methods for improving the inferences we can draw across participants.
Why would we need to do this?

First, let’s consider our goals.
Generally, cognitive neuroscience is interested in understanding how psychological constructs like memory or decision-making are implemented in the brain.
There are many well-known challenges to achieving this understanding: from construct definition to experimental design to measurement noise.
Even if we could solve all of these problems, we would still face another challenge:
how can we make sure our findings extend to new participants?

## Contrasting anatomically-based alignment

Specifically for neuroimaging data, we usually make inferences across subjects by creating a mapping between each subject’s neuroanatomy.
This is usually done by normalizing their anatomical (T1-weighted) MRI scan to a standard template such as the MNI152. But there are limits to this approach.
Individual differences in structure-function mapping mean that the same function can be supported by different neural circuits across individuals.
In fMRI, we usually compensate for these differences by smoothing our images with a Gaussian kernel.
Although this allows us to improve our statistical power, it also throws away relevant information about individual differences.

Functional alignment takes a different approach.
To understand it, we need to think outside of the box—the box of three dimensions, that is.

## What to align?

Usually, we think of fMRI data in a 3D space of _x_, _y_, and _z_ coordinates.

< insert visualization >

This is not the only way to think about our data, however.
Instead, we can imagine a new space where our dimensions equal the number of voxels we’re comparing between subjects.
To keep things simple, let’s first pretend we have a toy region-of-interest with only three voxels.

```{figure} ../images/voxel_space.gif
---
height: 400px
name: voxel-space-gif
---
Moving from anatomical space to a high-dimensional voxel space.
Here, we only consider two voxels to aid in visualization.
```

As we increase the number of voxels in our region of interest, we also increase the number of dimensions.
It quickly becomes unreasonable to visualize these new spaces, despite [what Geoff Hinton says](https://twitter.com/videodrome/status/1005887240407379969):

> To deal with hyper-planes in a 14-dimensional space, visualize a 3-D space and say "fourteen" to yourself very loudly. Everyone does it.

Instead of visualizing these spaces, then, we will simply have to reason about them.
This takes a bit of getting used to, and it's important to note that [our default intution is often wrong](https://marckhoury.github.io/blog/counterintuitive-properties-of-high-dimensional-space)!
There are [good resources](https://www.youtube.com/watch?v=zwAD6dRSVyI) for learning to think in higher dimensions, but here we'll focus on how we can learn to work with them.
The next four tutorials detail different methods for functionally aligning two (or more) high-dimensional, voxel spaces.