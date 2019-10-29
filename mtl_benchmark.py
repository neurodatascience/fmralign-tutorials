# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.2'
#       jupytext_version: 1.2.4
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# # Functional alignment in ds1545
#
# In this notebook, we'll benchmark functional alignment strategies with [ds1545](https://openneuro.org/datasets/ds001545/versions/1.0.0).
# This dataset was generously shared by Aly and colleagues and is described in their original paper:
#
# > Aly M, Chen J, Turk-Browne NB, & Hasson U (2018). Learning naturalistic temporal structure in the posterior medial network. _Journal of Cognitive Neuroscience_ , 30(9): 1345-1365.
#
# Participants were shown clips from the film _Grand Budapest Hotel_ in either a fixed or temporally scrambled order. Of those clips shown temporally scrambled, the scrambling could either be consistent or inconsistent across runs. These three conditions were presented over three runs, and are depicted graphically in the following figure.
#
# <img src="https://www.mitpressjournals.org/na101/home/literatum/publisher/mit/journals/content/jocn/2018/jocn.2018.30.issue-9/jocn_a_01308/20180730/images/large/01308f01c.jpeg" width=500>
#
# _Figure 1._ Experimental design. Figure reproduced from Aly et al (2018).

# %% [markdown]
# Data were downloaded from OpenNeuro and pre-processed with [fMRIPrep](http://fmriprep.readthedocs.io) [1.5.0-rc1](https://github.com/poldracklab/fmriprep/releases/tag/1.5.0rc1) using a generated Singularity image deployed on Compute Canada infrastructure.
# Specifically, the following flags were provided:
#
# ```
# singularity run -B ${DATADIR}:/data:ro \
#         -B ${OUTDIR}:/out \
#         -B ${SIMGDIR}/license.txt:/license/license.txt:ro \
#         ${SIMGDIR}/fmriprep-1.5.0rc1.simg \
#         /data /out participant \
#         --participant-label sub-${sub} \
#         --output-space fsaverage5 template \
#         -w /out/workdir \
#         --notrack \
#         --fs-license-file /license/license.txt
# ```
#
# Generated reports were visually inspected for functional-anatomical coregistration.
# Importantly, these data were originally collected for a study that focused on the long-axis of the hippocampus.
# Therefore, the selected field-of-view excludes large portions of prefrontal cortex and cerebellum.
# An example visual report output is as shown below:
#
# <img src="https://gistcdn.githack.com/emdupre/d70b39cf5467410d89212d374c091b98/raw/db894eaa86203192ed3c2e9cc9e40530035f778a/sub-01_task-movie_run-1_desc-bbregister_bold.svg" width="600">
#
# _Figure 2._ An example visual report generated by fMRIPrep for ds1545.

# %% [markdown]
# ##  Accessing the dataset and selecting a region-of-interest
#
# First, we'll need to download the preprocessed data.
# This data is [currently hosted](https://osf.io/vgj7w/) on the Open Science Framework (OSF), and we can access it using a simple [Nilearn-style](https://nilearn.github.io) fetcher.

# %%
from fetch_data import fetch_mtl_fmri

# Here, we're using the nickname MTL for the Medial Temporal Lobe,
# since the original publication with ds1545 focused on this region
mtl = fetch_mtl_fmri(n_subjects=2, n_runs=2)

# %% [markdown]
# Given the limited field-of-view, in this notebook we will focus our investigations on regions of interest (ROIs) within the ventral visual stream.
# We can select an ROI previously defined by Haxby and colleagues (2001) in the ventral temporal cortex.
# We'll access this ROI with Nilearn.

# %%
from nilearn import (datasets, image, plotting)

atlas_schaefer_2018 = datasets.fetch_atlas_schaefer_2018(
    n_rois=800, yeo_networks=17, resolution_mm=2)
atlas = image.load_img(atlas_schaefer_2018.maps)
mask = image.new_img_like(atlas, atlas.get_data() == 5)
resampled_mask = image.resample_to_img(
    mask, image.mean_img(mtl.func[0]), interpolation="nearest")

# %%
# %matplotlib inline
from nilearn.input_data import NiftiMasker

roi_masker = NiftiMasker(mask_img=resampled_mask).fit()
roi_masker.generate_report()

# %% [markdown]
# ## Defining and running the alignment
#
# We'll need to define our `source` and `target` datasets for alignment.
# Since we'd like to learn about the relative accuracy of the different methods being compared,
# we'll also define a `train` and `test` loop.
#
# To keep our investigations computationally tractable, we'll only use the first ten volumes for each image,
# indexed using Nilearn's `index_img` function.

# %%
import fmralign

files = []
keys  = ['source_train', 'target_train', 'source_test', 'target_test']

for i, k in enumerate(keys):
    files.append(image.index_img(mtl.func[i], index=slice(0,10)))
    
data = dict(zip(keys, files))

# %% [markdown]
# Alignment is performed in local neighborhoods, so we'll first parcellate our functional scans using [ReNA clustering](https://arxiv.org/abs/1609.04608).
# Because we don't want our parcels to be overly large &mdash;as this would signifcantly increase the computational cost&mdash; we'll explictly set the number of parcels.
# In this case, we'll set the number of parcels such that each contains approximately 200 voxels.

# %%
import warnings
warnings.simplefilter(action='ignore', category=(DeprecationWarning,
                                                 FutureWarning,
                                                 UserWarning))

from fmralign.pairwise_alignment import PairwiseAlignment
from fmralign._utils import voxelwise_correlation
methods = ['identity', 'scaled_orthogonal', 'ridge_cv']

for method in methods:
    alignment_estimator = PairwiseAlignment(alignment_method=method, n_pieces=1,
                                            clustering='rena', mask=roi_masker)
    alignment_estimator.fit(data['source_train'], data['target_train'])
    target_pred = alignment_estimator.transform(data['source_test'])
    # calculate and display the performance of the alignment estimator
    aligned_score = voxelwise_correlation(data['target_test'], target_pred, roi_masker)
    display = plotting.plot_stat_map(aligned_score,
                                     title=f"Correlation of prediction after {method} alignment")

# %%
