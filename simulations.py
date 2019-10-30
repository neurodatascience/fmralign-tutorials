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
# ## Simulating functional alignment performance
#
# In this notebook, we'd like to simulate functional alignment in small regions of interest (ROIs) across cortex. 
# To do so, we'll generate a matrix with highly correlated "intrinsic" activity.
# This corresponds to our assumption that -- as independent functional areas -- ROIs should have relatively similar activity patterns within their voxels.
#
# On top of this "intrinsic" activity, we'll add a sparse pattern of activation which we can consider to be "stimulus bound."
# The sparsity of this pattern can be smoothly varied (controlled with the `density` parameter).
# As an initial guess, we'll create a pattern with 25% sparsity.
# From initial testing with Procrustes alignment, the sparsity of the pattern does not appear to impact the accuracy of resulting alignment.
#
# To mimic the hemodynamic spread, we also add a small Gaussian blur on top of the generated matrix.
# The size of this blur can be smoothly varied with the `sigma` parameter.
# As an initial guess, we can set the blur to 1 sigma.
#
# Within the same ROI, each participant's uniform distribution is conserved.
# We generate a new "stimulus bound" sparse pattern which is shared across participants.
# We can then apply the generate transformation from the previous sparse pattern and perform a "voxelwise correlation" of the transformed ROIs.
#
# # Some initial findings
# From initial testing with Procrustes alignment, the size of the blur impacts the accuracy of resulting alignment in an inverted-U relationship.
# The "ideal" amount of smoothing for Procrustes alignment is approximately 10 sigma, with 25% sparsity.

# %%
# %matplotlib inline
import matplotlib.pyplot as plt

def draw_heatmap(img):
    plt.imshow(img, cmap='viridis', interpolation='nearest')
    plt.show()


# %%
# let's use scaled_procrustes from fmralign for easier comparisons
from fmralign.alignment_methods import scaled_procrustes

# %% [markdown]
# First, we'll sample from a uniform distribution to stimulate an ROI.
# We're choosing to sample from a uniform distribution in that a well-defined ROI should have relatively homogenous functional responses.

# %%
import numpy as np
from scipy.stats import uniform

rv = uniform.rvs(size=np.array([10, 10]))
draw_heatmap(rv)

# %% [markdown]
# Next, we'll generate a stimulus-bound response.
# This should be sparse within the ROI and reflect the unique "tuning" of each voxel to a presented stimulus.
# This response is expected to be differently encoded across stimuli and across participants.
# Importantly for the purposes of this simulation, however, the _geometry_ of this response should be conserved across participants.

# %%
from scipy import sparse

p = sparse.random(10, 10, density=0.25)
draw_heatmap(p.A)

# %% [markdown]
# We can shift this pattern a bit, to mimic functional variability in the structure of these representations across participants.

# %%
draw_heatmap(np.roll(p.A, shift=2))  # we could also try np.rot90

# %% [markdown]
# Now we can add the shared response and stimulus-bound response together to get an idealized response within the ROI to some particular stimulus.

# %%
resp = rv + p.A
draw_heatmap(resp)

# %% [markdown]
# We'll then blur it slightly with a small gaussian filter to account for the hemodynamic spread.

# %%
from scipy.ndimage import filters

smooth_resp = filters.gaussian_filter(resp, sigma=1)
draw_heatmap(smooth_resp)

# %% [markdown]
# We now need multiple subjects to align.
# Following this formula, each subject should get a new uniform distribution, but they should share the stimulus-bound response (though the response may be rotated, re-scaled, or inverted).
# For simplicity, in this first pass we'll give all subjects exactly the same stimulus-bound response and the same amount of smoothing.

# %%
rvs1 = uniform.rvs(size=np.array([10, 10]))
mtx1 = rvs1 + p.A
mtx1 = filters.gaussian_filter(mtx1, sigma=1)

rvs2 = uniform.rvs(size=np.array([10, 10]))
mtx2 = rvs2 + np.roll(p.A, shift=2)
mtx2 = filters.gaussian_filter(mtx2, sigma=1)

# %%
f, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
ax1.set_title('Original responses for two example "subjects"', loc='left', pad=12)

ax1.imshow(mtx1, cmap='viridis', interpolation='nearest');
ax2.imshow(mtx2, cmap='viridis', interpolation='nearest');

# %%
R, sc = scaled_procrustes(mtx1, mtx2)
f, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
ax1.set_title('Procrustes-aligned responses for two example "subjects"', loc='left', pad=12)

ax1.imshow(R @ mtx1, cmap='viridis', interpolation='nearest');
ax2.imshow(mtx2, cmap='viridis', interpolation='nearest');

# %% [markdown]
# What if we want to assess the success of this alignment?
# A naive method might be to take the voxelwise correlation of the aligned patterns:

# %%
# Since this comes bundled with Procrustes, let's also try a voxelwise correlation:
corr_mat = np.corrcoef(R @ mtx1, mtx2)
draw_heatmap(corr_mat)

# %% [markdown]
# The difficulty is that we have no "ground truth" in this scenario;
# that is, we're only comparing patterns after we have already influenced them by performing an alignment.
# It would be better instead to calculate the voxelwise correlation using the alignment parameters from a separate "train" run.
#
# To do this, let's revisit how we're generating our patterns.

