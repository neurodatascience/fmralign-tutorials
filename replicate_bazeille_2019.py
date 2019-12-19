# -*- coding: utf-8 -*-
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
# First, we'll need to define region(s) of the brain over which to perform functional alignment.
# Luckily, the IBC data set comes with a pre-computed gray matter mask.

# %%
import itertools
import numpy as np
import nibabel as nib
from nilearn import datasets, input_data
from fmralign.fetch_example_data import fetch_ibc_subjects_contrasts

files, df, mask = fetch_ibc_subjects_contrasts(subjects="all")
masker = input_data.NiftiMasker(mask_img=mask)

# we'll do an empty fit just so we can see what the mask looks like
masker.fit()
masker.generate_report()

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
def create_data_dicts(pairs):
    """
    Creates a single data dictionary for analysis.
    
    Parameters
    ----------
    pairs : list
        A list of tuples denoting individual subject pairs to
        functionally align.
    
    Returns
    -------
    data_dicts : list
        A list of dictionaries, each with defined source_train,
        target_train, source_test, and target_test fields.
    """
    data_dicts = []
    for p in pairs:
        data = {}
        data["source_train"] = df[(df.subject == p[0]) &
                                  (df.acquisition == 'ap')].path.values
        data["target_train"] = df[(df.subject == p[1]) &
                                  (df.acquisition == 'ap')].path.values
        data["source_test"] = df[(df.subject == p[0]) &
                                 (df.acquisition == 'pa')].path.values
        data["target_test"] = df[(df.subject == p[1]) &
                                 (df.acquisition == 'pa')].path.values
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
from scipy.stats import pearsonr
from sklearn.metrics import r2_score


def score_table(loss, X_gt, X_pred, multioutput='raw_values'):
    """
    
    Parameters
    ----------
    loss : str in ['R2', 'corr', 'n_reconstruction_err']
        The loss function used in scoring. Default is normalized
        reconstruction error.
        'R2' :
            The R2 distance between source and target arrays.
        'corr' :
            The correlation between source and target arrays.
        'n_reconstruction_err' :
            The normalized reconstruction error.
    X_gt : arr
        The ground truth array.
    X_pred : arr
        The predicted array
    multioutput: str in [‘raw_values’, ‘uniform_average’]
        Defines aggregating of multiple output scores. Default is raw values.
        ‘raw_values’ :
            Returns a full set of scores in case of multioutput input.
        ‘uniform_average’ :
            Scores of all outputs are averaged with uniform weight.

    Returns
    -------
    score : float or ndarray of floats
        The score or ndarray of scores if ‘multioutput’ is ‘raw_values’.
    """
    if loss is "R2":
        score = r2_score(X_gt, X_pred, multioutput=multioutput)
    elif loss is "n_reconstruction_err":
        score = normalized_reconstruction_error(
            X_gt, X_pred, multioutput=multioutput)
    elif loss is "corr":
        score = np.array([pearsonr(X_gt[:, vox], X_pred[:, vox])[0]  #pearsonr returns both rho and p
                          for vox in range(X_pred.shape[1])])
    else:
        raise NameError(
            "Unknown loss. Recognized values are 'R2', 'corr', or 'reconstruction_err'")
    # if the calculated score is less than -1, return -1
    return np.maximum(score, -1)


def normalized_reconstruction_error(y_true, y_pred, multioutput='raw_values'):
    """
    Calculates the normalized reconstruction error
    as defined by Bazeille and colleagues (2019).
    
    A perfect prediction yields a value of 1.
    
    Parameters
    ----------
    y_true : arr
        The ground truth array.
    y_pred : arr
        The predicted array.
    multioutput: str in [‘raw_values’, ‘uniform_average’]
    Defines aggregating of multiple output scores. Default is raw values.
    ‘raw_values’ :
        Returns a full set of scores in case of multioutput input.
    ‘uniform_average’ :
        Scores of all outputs are averaged with uniform weight.
    
    Returns
    -------
    score : float or ndarray of floats
        The score or ndarray of scores if ‘multioutput’ is ‘raw_values’.
    """
    if y_true.ndim == 1:
        y_true = y_true.reshape((-1, 1))

    if y_pred.ndim == 1:
        y_pred = y_pred.reshape((-1, 1))

    numerator = ((y_true - y_pred) ** 2).sum(axis=0, dtype=np.float64)
    denominator = ((y_true) ** 2).sum(axis=0, dtype=np.float64)
    
    # Include only non-zero values
    nonzero_denominator = (denominator != 0)
    nonzero_numerator = (numerator != 0)
    valid_score = (nonzero_denominator & nonzero_numerator)
    
    # Calculate reconstruction error
    output_scores = np.ones([y_true.shape[1]])
    output_scores[valid_score] = 1 - (numerator[valid_score] /
                                      denominator[valid_score])
    if multioutput == 'raw_values':
        # return scores individually
        return output_scores
    elif multioutput == 'uniform_average':
        # passing None as weights yields uniform average
        return np.average(output_scores, weights=None)


