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
in these tutorials we define functional alignment as transformations which directly align individual functional activity without relying on anatomical landmarks.

## Contrasting anatomically-based alignment

With neuroimaging data, we usually make inferences across subjects by creating a mapping between each subject’s neuroanatomy;
this is usually done by normalizing their anatomical (T1-weighted) MRI scan to a standard template such as the MNI152.
We can then look at similarities across individuals in this standardized space.
Although this approach allows us to learnt commonalities across subjects, it can obscure important individual information.

A relevant analogy here is to the idea of face morphing,
as shown in {numref}`average-president-jpg`.
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

Traditionally, we would extract the activity time courses for these voxels,
such that we had two graphs of voxel activity over time.
We could then compare the similarity of these time courses using techniques such as correlation.
An alternative way to think about these voxel activity profiles is in a new, functional space.
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

Note that as we increase the number of voxels, we also increase the number of dimensions.

```{margin}
Some _latent factor models_ reduce the number of dimensions using an initial decomposition.
The idea is that there may be several latent factors supporting voxel-level activity patterns,
and we can therefore capture relevant information even in a lower dimensional space.
We will cover one such latent factor model, the Shared Response Model, in these tutorials.
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

## Constraining functional alignment to local neighborhoods

Since functional alignment is not guided by anatomical landmarks,
considering a large number of voxels can generate biologically implausible transformations.
For example, we may maximize distribution similarity while aligning voxel activity from one participant's visual cortex to another participant's prefrontal cortex.
To avoid this, we can constrain the voxels included in calculating each functional alignment transformation to smaller, local neighborhoods.

A relevant neighborhood might be defined by an _a priori_ region of interest (ROI).
That is, a researcher may have identified a relevant patch of cortex through functional localizers or anatomical tracing.
They can then only consider voxels within this ROI and functionally align their activity across participants.

To generate a whole brain transformation, however, we must define many more local neighborhoods.
There are two primary strategies to do so.
The first is through a deterministic or non-overlapping parcellation.
This can be considered as an extension of the ROI-based approach, in that we now have as many ROIs as there are parcels.
Transformations are calculated separately for each parcel and then aggregated into a larger whole brain transformation matrix.

Alternatively, we can define our local neighborhoods using a searchlight approach.
Here, a searchlight is a small sphere of defined radius that we can iterate through a brain volume.
Importantly, the centroids of each searchlight are selected such that the spheres slightly overlap.
When generating an aggregated transformation, then, this overlap must be accounted for in the transformation itself;
for example, by averaging or summing the calculated transformation from two overlapping searchlights.
You can see an example of these different local neighborhood methods in {numref}`parcellation-searchlight-png`.

```{figure} ../images/parcellation_v_searchlight.png
---
height: 350px
name: parcellation-searchlight-png
---
Two different methods to constrain functional alignment transformations:
non-overlapping parcels from a deterministic parcellation or partially overlapping searchlights.
```

Importantly, when functional alignment transformations are aggregated using the searchlight methods,
the final transformations are no longer guaranteed to have the same properties as the initial, unaggregated transforms.