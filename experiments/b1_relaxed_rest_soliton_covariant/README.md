# B1 — Relaxed Rest Soliton for the Covariant Programme

## Purpose

This experiment creates a better rest-frame soliton than the raw hedgehog ansatz before repeating Lorentz boost diagnostics.

Boosting a non-relaxed ansatz injects shape and oscillation artifacts into the Lorentz tests. A relaxed rest soliton should improve later comparisons of:

```text
E/E0
E² - P²
sigma_x/sigma_x0
```

against relativistic expectations.

## Method

The field remains:

```text
s(x,y) in S²
```

The initial condition is a Q≈-1 hedgehog-like profile. It is relaxed using projected gradient descent on the static baby-Skyrme energy:

```text
E_static = ∫ [ 1/2(|s_x|² + |s_y|²)
             + κ/2 |s_x × s_y|²
             + μ²(1 - s_z) ] dxdy
```

The target constraint is enforced after each step:

```text
|s| = 1
```

A fixed north-pole boundary is used outside the circular free region.

## Result

The relaxation reduces the static field energy by about 13%:

```text
E: 19.2902 -> 16.7554
```

The final state remains symmetric:

```text
sigma_x ≈ sigma_y
width ratio ≈ 1.0
```

Topological charge remains near the intended Q≈-1 sector:

```text
Q: -0.9169 -> -0.9102
```

The norm constraint is preserved to numerical precision.

## Interpretation

This is a better rest-frame input state for later covariant boost tests than the raw hedgehog ansatz. However, Q is still under-resolved compared with an ideal integer value, so B2/B3 should increase domain and resolution before final Lorentz diagnostics.

## Next Steps

1. Repeat relaxation on a larger grid and larger domain.
2. Use the relaxed state as the input for the covariant boost test.
3. Compare Lorentz diagnostics against the previous non-relaxed boost tests.
