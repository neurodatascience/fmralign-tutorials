---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3
  name: python3
---

# Comparing representational geometries with functional alignment

Cognitive neuroscience is broadly interested in how cognition is represented in the brain;
that is, how psychological constructs like memory, emotion, or decision-making are implemented in brain regions or networks of regions.
There are many challenges to achieving this understanding,
from providing precise, testable definitions for our psychological constructs
to accounting for noise in our measurements.

Perhaps the broadest challenge, however, is the sheer diversity of realizations that we see for a given psychological process or neural circuit.
That is, individual participants (human or animal) may show very different neural and behavioral patterns to achieve the same goal.
These individual differences are an important area of study;
however, traditional analyses are designed to compare those patterns which hold across individuals and discard individual variability as noise.

Recently, new analysis methods have emerged which account for this variability.
One example is _functional alignment_ methods,
also known as _hyperalignment_ methods.
In traditional analyses, we ensure that the anatomy of our participants is aligned by registering their scans to a standardized template (such as the MNI152).
Functional alignment extends this intuition to the collected functional scans;
for example, fMRI time series.
Our goal, then, is to align the representational geometry of each subject,
much as we align their structural geometry.

## What's all this about then?

This site is intended as a collection of tutorials for several popular functional alignment methods.
We aim to provide the intuitions behind each method,
some mathematical derivations,
and an example implementation on toy data.

There are many resources for applying functional alignment methods to domain-specific data.
For fMRI data, we recommend [fmralign](https://parietal-inria.github.io/fmralign-docs),
[PyMVPA](http://www.pymvpa.org/),
or [BrainIAK](https://brainiak.org/).
