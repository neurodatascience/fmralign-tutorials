---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# What functional alignment alignment is not

There are two other popular methods in the cognitive neuroscience literature which provide alternative solutions to the problem of individual variability: individualized parcellations and Representational Similarity Analysis (RSA).
Although not the focus of this site,
we briefly contrast these methods with functional alignment to provide a clearer understanding of what functional alignment entails.

## Individualized parcellations

High-dimensional neural recordings, such as those achieved through fMRI,
measure hundreds of thousands of voxels over hundreds of time points.
Computationally, working with this data thus demands some kind of dimensionality reduction.
Although many forms of dimensionality reduction have been explored,
perhaps the most popular method involves parcellating the brain into a set of functional regions.

This method has a strong sense of biological validity,
as we know that the brain shows cytoarchitectonic and functional differences across both cortex and sub-cortex.
Although functional parcellations can be directly estimated from an individual's fMRI scans,
variability in their localization makes inter-subject comparison difficult.
Many investigators, therefore, choose to rely on canonical parcellations derived from a different group of participants, such as the Schaefer or BASC parcellations.

Because these are group-averaged parcellations, however,
we now have the opposite problem--that these parcellations do not appropriately reflect individual-level functional structure!
As a result, new methods are being actively developed to "individualize parcellations."
That is, to take a canonical parcellation and alter the spatial extent or localization of its parcels such that it better reflects individual-level organization while still being comparable across the group.

Although the intuition behind individualizing parcellations can be viewed as a form of functional alignment,
there is one large conceptual difference.
When we parcellate fMRI data,
we know that this is a useful form of dimensionality reduction.
It is unlikely, however, that the identified areas reflect "true" functional modules in the brain.
This requires a much higher evidence-threshold,
such as converging cytoarchitectonic boundaries.
By individualizing functional parcels,
we implicitly agree that we expect this set of parcels to exist across all individuals.
It may be possible to describe the data using the set of parcels,
but this does not guarantee that these parcels in fact exist across individuals
or that they reflect the true data-generating process.

Rather than using pre-established parcels as their starting point,
functional alignment methods use the individual functional units.
In the case of fMRI data, therefore,
alignment transformations are computed directly on the voxels.
Functional alignment can be computed _within_ a parcel,
and this serves to regularize the resulting transformation.
There is no assumption however--implicit or otherwise--that fMRI data can be well-described by a given parcellation.

## Representational Similarity Analysis (RSA)

Much like functional alignment,
RSA focuses on comparing representational geometries across subjects.
RSA does this, however, in service of a representational model.
That is, we have particular stimuli or stimulus classes which are chosen by the experimenter to reflect putative properties of the brain's functional organization.

For example, we could consider how animacy vs inanimacy is differently encoded in a given cortical region.
We would present many animate or inanimate stimuli,
and use these stimuli to define our representational geometry.
We could then compare this labelled representational geometry with an exisiting representational model,
or with data collected using the same paradigm in a different modality
such as behavioral reports.

Functional alignment does not have the same reliance on stimuli.
Ideal functional alignment stimuli are those which richly sample functional space (such as a Hollywood movie)
rather than stimuli which precisely align to an investigator's hypothesis.
As a result, functional alignment methods do not provide a clear path to representational models,
even though--like RSA--they involve examining individual-level representational geometries.