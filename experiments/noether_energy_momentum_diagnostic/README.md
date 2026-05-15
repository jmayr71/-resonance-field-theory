# Noether Energy-Momentum Diagnostic

## Purpose

This experiment addresses A5 in the Lorentz-structure roadmap: replace the earlier simple momentum proxy with a momentum definition derived from the Lagrangian.

## Key Theory Point

The earlier relativistic prototype used the spatial energy:

```text
E = 1/2 |p|^2 + 1/2 |grad s|^2
    + kappa/2 |s_x x s_y|^2 + V(s)
```

This is useful numerically but not the full Lorentz-covariant baby-Skyrme structure.

A Lorentz-covariant baby-Skyrme Lagrangian contains:

```text
F_mu_nu F^mu_nu,  F_mu_nu = partial_mu s x partial_nu s
```

which introduces time-space terms:

```text
|p x s_x|^2 and |p x s_y|^2
```

## Noether-Corrected Quantities

For the diagnostic Lagrangian:

```text
L = 1/2 |p|^2 - 1/2(|s_x|^2+|s_y|^2)
    + kappa/2(|p x s_x|^2 + |p x s_y|^2 - |s_x x s_y|^2)
    - V(s)
```

we compute:

```text
pi = dL/dp
   = p + kappa [s_x x (p x s_x) + s_y x (p x s_y)]
```

and:

```text
P_x = -∫ pi · s_x dxdy
E   = ∫ [pi · p - L] dxdy
```

These are compared against the previous simple definitions.

## Result

The Noether correction changes momentum and energy in the expected direction:

- `P_noether_x` is systematically larger than `P_simple_x`.
- `E_noether` is systematically larger than `E_simple` at non-zero boost.
- Time-space Skyrme terms grow with boost.

However, the invariant proxy:

```text
E^2 - P^2
```

still drifts with boost. For example, at `v=0.4` the normalized Noether invariant is approximately:

```text
mu2=0.00: M²/M0² ≈ 0.9889
mu2=0.02: M²/M0² ≈ 0.9866
```

## Interpretation

A5 gives an important correction but does not fully resolve the Lorentz issue.

Most important conclusion:

> The current evolution equations are still not the fully covariant baby-Skyrme equations, because the dynamics uses only the spatial Skyrme energy and not the full time-space Skyrme coupling.

Therefore the next required step is not only better diagnostics, but a fully covariant Euler-Lagrange solver or an approximation that includes the correct time-space Skyrme terms in the canonical momentum and equations of motion.

## Next Steps

1. Derive or implement the fully covariant constrained Euler-Lagrange equations.
2. Include the canonical momentum relation `pi = dL/dp` in the actual dynamics.
3. Re-run the Lorentz boost and energy-momentum tests.
4. Then proceed to larger domains and resolution sweeps.
