# Minimal Covariant Boost Test

## Purpose

This experiment tests the new fully covariant baby-Skyrme Hamiltonian solver under Lorentz-initialized boosts.

Compared to the previous partially covariant solver, this experiment evolves canonical variables:

```text
(s, pi)
```

and recovers velocity via:

```text
p = A(s)^-1 pi
```

The boost initialization is:

```text
s_v(x,y) = s0(gamma x, y)
p_v(x,y) = -gamma v ∂x s0(gamma x, y)
pi_v = A(s_v) p_v
```

## Diagnostics

The test measures:

- total covariant Hamiltonian energy `E`,
- Noether momentum `P_x = -∫ pi · s_x dxdy`,
- invariant proxy `M² = E² - P_x² - P_y²`,
- topological charge `Q`,
- width contraction proxy `sigma_x/sigma_x0`,
- constraints `|s|=1`, `pi·s=0`, and `p·s=0`.

## Main Result

At `v=0.4`, the invariant proxy improves compared with earlier partially covariant diagnostics:

```text
M²/M0² ≈ 0.9938
```

Earlier tests were around `0.987–0.989` for comparable boost levels.

The width contraction proxy also remains qualitatively consistent:

```text
v=0.2: sigma_x/sigma_x0 ≈ 0.9899, expected 1/gamma ≈ 0.9798
v=0.4: sigma_x/sigma_x0 ≈ 0.9569, expected 1/gamma ≈ 0.9165
```

Energy scaling is still too weak compared with ideal gamma scaling:

```text
v=0.4: E/E0 ≈ 1.0383, gamma ≈ 1.0911
```

## Interpretation

The fully covariant solver improves Lorentz consistency, especially the invariant proxy `E²-P²`. This supports the hypothesis that the previous Lorentz mismatch was partly caused by missing time-space Skyrme terms and the incorrect use of velocity rather than canonical momentum.

However, this is still not a full Lorentz proof. The remaining gap is likely due to:

1. very low resolution,
2. hard fixed circular boundary,
3. non-relaxed initial soliton profile,
4. simple projected integrator,
5. finite-difference lattice artifacts.

## Next Steps

1. Run the same test at higher resolution.
2. Use a relaxed rest soliton as the boost source.
3. Increase the domain and boundary margin.
4. Improve the constrained symplectic integrator.
5. Repeat energy-momentum scaling tests.
