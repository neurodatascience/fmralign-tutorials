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

# Shared Response Model

Shared Response Modelling (SRM) is a _latent factor model_.
This means that--rather than searching for direct correspondences across subjects--an initial dimensionality reduction is
used to identify latent factors that support the observed measreuments and are shared across subjects.
The deterministic SRM model assumes Gaussian noise with the same variance for all subjects and orthonormal spatial components.

## Formalism

```{math}
:label: srm_eq_1
\forall_i \in {1 ... n}, X_i[τ] ~ N(S[τ]W_i, σ^2 I_v) \\
\mathbf{W}_i\mathbf{W}^\intercal_i = \mathbf{I}_k
```

Maximizing the log-likelihood we obtain the following optimization problem:

```{math}
:label: srm_eq_2
\min{W_1, ... ,W_n, S} \Sigma{i=1}^n ||Xi − SW_i||_2 \\
\text{such that} \forall_i \in {1, ..., n}
\mathbf{W}_i\mathbf{W}^\intercal_i = \mathbf{I}_k
```

This can be solved efficiently using alternate minimization on $(W1, ..., Wn)$
and $S$.
At each iteration we have two problems to solve that have a closed form
solution:

```{math}
:label: srm_eq_3
\forall_i \in {1, ..., n},
\arg\min_{\mathbf{W}}\Sigma_{j=1}^n ||X_j − SW_j||^2 = U_iV_i \\
\text{where} Ui, Di, Vi = SVD(S^\intercal X_i) \\
\text{such that} \mathbf{W}_i\mathbf{W}^\intercal_i = \mathbf{I}_k
```

```{math}
:label: srm_eq_4
\arg\min_{\mathbf{S}}\Sigma_{i=1}^n ||X_i − SW_i||^2 = 1 / n \Sigma_{i=1}^n X_i W_i^\intercal
```

## Implementation

Accessible implementations are available in `brainiak.funcalign.srm.DetSRM`,
with an optimized implementation in `brainiak.funcalign.fastsrm.FastSRM`.

```{code-cell} python3
```