# %% [markdown]
# With this metric defined, we can calculate the reconstruction error for a given set of data, with a given functional alignment method and a defined parcellation.

# %%
from fmralign.pairwise_alignment import PairwiseAlignment


def calculate_pairwise_error(data, method, masker,
                             clustering='hierarchical_kmeans',
                             n_pieces=200, n_jobs=5):
    """
    Derive the reconstruction error and ratio for a given alignment method
    over the provided data set.
    
    Parameters
    ----------
    data : dict
        A dictionary with defined 'source_train',
        'target_train', 'source_test', and 'target_test'
        keys whose values should be file paths
    method : str in ['scaled_orthogonal', 'ridge_cv',
                     'optimal_transport', 'identity']
        A method for functional alignment.
    masker : instance of NiftiMasker or MultiNiftiMasker
        Masker to be used on the data. For more information see:
        http://nilearn.github.io/manipulating_images/masker_objects.html
    clustering : str or 3D Niimg-like object
        Method used to perform parcellation of data.
        Supported methods are ['hierarchical_kmeans', 'kmeans', 'rena', 'ward']
        If 3D Niimg, image used as predefined clustering.
        Default is 'hierarchical_kmeans'.
    n_pieces : int
        Number of regions in which the data is parcellated for alignment.
        Default is 200.
    n_jobs : int
        The number of CPUs to use to do the computation. -1 means
        'all CPUs'.
    """
    if method is 'identity':  # no need to calculate alignment; base off input data
        method_error = score_table(loss='n_reconstruction_err',
                                   X_gt=masker.transform(data["target_test"]),
                                   X_pred=masker.transform(data["source_test"]))
    else:
        alignment_estimator = PairwiseAlignment(alignment_method=method,
                                                n_pieces=n_pieces, mask=masker,
                                                n_jobs=n_jobs)
        alignment_estimator.fit(data["source_train"],
                                data["target_train"])
        target_pred = alignment_estimator.transform(data["source_test"])
        method_error = score_table(loss='n_reconstruction_err',
                                         X_gt=masker.transform(data["target_test"]),
                                         X_pred=masker.transform(target_pred))
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
def calculate_group_error(pairs, methods, clustering='hierarchical_kmeans'):
    """
    
    Parameters
    ----------
    pairs : list
        A list of tuples denoting individual subject pairs
    methods : list
        A list of strings for functiona alignment. Supported
        methods are ['scaled_orthogonal', 'ridge_cv',
        'optimal_transport', 'identity']
    clustering : str or 3D Niimg-like object
        Method used to perform parcellation of data.
        Supported methods are ['hierarchical_kmeans', 'kmeans', 'rena', 'ward']
        If 3D Niimg, image used as predefined clustering.
        Default is 'hierarchical_kmeans'.
    
    Returns
    -------
    errors : dictionary
        A dictionary of derived reconstruction error values
        for each method
    """
    data_dicts = create_data_dicts(pairs)
    errors = {}

    for method in methods:
        method_error = []
        for d in data_dicts:
            method_error.append(calculate_pairwise_error(d, method, masker, clustering=clustering, n_jobs=2))
        errors["{}_reconstruction_error".format(method)] = method_error
    return errors


# %%
methods = ['scaled_orthogonal', 'ridge_cv', 'optimal_transport', 'identity']
reconstruction_errors = calculate_group_error(pairs, methods=methods, clustering='kmeans')

reconstruction_ratios = []
identity_errors = reconstruction_errors.pop('identity_reconstruction_error')
identity_errors = np.asarray(identity_errors).flatten()
for keys, vals in reconstruction_errors.items():
    method_errors = np.asarray(vals).flatten()
    method_ratios = reconstruction_ratio(method_errors, identity_errors)
    reconstruction_ratios.append(method_ratios)

# %%
# %matplotlib inline
import matplotlib.pyplot as plt

methods.remove('identity')

plt.figure(figsize=(5, 5))
plt.violinplot(reconstruction_ratios, vert=False, showextrema=False,
               showmeans=False, showmedians=True, points=800, widths=0.8)
plt.tick_params(axis='y', labelsize=20)
plt.xlim(left=-1, right=1)
plt.xlabel(r'$R_{\eta^2}$', fontsize=24, rotation="horizontal")
plt.axvline(x=0, color='dimgrey')
plt.tight_layout()
plt.yticks(range(1, len(methods) + 1), methods);

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
