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
# In order to match their results as closely as possible, we'll use the same dataset of [Individual Brain Charting (IBC)](https://project.inria.fr/IBC/) subject-level contrast maps which the authors have generously [shared on OSF](https://osf.io/69wvq/).
#
# Since it was unclear which parcellation was adopted in calculating local functional alignment transformations, we'll use the [schaefer multiscale parcellation](https://nilearn.github.io/modules/generated/nilearn.datasets.fetch_atlas_schaefer_2018.html) distributed through [_Nilearn_](https://nilearn.github.io).
# We'll use the finest scale of this parcellation, with 1000 defined clusters.

# %%
import itertools
import numpy as np
import nibabel as nib
from nilearn import datasets
from fmralign.fetch_example_data import fetch_ibc_subjects_contrasts

schaefer = datasets.fetch_atlas_schaefer_2018(n_rois=1000,
                                              yeo_networks=17,
                                              resolution_mm=2)
files, df, mask = fetch_ibc_subjects_contrasts(subjects="all")

# %% [markdown]
# This is a rich dataset, with 53 unique conditions acquired in both poster-to-anterior (PA) and anterior-to-posterior (AP) phase-encoding sessions.
# We'd like to compare functional alignment accuracy across all of these contrast maps.
#
# Here, we'll also focus on results derived from pairwise alignment.
# Since there are 13 unique subjects, we have ${13 \choose 2} = 78$ possible subject pairs.
# We'll randomly select 20 pairs to mimic the randomly chosen 20 subject pairs of the original paper.

# %%
import random
random.seed(a=18)

condition_list = df.condition.unique()
subject_list = df.subject.unique()
possible_pairs = list(itertools.combinations(subject_list, 2))
pairs = random.sample(possible_pairs, 20)
pairs


# %% [markdown]
# For each subject pair, we now need to define our training and test set for each of the 53 unique conditions.
# We'll then be able to loop through these and derive functional alignment transformations for each subject pair for all considered conditions.

# %%
def create_data(pair, condition):
    """
    Creates a single data dictionary for analysis.
    
    Parameters
    ----------
    pair : tuple
        A subject pair to functionally align
    condition : string
    
    Returns
    -------
    data : dict
        A dictionary with source_train, target_train,
        source_test, and target_test fields
    """
    data = {}
    data['source_train'] = df[(df.subject == pair[0]) & (df.acquisition == 'ap') &
                              (df.condition == condition)].path.values.item()
    data['target_train'] = df[(df.subject == pair[1]) & (df.acquisition == 'ap') &
                              (df.condition == condition)].path.values.item()
    data['source_test'] = df[(df.subject == pair[0]) & (df.acquisition == 'pa') &
                             (df.condition == condition)].path.values.item()
    data['target_test'] = df[(df.subject == pair[1]) & (df.acquisition == 'pa') &
                             (df.condition == condition)].path.values.item()
    return data



def create_data_dicts(pairs, condition_list):
    """
    Creates a list of data dictionaries for analysis.
    
    Parameters
    ----------
    pairs : list
        A list of tuples denoting individual subject pairs
    condition_list : list
        A list of strings denoting different experimental
        conditions
    
    Returns
    -------
    data_dicts : list
        A list of data dictionaries
    """
    data_dicts = []
    for p in pairs:
        for c in condition_list:
            data = create_data(p, c)
            data_dicts.append(data)
    return data_dicts


# %% [markdown]
# Following Bazeille and colleagues, we'll define a "reconstruction error" to assess the quality of our alignment; that is, the error of the functional alignment predicted signal in reconstructing or matching the target subject.
#
# It can be mathematically expressed as:
#
# $$
# {\eta}^2_*(Y, Y_i, X) = 1 - \dfrac{\Sigma^n_{i=1}(Y_i - R_iX)^2}{\Sigma^n_{i=1}Y^2_i}
# $$
#
# where $Y$ is the target data, $X$ is the source data, $R$ is the derived transformation matrix, and $*$ indicates the alignment method of interest such as `scaled_orthogonal` alignment.

# %%
def reconstruction_error(truth, pred):
    """
    Calculates the reconstruction error
    as defined by Bazeille and
    colleagues (2019).
    
    A perfect prediction yields a value of 1.
    
    Parameters
    ----------
    truth : str
        A file path to the true target subject
    pred : nib.Nifti1Image
        In-memory nifti-image of the target
        subject predicted by functional alignment
    """
    # load and reshape the data
    truth = nib.load(truth).get_fdata()
    pred = np.squeeze(pred.get_fdata())
    
    # calculate the reconstruction error
    num = np.sum((truth - pred)**2)
    den = np.sum(truth**2)
    return 1 - (num / den)


