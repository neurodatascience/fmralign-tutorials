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

Manhattan or taxicab distance.
L1 norm.

## Formalism

You say "I can break $s(t)$ into different parts, or features\". This transforms $s(t)$ into some other representation that we'll call $x(t)$. Let's say that the number of features in $x(t)$ is $p$.

You say "I can predict $y(t)$ from a weighted combination of the features in $x(t)$". This means you are imagining a model that looks something like this,

```{math}
:label: ridge_eq_1
y(t) = \sum_{i=1}^p x_i(t) \beta_i + \epsilon(t)
```

where:

* $x_i(t)$ refers to the $i$th feature in $x(t)$
* $\beta_i$ refers to the weight on that feature (we don't know what this weight is yet), and
* $\epsilon(t)$ refers to the noise, i.e. any part of $y(t)$ that you can't predict from $x(t)$ (we don't know what this is yet either)

Since this model is just a weighted sum, we can write it more simply using a little linear algebra:

```{math}
:label: ridge_eq_2
y(t) = x(t) \beta + \epsilon(t)
```

where $x(t)$ is now a $1 \times p$ vector of feature values and $\beta$ is a $p \times 1$ vector of weights.
To deal with these equations more easily, we'll need to stack the values of $y(t)$ and $x(t)$ into matrices. Let's define those matrices like this:

```{math}
Y = \begin{bmatrix} y(t=1) \\\\ y(t=2) \\\\ \vdots \\\\ y(t=T) \end{bmatrix},
X = \begin{bmatrix} x(t=1) \\\\ x(t=2) \\\\ \vdots \\\\ x(t=T) \end{bmatrix}
```

So we now have $Y$, which is a $T \times 1$ matrix of brain responses, and $X$, which is a $T \times p$ matrix of features that we extracted from the stimuli. If we also define $\epsilon$ as a vector of the same size as $Y$, then we can re-write the model like this:

```{math}
:label: ridge_eq_3
Y = X \beta + \epsilon
```

Remember when we talked about the noise term, $\epsilon(t)$? We said it was any part of $y(t)$ that couldn't be predicted from $x(t)$. We can write this mathematically as the difference between $y(t)$ and the predicted value based on $x(t)$ and our estimated weights (this comes from re-arranging the equation above:

```{math}
:label: ridge_eq_4
\epsilon(t) = y(t) - x(t) \beta_{OLS}
```

Huh. When we write it this way, it looks a lot like the loss function $\mathcal{L}(\beta)$, doesn't it? In fact, the loss function is exactly the sum of the squared errors. This means our OLS regression model made the assumption that _$\epsilon(t)$ is as small as possible_, because we selected $\beta_{OLS}$ to minimize the size of the loss.

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

The first term on the right hand side of this equation is the same squared error loss that we used before for OLS. The second term is the sum of the squares of all the weights in $\beta$, multiplied by a scalar variable $\lambda$ that we will call the **ridge coefficient**

The ridge coefficient $\lambda$ determines the _strength_ of the regularization that's applied in ridge regression:

* If you give $\lambda$ a large value, then the penalty term will be big relative to the loss, and the resulting weights will be very small. (In the limit of very large $\lambda$ you will force the weights to be almost exactly zero!)
* If you give $\lambda$ a small value, then the penalty term will be small relative to the loss, and the resulting weights will not be too different from the OLS weights. (In the limit of $\lambda \rightarrow 0$, the penalty term will be zero and you'll get back exactly the OLS solution!)

To get the ridge regression weights, $\beta_{ridge}$, you minimize the ridge loss function. We don't need to go through the full derivation of the solution (though it's pretty fun, and easy to do based on the matrix calculus we did for the OLS solution!), so let's just take a look at the answer:

```{math}
:label: ridge_eq_7
\beta_{ridge} = (X^\top X + \lambda I)^{-1} X^\top Y
```

Compute $R$ s.t. $|| XR - Y ||^2 + alpha ||R||^2$ is minimized with CV.

```{math}
:label: ridge_eq_8
||y - Xw||^2_2 + alpha * ||w||^2_2
```

## Implementation

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
* [L1 vs L2 norms](https://www.kaggle.com/residentmario/l1-norms-versus-l2-norms)
