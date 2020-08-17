# fmralign-tutorials

A collection of tutorials for functional alignment methods in fMRI data.
This repository does not include implementations of these methods; for this,
we recommend [BrainIAK](http://brainiak.org/),
[fmralign](https://github.com/Parietal-INRIA/fmralign), or
[pyMVPA](http://www.pymvpa.org/).

## Local Installation

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

You can render the tutorials using [`Jupytext`](https://jupytext.readthedocs.io/en/latest/),
which provides a convenient means to sync the user-friendly notebook interface with a git-friendly MyST markup.

For example, for the `02-procrustes` tutorial, simply run:

```bash
jupytext 02-procrustes.md --to notebook
jupytext --set-formats md:myst, ipynb 02-procrustes.md
jupytext --sync 02-procrustes.md 02-procrustes.ipynb
```

You can then launch the notebook using:

```bash
jupyter notebook 02-procrustes.ipynb
```

All changes you make there will be automatically updated in the associated MyST file.
