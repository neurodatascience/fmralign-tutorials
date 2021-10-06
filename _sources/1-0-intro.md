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

# Inclusion criteria

At a high-level, the goal of functional alignment is to make two distributions of participant activity patterns look as similar as possible,
given certain constraints on the transformation.
The precise constraints differ according to the method; however, we are only interested in methods which generate linear mappings.
The resulting transformations, then, should improve functional similarity while retaining as much information as possible about individual participants or conditions.

The methods used to create these transformations can be considered as part of a broader class of "distribution alignment" methods.
Although distribution alignment is used in domain adaptation,
functional alignment is unique in that we generally have access to both the "source" and "target" distributions and are trying to learn a relationship between them,
rather than transferring a learnt relationship from one distribution to another.

The next five tutorials detail different methods for functionally aligning two (or more) high-dimensional, voxel spaces.
