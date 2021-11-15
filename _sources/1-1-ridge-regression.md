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
In previous work {cite:ts}`tavor2016task`, we've seen this method used to predict one task condition (such as a working memory task) from another (such as resting-state) within the same participant.

Here, we don't expect that every voxel will provide equal information across the two tasks.
Instead, we'd like to learn more from informative voxels than from non-informative voxels.
We can do so by predicting $Y$ as a _weighted combination_ of information from $X$.
The corresponding model would look something like this,

```{math}
:label: ridge_eq_1
Y = X \beta + \epsilon
```

where

* $\beta$ refers to a matrix of weights, one for each voxel (we don't know what the weights are yet), and
* $\epsilon$ refers to the noise, i.e. any part of $Y$ that you can't predict from $X$ (we don't know what this is yet either).
  $\epsilon$ as a matrix of the same size as $Y$

## Learning the $\beta$ weights

Going forward, we're going to refer to this regression procedure as ordinary least squares or OLS, and the solution that we derived as "the OLS solution" or $\beta_{OLS}$.

We can write $\epsilon$ mathematically as the difference between $Y$ and the predicted value based on $X$ and our estimated $\beta$ weights:

```{math}
:label: ridge_eq_2
\epsilon = Y - X \beta_{OLS}
```

Huh. When we write it this way, it looks a lot like the loss function $\mathcal{L}(\beta)$, doesn't it? In fact, the loss function is exactly the sum of the squared errors. This means our OLS regression model made the assumption that _$\epsilon(t)$ is as small as possible_, because we selected $\beta_{OLS}$ to minimize the size of the loss.

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