# %%
p1 = sparse.random(10, 10, density=0.25)
p2 = sparse.random(10, 10, density=0.25)
rvs1 = uniform.rvs(size=np.array([10, 10]))
rvs2 = uniform.rvs(size=np.array([10, 10]))

def generate_train_test(dis1, dis2, pattern, sigma=2):
    # generate first distribution
    dis1 = dis1 + pattern.A
    dis1 = filters.gaussian_filter(dis1, sigma=sigma)
    # generate second distribution
    dis2 = dis2 + np.roll(pattern.A, shift=2)
    dis2 = filters.gaussian_filter(dis2, sigma=sigma)
    
    return dis1, dis2

train1, train2 = generate_train_test(rvs1, rvs2, p1)
test1, test2   = generate_train_test(rvs1, rvs2, p2)

# %% [markdown]
# Here, each subject has a unique uniform distribution and a shared sparse pattern, although this pattern is shifted slightly across subjects.
# Thus, this is roughly equivalent to two subjects engaged in two unique conditions (e.g., watching two different movie clips).

# %%
f, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
ax1.set_title('Original responses for an example "subject" in two conditions', loc='left', pad=12)

ax1.imshow(train1, cmap='viridis', interpolation='nearest');
ax2.imshow(train2, cmap='viridis', interpolation='nearest');

# %%
R, sc = scaled_procrustes(train1, train2)
f, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
ax1.set_title('Aligned responses for an example "subject" in two conditions', loc='left', pad=12)

ax1.imshow(R @ train1, cmap='viridis', interpolation='nearest');
ax2.imshow(train2, cmap='viridis', interpolation='nearest');

# %% [markdown]
# We expect that if we generate an alignment from subject 1 to subject 2 in the first condition, we could use this transformation matrix to generate an "expected" alignment from subject 1 to subject 2 in the second condition.
# We'll first visualize the voxelwise correlation of this approach:

# %%
R, sc = scaled_procrustes(train1, train2)
pred_test2 = R @ test1

corr_mat = np.corrcoef(pred_test2, test2)
draw_heatmap(corr_mat)


# %% [markdown]
# It would also be helpful to be able to assign metrics to this prediction or "reconstruction."
# We'll use the normalized reconstruction error defined by Bazeille and colleagues (2019):
#
# $$
# {\eta}^2_*(Y, Y_i, X) = 1 - \dfrac{\Sigma^n_{i=1}(Y_i - R_iX)^2}{\Sigma^n_{i=1}Y^2_i}
# $$
#
# where $*$ indicates the alignment method of interest; in this case, `scaled_orthogonal` alignment.

# %%
def reconstruction_error(Y, R, X):
    """
    Calculates the reconstruction error
    as defined by Bazeille and
    colleagues (2019).
    
    Where R @ X is the prediction and
    Y is the ground truth.
    
    A perfect prediction yields a value of 1.
    """
    num = np.sum((Y - R @ X)**2)
    den = np.sum(Y**2)
    return 1 - (num / den)

reconstruction_error(test2, R, test1)


# %% [markdown]
# Considering this metric in isolation may not give us full insight into the increase in prediction gained by functional alignment.
# Instead, we can use the "reconstruction ratio" defined by Bazeille and colleagues (2019):
#
# $$
# R_{{\eta}^2_*}(Y, R, X) = 1 - \dfrac{\Sigma^n_{i=1}(Y_i - R_iX)^2}{\Sigma^n_{i=1}(Y_i - X_i)^2} = 1 - \dfrac{1 - {\eta}^2_*(Y, R_i, X)}{1 - {\eta}^2_{id}(Y, Id, X)}
# $$
#
# Here, the ratio is greater than zero if voxels are predicted better by aligned data than by raw data.

# %%
def reconstruction_ratio(Y, R, X):
    num = 1 - reconstruction_error(Y, R, X)
    den = 1 - reconstruction_error(Y, np.eye(10), X)  # since we've defined X and Y to be 10,10
    return 1 - (num / den)

reconstruction_ratio(test2, R, test1)


# %% [markdown]
# This is only one comparison.
# To get a better idea of our performance, we can run this many times to simulate a noise ceiling;
# that is, the best performance we can expect to achieve if our true patterns are exactly the same. 

# %%
def simulate_alignment(size=np.array([10, 10]), density=0.25):
    p1 = sparse.random(10, 10, density=density)
    p2 = sparse.random(10, 10, density=density)
    rvs1 = uniform.rvs(size=size)
    rvs2 = uniform.rvs(size=size)

    train1, train2 = generate_train_test(rvs1, rvs2, p1)
    test1, test2   = generate_train_test(rvs1, rvs2, p2)
    R, sc = scaled_procrustes(train1, train2)
    return reconstruction_ratio(test2, R, test1)

vals = []
for i in range(10000):
    vals.append(simulate_alignment())

# %%
import seaborn as sns
sns.set(style="whitegrid")

ax = sns.violinplot(x=vals)


# %% [markdown]
# ---

# %%
# HaxbyLab reports in their 2011 paper that a FWHM of 4 achieved optimal predictive performance
# Matthew Brett gives a formula in https://matthew-brett.github.io/teaching/smoothing_intro.html
# to convert between the FWHM of a Gaussian kernel and sigma.

def fwhm2sigma(fwhm):
    return fwhm / np.sqrt(8 * np.log(2))

fwhm2sigma(4)