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

# Optimal Transport

## Formalism

```{math}
:label: ot_eq_1
\mathbf{C}_{i, j}(\mathbf{X}, \mathbf{Y}) = ||\mathbf{X}_i - \mathbf{Y}_j|| \\
```

To allow for a more efficient estimation, we slightly relax this constraint with an additional entropic smoothing term. We can then find $\mathbf{R}$, the regularized Optimal Transport plan by finding a minimum through the Sinkhorn algorithm.

```{math}
:label: ot_eq_2
    \min_{\substack{\mathbf{R} \in \mathbb{R_+}^{p\times p}; \\ \mathbf{R} \mathbf{1} = 1/p, \mathbf{1} \mathbf{R}^\top = 1/p}}\mathrm{Tr}({\mathbf{R}\cdot\mathbf{C})}  - \epsilon  \mathbf{H}(\mathbf{R})
```

where $\epsilon > 0$, and  the discrete entropy of the transformation $\mathbf{H}(\mathbf{R})$ is defined as:

```{math}
:label: ot_eq_3
\mathbf{H}(\mathbf{R}) \overset{\mathrm{def.}}{=} - \sum_{i,j} \mathbf{R}_{i,j}(\log(\mathbf{R}_{i, j}) - 1)
```

This method differs from Procrustes analysis in that it yields a sparser mapping between source and target voxels with high functional similarity, making it less sensitive to noisy voxels on both ends. The level of sparsity is controlled by the user-supplied hyper-parameter $\epsilon$.

## Implementation

Efficient implementations in Python are available through the `POT` and `OTT` packages.

```{code-cell} python3
import POT
```

## Other useful resources

* [Leyla Tarhan's blogpost series on Wasserstein distance](http://lytarhan.rbind.io/categories/wasserstein-distance/)
* [Broad Institute summary of applied Optimal Transport](https://www.youtube.com/watch?v=aio1lAE-h_I)