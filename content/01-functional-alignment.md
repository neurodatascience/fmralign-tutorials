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

What is "functional alignment"?
Although a range of terminology is in use across the field,
in these tutorials we define functional alignment as transformations which align directly individual functional activity,
without relying on anatomical landmarks.

## Contrasting anatomically-based alignment

With neuroimaging data, we usually make inferences across subjects by creating a mapping between each subject’s neuroanatomy;
this is usually done by normalizing their anatomical (T1-weighted) MRI scan to a standard template such as the MNI152.
We can then look at similarities across individuals in this standardized space.
Although this approach allows us to learnt commonalities across subjects, it can obscure important individual information.

A relevant analogy here is to the idea of face morphing.
Much like sulci and gyri in MRI data,
faces also have relevant landmarks (e.g. eyes) that can be used to generate a mapping between individual's faces.
Using these mappings can bring one or more faces into alignment, where they can then be averaged.

```{figure} ../images/average-president.jpg
---
height: 350px
name: average-president-jpg
---
An average face from six US presidents, generaged [using OpenCV](https://learnopencv.com/average-face-opencv-c-python-tutorial/).
With [thanks to Jack Gallant](https://smartech.gatech.edu/handle/1853/60990).
```

An "average face" retains important structure that is consistent across individuals,
but it does not resemble any of the individuals used to derive the average.

## High-dimensional functional spaces

Functional alignment doesn't use landmark information to generate its alignments.
To understand it, we need to think outside of the box—the box of three dimensions, that is.

Usually, we think of fMRI data in a 3D space of _x_, _y_, and _z_ coordinates.
This is not the only way to think about our data, however.
Instead, we can imagine a new space where our dimensions equal the number of voxels we’re comparing between subjects.
To keep things simple, let’s first pretend we are only interested in two voxels.

```{figure} ../images/voxel_space.gif
---
height: 375px
name: voxel-space-gif
---
Moving from anatomical space to a high-dimensional voxel space.
Here, we only consider two voxels to aid in visualization.
```

As we increase the number of voxels, we also increase the number of dimensions.

```{sidebar}
It quickly becomes unreasonable to visualize these new spaces, despite [what Geoff Hinton says](https://twitter.com/videodrome/status/1005887240407379969):

> To deal with hyper-planes in a 14-dimensional space, visualize a 3-D space and say "fourteen" to yourself very loudly. Everyone does it.
```

Instead of visualizing these spaces, then, we will simply have to reason about them.
This takes a bit of getting used to,
and it's important to note that [our default intution is often wrong](https://marckhoury.github.io/blog/counterintuitive-properties-of-high-dimensional-space)!
There are [good resources](https://www.youtube.com/watch?v=zwAD6dRSVyI) for learning to think in higher dimensions,
but here we'll focus on how we can learn to work with them.

At a high-level, the goal is to make two distributions of participant activity patterns look as similar as possible,
given certain constraints on the transformation.
The precise constraints differ according to the method; however, we are only interested in methods which generate linear mappings.
The resulting transformations, then, should improve functional similarity while retaining as much information as possible about individual participants or conditions.

The methods used to create these transformations can be considered as part of a broader class of "distribution alignment" methods.
Although distribution alignment is used in domain adaptation,
functional alignment is unique in that we have access to both the "source" and "target" distributions and are trying to learn a relationship between them,
rather than transferring a learnt relationship from one distribution to another.

The next four tutorials detail different methods for functionally aligning two (or more) high-dimensional, voxel spaces.