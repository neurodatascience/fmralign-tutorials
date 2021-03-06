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

# Generalized Procrustes analysis

The apocraphyl legend of Procrustes describes an inn-keeper who--having only one bed in the inn--gruesomely stretched or shortened his customers to fit it.

Procrustes analysis allows us to compares the geometry of two objects or data sets. Specifically, for two geometries with a known one-to-one mapping, we can consider the distance between each pair of corresponding points. Our goal is to derive an orthogonal transformation that minimizes the distance between each pair of points, thus minimizing the total distance between the two geometries. Named for the legend of Procrustes, the ancient Greek innkeeper who stretched or cut off traveller's limbs so they would fit his bed, Procrustes analysis can be seen as conforming datasets through a series of rigid-body transformations {cite}Schonemann1966-qq.

Generalized Procrustes analysis differs from Procrustes analysis in two significant ways.
First, generalized Procrustes includes both the orthogonal transformations of Procrustes (i.e., rotations and reflections),
as well as additional scaling and translation transformations.
Second, generalized Procrustes can be applied to more than two shapes through the iterative use of a reference shape.

We can formally express the generalized Procrustes problem as:

```{math}
:label: general_procrustes_eq_1
\min_{\mathbf{R}= s\mathbf{M}} ||\mathbf{R} \mathbf{X} - \mathbf{Y}||_F^2 \\
s\in\mathbb{R^+}, \enspace \mathbf{M} \in \mathbb{R}^{p \times p} \text{ s.t. } \mathbf{M}^\intercal\mathbf{M} = \mathbf{I}_p
```