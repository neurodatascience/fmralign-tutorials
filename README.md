# fmralign-tutorials

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/neurodatascience/fmralign-tutorials/master)

A collection of tutorials for functional alignment methods in fMRI data.
This repository does not include implementations of these methods; for this,
we recommend [BrainIAK](http://brainiak.org/),
[fmralign](https://github.com/Parietal-INRIA/fmralign), or
[pyMVPA](http://www.pymvpa.org/).

Here, we demonstrate functional alignment methods using the publicly accessible [MTL dataset](https://osf.io/vgj7w/), generously shared by Aly and colleagues.
For more information on the acquisition of this data set, please see their paper:

> Aly M, Chen J, Turk-Browne NB, & Hasson U (2018).
  Learning naturalistic temporal structure in the posterior medial network.
  _Journal of Cognitive Neuroscience_, 30(9): 1345-1365.

Data were pre-processed using [fMRIPrep](https://fmriprep.readthedocs.io) version 1.5.0rc1.
For a full description of the pipeline, please see the Open Science Framework [README](https://osf.io/479pt/).

## Installation

To access this material locally, you can download this repository and install the requirements using `pip`.
We recommend that you install these requirements within a virtual environment;
for example, the following commands will create a conda environment and install all necessary packages:

```bash
git clone https://github.com/neurodatascience/fmralign-tutorials
cd fmralign-tutorials
conda create --name fmralign-tutorials python=3.6
source activate fmralign-tutorials
pip install -r requirements.txt
```

You can render main tutorial using [`Jupytext`](https://jupytext.readthedocs.io/en/latest/), which provides a convenient means to sync the user-friendly notebook interface with a git-friendly plain-text Python script.

To do so, simply run:

```bash
jupytext mtl_benchmark.py --to notebook
jupytext sync mtl_benchmark.py mtl_benchmark.ipynb
```

You can then launch the notebook using:

```bash
jupyter notebook mtl_benchmark.ipynb
```

All changes you make there will be automatically updated in the associated Python script.
