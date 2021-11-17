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

# Ridge Regression

Let's say that you'd like to predict one distribution _Y_ from the other distribution _X_.
In previous work such as {cite:ts}`tavor2016task`, we've seen this method used to predict one task condition (such as a working memory task) from another (such as resting-state) within the same participant.

We can do so by predicting $Y$ as a _weighted combination_ of information from $X$.
The corresponding model would look something like this,

```{math}
:label: ridge_eq_1
Y = X \beta + \epsilon
```

where we have two unknowns:

* $\beta$ refers to a matrix of weights, one for each voxel, and
* $\epsilon$ refers to a matrix of noise, i.e. any part of $Y$ that you can't predict from $X$.

## Learning the $\beta$ weights

Our goal is to learn the $\beta$ weights that minimize our "noise" or error values, $\epsilon$.
Ordinary Least Squares (OLS) is an ideal approach to solving this regression in that it provides the Best Linear Unbiased Estimator (BLUE).
A nice introduction to OLS is available from [Mumford Brain Stats](https://mumfordbrainstats.tumblr.com/post/124743714561/day-2-simple-linear-regression).

Unfortunately, using OLS regression tends to overfit to a given data sample, meaning that our learned $\beta$ values will not generalize well to new data.
This is important, as we do not want to learn mappings between only two sets of samples (i.e. one run each of resting-state and task).
Instead, we want to learn mappings that _generalize_ to new samples collected under the same conditions.
We therefore need to reduce how much we're overfitting to our training samples.

To do so, we can modify the learnt $\beta$ weights using a set rule.
Although many different rules are possible, here we'll use "ridge," from which ridge regression gets its name.
This is also known as an L2 penalty.

## Improving performance with an L2 penalty

The simplest way to describe ridge regression mathematically is including a **penalty** on the size of the weights in the loss function. Specifically, ridge regression penalizes the sum of the squared weights, leading to a new and improved loss function that we'll call $\mathcal{L}_{ridge}(\beta)$:

```{math}
:label: ridge_eq_5
\mathcal{L}_{ridge}(\beta) = \sum_{t=1}^T (y(t) - x(t) \beta)^2 + \lambda \sum_{i=1}^p \beta_i^2
```

or, in fancy linear algebra terms:

```{math}
:label: ridge_eq_6
\mathcal{L}_{ridge}(\beta) = (Y - X\beta)^\top (Y - X \beta) + \lambda \beta^\top \beta
```

The first term on the right hand side of this equation is the same squared error loss that we used before for OLS.
The second term is the sum of the squares of all the weights in $\beta$, multiplied by a scalar variable $\lambda$ that we will call the **ridge coefficient**

The ridge coefficient $\lambda$ determines the _strength_ of the regularization that's applied in ridge regression:

* If you give $\lambda$ a large value, then the penalty term will be big relative to the loss, and the resulting weights will be very small. (In the limit of very large $\lambda$ you will force the weights to be almost exactly zero!)
* If you give $\lambda$ a small value, then the penalty term will be small relative to the loss, and the resulting weights will not be too different from the OLS weights. (In the limit of $\lambda \rightarrow 0$, the penalty term will be zero and you'll get back exactly the OLS solution!)

To get the ridge regression weights, $\beta_{ridge}$, you minimize the ridge loss function.
We don't need to go through the full derivation of the solution (though it's pretty fun, and easy to do based on the matrix calculus we did for the OLS solution!), so let's just take a look at the answer:

```{math}
:label: ridge_eq_7
\beta_{ridge} = (X^\top X + \lambda I)^{-1} X^\top Y
```

Compute $R$ s.t. $|| XR - Y ||^2 + alpha ||R||^2$ is minimized with CV.

```{math}
:label: ridge_eq_8
||y - Xw||^2_2 + alpha * ||w||^2_2
```

## Implementing directly in nilearn

There's an [example in the Nilearn gallery](https://nilearn.github.io/auto_examples/02_decoding/plot_miyawaki_encoding.html) that uses ridge regression to predict fMRI activity from visual stimuli.

We can lightly adapt this example to predict fMRI activity in one condition from another condition.

```{code} python3
from sklearn.linear_model import RidgeCV

R = RidgeCV(alphas=self.alphas, fit_intercept=True,
            normalize=False,
            scoring=sklearn.metrics.SCORERS['r2'],
            cv=self.cv)
R.fit(X, Y)
```

## Other useful resources

* [Alexander Huth tutorial on ridge regression with word embeddings](https://github.com/neurohackademy/nh2020-curriculum/tree/master/we-word-embeddings-huth)
* [9 Distance Measures in Data Science](https://towardsdatascience.com/9-distance-measures-in-data-science-918109d069fa)

## References

```{bibliography}
:style: unsrt
:filter: docname in docnames
```
