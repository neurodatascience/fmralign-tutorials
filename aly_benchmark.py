# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.3.2
#   kernelspec:
#     display_name: 'Python 3.7.6 64-bit (''fmralign'': conda)'
#     language: python
#     name: python37664bitfmraligncondacf2e1401738b4da68b8c38457b80e82a
# ---

# %% [markdown]
# # Functional alignment in ds1545
#
# In this notebook, we'll benchmark functional alignment strategies
# with [ds1545](https://openneuro.org/datasets/ds001545/versions/1.0.0).
# This dataset was generously shared by Aly and colleagues and is described
# in their original paper:
#
# > Aly M, Chen J, Turk-Browne NB, & Hasson U (2018).
# > Learning naturalistic temporal structure in the posterior medial network.
# > _Journal of Cognitive Neuroscience_ , _30_ (9): 1345-1365.
#
# Participants were shown clips from the film _Grand Budapest Hotel_ in either
# a fixed or temporally scrambled order.
# Of those clips shown temporally scrambled,
# the scrambling could either be consistent or inconsistent across runs.
# These three conditions were presented over three runs,
# and they are depicted graphically in the following figure.
#
# <img src="https://www.mitpressjournals.org/na101/home/literatum/publisher/mit/journals/content/jocn/2018/jocn.2018.30.issue-9/jocn_a_01308/20180730/images/large/01308f01c.jpeg" width=500>
#
# _Figure 1._ Experimental design. Figure reproduced from Aly et al (2018).

# %% [markdown]
# Data were downloaded from OpenNeuro and pre-processed with
# [fMRIPrep](http://fmriprep.readthedocs.io)
# [1.5.0-rc1](https://github.com/poldracklab/fmriprep/releases/tag/1.5.0rc1)
# using a generated Singularity image deployed on Compute Canada
# infrastructure.
#
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
# Generated reports were visually inspected for functional-anatomical
# coregistration.
# Importantly, these data were originally collected for a study that focused
# on the long-axis of the hippocampus.
# Therefore, the selected field-of-view excludes large portions of
# prefrontal cortex and cerebellum.
# An example visual report output is as shown below:
#
# <img src="https://gistcdn.githack.com/emdupre/d70b39cf5467410d89212d374c091b98/raw/db894eaa86203192ed3c2e9cc9e40530035f778a/sub-01_task-movie_run-1_desc-bbregister_bold.svg" width="700">
#
# _Figure 2._ An example visual report generated by fMRIPrep for ds1545.

# %% [markdown]
# ##  Accessing the dataset and defining a parcellation
#
# First, we'll need to download the preprocessed data.
# This data is [currently hosted](https://osf.io/vgj7w/) on the
# Open Science Framework (OSF), and we can access it using a simple
# [Nilearn-style](https://nilearn.github.io) fetcher.

# %%
from fetch_data import fetch_aly_2018

aly = fetch_aly_2018(n_subjects=2, n_runs=2)

# %% [markdown]
# Here, we'll use the 1000 node parcellation defined by Schaefer and colleagues
# (2018). The authors have assigned each parcel to one of the seven canonical
# "Yeo networks" from Yeo and colleagues (2011). We'll use this information
# to generate seven new "clusterings" &mdash; one for each network. We'll then
# calculate alignment transformations separately for each parcel within a given
# clustering.
#
# First, we can plot all ROIs within the Visual network clustering.

# %%
import numpy as np
from nilearn import (image, datasets, plotting)

schaefer = datasets.fetch_atlas_schaefer_2018(
    n_rois=1000, yeo_networks=7, resolution_mm=1)
atlas = image.load_img(schaefer.maps)
labels = [l.decode().split('_')[2] for l in schaefer.labels]
networks = np.unique(labels)
mapping = dict.fromkeys(networks)
for n in networks:
    affil = [True if n in l else False for l in labels]
    indic = [i + 1 for i, x in enumerate(affil) if x]
    data = np.array(atlas.dataobj, copy=True, dtype='int')
    data[~np.isin(data, indic)] = 0
    mapping[n] = image.new_img_like(atlas, data)

# %%
# %matplotlib inline
import matplotlib.pyplot as plt

resample_vis_clustering = image.resample_to_img(
    mapping['Vis'], image.mean_img(aly.func[0]),
    interpolation="nearest")
plotting.plot_roi(resample_vis_clustering)
plt.show()

# %% [markdown]
# We'll need to define a binarized version of this clustering to use as our NiftiMasker.
# We can generate this binarized clustering and display it using NiftiMasker's `generate_report` method.

# %%
import nibabel as nib
from nilearn import input_data

binarized_mask = nib.Nifti1Image(resample_vis_clustering.dataobj.astype(bool),
                                 header=resample_vis_clustering.header,
                                 affine=resample_vis_clustering.affine)
masker = input_data.NiftiMasker(mask_img=binarized_mask).fit()
masker.generate_report()

# %% [markdown]
# ## Defining and running the alignment
#
# We'll need to define our `source` and `target` datasets for alignment.
# Since we'd like to learn about the relative accuracy of the different methods being compared,
# we'll also define a `train` and `test` loop.
#
# Here, we'll use the first 60 TRs of stimulus presentation, corresponding to the first 90 seconds 'intact' clip.

# %%
indexed_fdata = [nib.load(f) for f in aly.func]

data_folds = ['source_train', 'source_test', 'target_train', 'target_test']
data_dict = dict(zip(data_folds, indexed_fdata))

# %%
from fmralign._utils import voxelwise_correlation
from fmralign.pairwise_alignment import PairwiseAlignment

methods = ['identity', 'scaled_orthogonal', 'ridge_cv']

for method in methods:
    alignment_estimator = PairwiseAlignment(
        clustering=resample_vis_clustering, mask=masker,
        alignment_method=method)
    alignment_estimator.fit(data_dict['source_train'], data_dict['target_train'])
    target_pred = alignment_estimator.transform(data_dict['source_test'])
    aligned_score = voxelwise_correlation(data_dict['target_test'], target_pred, masker)

    # And we can plot the outcomes
    title = "Correlation of prediction after {} alignment".format(method)
    display = plotting.plot_stat_map(aligned_score, display_mode="z",
                                     vmax=1, title=title)

# %% [markdown]
# ## Deriving a template for alignment
#
# Next, we'd like to derive a 'template' alignment.
# This means that we'll align subjects to a randomly chosen reference.
# We'll then iterate on the resulting average alignment,
# and re-align all subjects to create a common template.

# %%
aly = fetch_aly_2018(n_subjects=3, n_runs=1)

template_train = [nib.load(f) for f in aly.func]
target_train = template_train.pop()

# %%
from fmralign.template_alignment import TemplateAlignment

methods = ['identity', 'scaled_orthogonal', 'ridge_cv']
    
for method in methods:
    alignment_estimator = TemplateAlignment(
        clustering=resample_vis_clustering, mask=masker,
        alignment_method=method)
    alignment_estimator.fit(template_train)

# %%

# %%
