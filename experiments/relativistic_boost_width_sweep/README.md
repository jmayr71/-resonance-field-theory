# Relativistic Boost Width Sweep

## Purpose

This experiment tests whether boosted relativistic CP1/S2 baby-Skyrme solitons show systematic deformation of their topological-density profile. It is the first proxy test for Lorentz-type contraction in the current theory roadmap.

## Model

Field: `s(x,y,t) in S^2` with `|s| = 1`.

Momentum: `p = ∂t s`, constrained by `s · p = 0`.

Energy density:

```text
E = 1/2 |p|^2 + 1/2 |∇s|^2
    + κ/2 |∂x s × ∂y s|^2
    + μ²(1 - s_z)
```

Initial boost proxy:

```text
p = -v ∂x s
```

## Diagnostics

For each boost value the experiment records:

- topological charge Q,
- energy drift,
- effective center velocity,
- topological-density widths σx and σy,
- width ratio σx / σy,
- kinetic energy,
- constraint deviations for `|s|=1` and `s·p=0`.

## Result

The measured center velocity grows approximately linearly with the boost parameter. The width ratio `σx/σy` decreases weakly but systematically from `1.000000` to `0.999971` over the tested boost range `v=0.0..0.4`.

This is not yet a proof of Lorentz contraction. The initial condition is not an exact Lorentz-transformed solution and the grid is intentionally small. However, it is a positive exploratory signal that boosted solitons deform consistently in the expected direction.

## Next steps

1. Increase resolution and runtime.
2. Improve the constrained symplectic integrator.
3. Construct analytically Lorentz-transformed initial states.
4. Compare measured width ratio to `1/gamma`.
5. Test boosted two-soliton scattering.
