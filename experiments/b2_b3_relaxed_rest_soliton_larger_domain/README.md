# B2/B3 — Larger-Domain Higher-Resolution Relaxed Rest Soliton

## Purpose

This experiment improves B1 by reducing discretization and boundary artifacts before repeating covariant Lorentz boost diagnostics.

The changes are:

- larger domain,
- larger free region,
- higher grid resolution than the minimal sanity runs,
- same projected static relaxation method.

## Method

The field is relaxed using projected gradient descent on the static baby-Skyrme energy:

```text
E_static = ∫ [ 1/2(|s_x|² + |s_y|²)
             + κ/2 |s_x × s_y|²
             + μ²(1 - s_z) ] dxdy
```

Target-space constraint:

```text
|s| = 1
```

A fixed north-pole boundary remains in place outside the circular free region.

## Parameters

```text
N = 40
L = 40.0
dx = 1.0
radius = 16.8
κ = 0.2
μ² = 0.02
```

## Result

The static energy relaxes by about 9.8%:

```text
E: 22.1352 -> 19.9707
```

Topological charge improves compared with B1:

```text
B1 final Q      ≈ -0.9102
B2/B3 final Q   ≈ -0.9441
```

The relaxed state remains isotropic:

```text
sigma_x ≈ sigma_y
width ratio ≈ 1.0
```

The topological drift during relaxation is smaller than in B1:

```text
Q drift ≈ 0.00155
```

However, there is still non-negligible topological density near the boundary:

```text
boundary |Q| ≈ 0.0507
```

## Interpretation

B2/B3 confirms that larger domain and resolution improve the rest soliton quality and bring Q closer to the intended integer sector. The remaining boundary charge indicates that fixed circular boundaries are still a significant source of Lorentz and topological error.

This relaxed state is a better input for the next covariant boost diagnostics than the raw hedgehog ansatz.

## Next Steps

1. Use this relaxed state for a covariant boost test.
2. Compare `E/E0`, `E²-P²`, and `sigma_x/sigma_x0` against the previous non-relaxed boost test.
3. Later improve the boundary condition or increase the margin further.