# %% [markdown]
# With this metric defined, we can calculate the reconstruction error for a given set of data, with a given functional alignment method and a defined parcellation.

# %%
from fmralign.pairwise_alignment import PairwiseAlignment

def calculate_method_error(data, method, clustering=schaefer):
    """
    Derive the reconstruction error for a given alignment method
    over the provided data set.
    
    Parameters
    ----------
    data : dict
        A dictionary with defined 'source_train',
        'target_train', 'source_test', and 'target_test'
        keys whose values should be file paths
    method : str
        A method for functional alignment. Valid
        methods are 'scaled_orthogonal', 'ridge_cv',
        'optimal_transport', and 'identity'
    clustering : nib.Nifti1Image 
        A defined parcellation. Default is the Schaefer
        multi-scale parcellation at 1000 region
        resolution.
    """
    alignment_estimator = PairwiseAlignment(alignment_method=method,
                                            clustering=clustering,
                                            standardize=True)
    alignment_estimator.fit(data["source_train"],
                            data["target_train"])
    target_pred = alignment_estimator.transform(data["source_test"])
    method_error = reconstruction_error(data["target_test"],
                                            target_pred)
    return method_error


# %% [markdown]
# To make comparisons across methods, we need to define an additional metric.
# Because considering the reconstruction error in isolation may not give us full insight into the increase in prediction gained by functional alignment, we may want to compare it against an `identity` alignment, where we predict that the target subject will exactly match the source subject.
# This is the "reconstruction ratio" defined by Bazeille and colleagues (2019):
#
# $$
# R_{{\eta}^2_*}(Y, R, X) = 1 - \dfrac{\Sigma^n_{i=1}(Y_i - R_iX)^2}{\Sigma^n_{i=1}(Y_i - X_i)^2} = 1 - \dfrac{1 - {\eta}^2_*(Y, R_i, X)}{1 - {\eta}^2_{id}(Y, Id, X)}
# $$
#
# Here, the ratio is greater than zero if voxels are predicted better by aligned data than by raw data.

# %%
def reconstruction_ratio(aligned_error, identity_error):
    """
    Calculates the reconstruction error
    as defined by Bazeille and
    colleagues (2019).
    
    A value greater than 0 indicates that
    voxels are predicted better by aligned data
    than by raw data.
    
    Parameters
    ----------
    aligned_error : float64
        The reconstruction error from a given
        functional alignment method
    identity error :  float64
        The reconstruction error from predicting
        the target subject as the source subject
    """
    num = 1 - aligned_error
    den = 1 - identity_error
    return 1 - (num / den)


# %% [markdown]
# Now, with everything defined, we're ready to run our replication!

# %%
def run_replication(pairs, condition_list):
    """
    Run a replication of Bazeille et al 2019.
    
    Parameters
    ----------
    pairs : list
        A list of tuples denoting individual subject pairs
    condition_list : list
        A list of strings denoting different experimental
        conditions
    
    Returns
    -------
    vals : list
        A list of derived reconstruction ratio values
    """
    data_dicts = create_data_dicts(pairs, condition_list)
    vals = []

    for d in data_dicts:
        orthogonal_error = calculate_method_error(d, 'scaled_orthogonal')
        identity_error = calculate_method_error(d, 'identity')
        vals.append(reconstruction_ratio(orthogonal_error, identity_error))
    return vals


# %%
# This is computationally intensive, and won't run on mybinder
vals = run_replication(pairs, condition_list)

# Instead, we can load a file containing the values
# these were generated by running the above code on my local machine
# orth_vals = np.loadtxt('./orthogonal_ibc_reconstruction_ratios.txt')

# %%
# %matplotlib inline
import seaborn as sns
sns.set(style="ticks")

ax = sns.violinplot(vals, palette="Paired")
ax.set_xlim(-1, 1)
ax.axvline(0, color="black");

# %% [markdown]
# In this notebook, we'd like to replicate part of _Figure 4a_ (reproduced below).
# Specifically, we'd like to replicate the range of reconstruction errors seen for each alignment method.
# In order to be sure that we're defining everything correctly, we'll first start with the `scaled orthogonal` alignment since this is computationally efficient.
#
# <img src='./Bazeille_2019_fig4a.png' width='500'>

# %% [markdown]
# The derived values do not match those seen by Bazeille and coauthors.
# Notably, although we have a similar central tendency, we have no negative reconstruction ratio values.

# %%

# %%

# %%
