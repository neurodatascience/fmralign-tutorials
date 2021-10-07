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

# fmralign tutorials

This is a series of tutorials to introduce the idea of "functional alignment" and associated statistical methods.
We aim to provide the intuitions behind each method alongside their implementations.

Although this class of methods is broadly referred to as both _functional alignment methods_ and _hyperalignment methods_,
we adopt the term _functional alignment methods_ to better distinguish from the specific Procrustes-based hyperalignment method in use in the literature.

Please note that these tutorials do not provide new implementations for functional alignment.
There are already many of these available in existing software toolboxes,
including [fmralign](https://parietal-inria.github.io/fmralign-docs),
[PyMVPA](http://www.pymvpa.org/), or [BrainIAK](https://brainiak.org/).

## What we'll cover

First, we provide a brief summary of the intutions behind functional alignment.
We then review five of the most popular methods for functional alignment:

1. Ridge regression
2. Procrustes analysis
3. Optimal transport
4. Canonical Correlation Analysis (CCA)
5. Shared Response Modelling (SRM)

For each method, we provide mathematical formalisms and corresponding Python code.
We also point to optimized implementations available in other software libraries for use on real-world data.

## Running the tutorials

These tutorials are developed as a [Jupyter Book](https://jupyter-book.org),
which means that you can view the text, code, and outputs directly in your web browser.
If you would like to run or modify the code yourself,
you can do so using the [Binder](https://mybinder.org) links available on each page.
You can also download and run these files locally.

## Related work

Although functional alignment is used across several fields and research contexts,
in these tutorials we draw on examples from our own field of cognitive neuroscience.
The associated code and methods, however, can easily be adapted for other domains.
For interested readers, we include a brief overview of applications in other fields and annotated bibliography in the final section.
