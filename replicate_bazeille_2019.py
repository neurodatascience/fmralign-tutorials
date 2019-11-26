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
#     display_name: Python [conda env:fmralign] *
#     language: python
#     name: conda-env-fmralign-py
# ---

# %% [markdown]
# # Replicating Bazeille et al. (2019)
#
# In this notebook, we'd like to replicate several of the core results reported in the recent paper:
#
# > Bazeille, Richard, Janati, & Thirion (2019). [_Local optimal transport for functional brain template estimation_](https://hal.archives-ouvertes.fr/hal-02278663/). doi: 10.1007/978-3-030-20351-1_18.
#
# For full details on the data and methods used here, please refer to their work!
#
# In order to match their results as closely as possible, we'll use the exact same dataset of [Individual Brain Charting (IBC)](https://project.inria.fr/IBC/) subject-level contrast maps which they have generously [shared on OSF](https://osf.io/69wvq/).
#
# Since it was unclear which parcellation was adopted in calculating local functional alignment transformations, we'll use the [Bootstrap Analysis of Stable Clustering (BASC) multiscale parcellation](https://nilearn.github.io/modules/generated/nilearn.datasets.fetch_atlas_basc_multiscale_2015.html) distributed through [_Nilearn_](https://nilearn.github.io).
# We'll use the finest scale of this parcellation, with 444 defined clusters.

# %%
import itertools
import numpy as np
import nibabel as nib
from nilearn import datasets
from fmralign.fetch_example_data import fetch_ibc_subjects_contrasts

basc = datasets.fetch_atlas_basc_multiscale_2015()
basc_444 = basc['scale444']

files, df, mask = fetch_ibc_subjects_contrasts(subjects=['sub-01', 'sub-02', 'sub-04',
                                                         'sub-05', 'sub-06', 'sub-07',
                                                         'sub-08', 'sub-09', 'sub-11', 
                                                         'sub-12', 'sub-13', 'sub-14',
                                                         'sub-15'])


# %% [markdown]
# Following Bazeille and colleagues, we'll also define a "reconstruction error;" that is, the error of the functional alignment predicted signal in reconstructing or matching the target subject.
#
# It can be mathematically expressed as:
#
# $$
# {\eta}^2_*(Y, Y_i, X) = 1 - \dfrac{\Sigma^n_{i=1}(Y_i - R_iX)^2}{\Sigma^n_{i=1}Y^2_i}
# $$
#
# where $*$ indicates the alignment method of interest such as `scaled_orthogonal` alignment.

# %%
def reconstruction_error(truth, pred):
    """
    Calculates the reconstruction error
    as defined by Bazeille and
    colleagues (2019).
    
    A perfect prediction yields a value of 1.
    """
    truth = nib.load(truth).get_fdata()
    pred = np.squeeze(pred.get_fdata())
    num = np.sum((truth - pred)**2)
    den = np.sum(truth**2)
    return 1 - (num / den)


# %% [markdown]
# In this notebook, we'd like to replicate part of _Figure 4a_ (reproduced below).
# Specifically, we'd like to replicate the range of reconstruction errors seen for each alignment method.
# In order to be sure that we're defining everything correctly, we'll first start with the `scaled orthogonal` alignment since this is computationally efficient.
#
# <img src='./Bazeille_2019_fig4a.png' width='500'>

# %% [markdown]
# To do so, we need to define an additional metric.
# Because considering the reconstruction error in isolation may not give us full insight into the increase in prediction gained by functional alignment, we may want to compare it against an `identity` alignment, where we predict that the target subject will exactly match the source subject.
# This is the "reconstruction ratio" defined by Bazeille and colleagues (2019):
#
# $$
# R_{{\eta}^2_*}(Y, R, X) = 1 - \dfrac{\Sigma^n_{i=1}(Y_i - R_iX)^2}{\Sigma^n_{i=1}(Y_i - X_i)^2} = 1 - \dfrac{1 - {\eta}^2_*(Y, R_i, X)}{1 - {\eta}^2_{id}(Y, Id, X)}
# $$
#
# Here, the ratio is greater than zero if voxels are predicted better by aligned data than by raw data.

# %%
from fmralign.pairwise_alignment import PairwiseAlignment

def orthogonal_alignment(source_train, target_train,
                         source_test, target_test,
                         clustering=basc_444):
    alignment_estimator = PairwiseAlignment(alignment_method='scaled_orthogonal',
                                            clustering=clustering,
                                            standardize=True)
    alignment_estimator.fit(source_train, target_train)
    target_pred = alignment_estimator.transform(source_test)
    orthogonal_error = reconstruction_error(target_test, target_pred)
    return orthogonal_error


# %%
def identity_alignment(source_train, target_train,
                       source_test, target_test,
                       clustering=basc_444):
    alignment_estimator = PairwiseAlignment(alignment_method='identity',
                                            clustering=clustering,
                                            standardize=True)
    alignment_estimator.fit(source_train, target_train)
    target_pred = alignment_estimator.transform(source_test)
    identity_error = reconstruction_error(target_test, target_pred)
    return identity_error


# %%
def reconstruction_ratio(aligned_error, identity_error):
    """
    Calculates the reconstruction error
    as defined by Bazeille and
    colleagues (2019).
    
    A value greater than 0 indicates that
    voxels are predicted better by aligned data
    than by raw data.
    """
    num = 1 - aligned_error
    den = 1 - identity_error
    return 1 - (num / den)


# %% [markdown]
# Now, with everything defined, we're ready to run our replication!

# %%
def run_experiment(df):
    condition_list = df.condition.unique()
    subject_list = df.subject.unique()
    pairs = list(itertools.combinations(subject_list, 2))
    
    vals = []
    for p in pairs:
        for c in condition_list:
            source_train = df[(df.subject == p[0]) &
                          (df.acquisition == 'ap') &
                          (df.condition == c)].path.values.item()
            target_train = df[(df.subject == p[1]) &
                              (df.acquisition == 'ap') &
                              (df.condition == c)].path.values.item()
            source_test = df[(df.subject == p[0]) &
                             (df.acquisition == 'pa') &
                             (df.condition == c)].path.values.item()
            target_test = df[(df.subject == p[1]) &
                             (df.acquisition == 'pa') &
                             (df.condition == c)].path.values.item()

            orthogonal_error = orthogonal_alignment(source_train, target_train,
                                                    source_test, target_test)
            identity_error = identity_alignment(source_train, target_train,
                                                source_test, target_test)
            vals.append(reconstruction_ratio(orthogonal_error, identity_error))
    return vals


# %%
# This is computationally intensive, and won't run on mybinder
# vals = run_experiment(df)

# Instead, we can load a file containing the values
# these were generated by running the above code on my local machine
vals = np.loadtxt('./ibc_reconstruction_ratios.txt')

# %%
# %matplotlib inline
import seaborn as sns
sns.set(style="whitegrid")

ax = sns.violinplot(x=vals)

# %% [markdown]
# The derived values do not match those seen by Bazeille and colleagues.
# Notably, although we have a similar central tendency, we have no negative reconstruction ratio values.
#
# Possible sources of the discrepancy are that we ran this for all 78 possible IBC subject pairs, rather than a randomly selected 20 pairs.

# %%
