# Relativistic Energy-Momentum Diagnostic

## Purpose

This experiment tests whether boosted CP1/S2 baby-Skyrme solitons show an approximate relativistic energy-momentum relation.

The intended relativistic relation is:

```text
E^2 ≈ P^2 + M^2
```

or equivalently for boosted states:

```text
E(v) / E(0) ≈ gamma
```

## Diagnostics

The experiment measures:

- total energy `E`,
- momentum proxy `P_x = -∫ p · ∂x s dxdy`,
- invariant proxy `M_eff² = E² - P_x² - P_y²`,
- topological charge `Q`,
- energy drift,
- momentum drift,
- effect of potential coefficient `mu2`.

## Result

The dynamics preserves energy and momentum very well during each short run.

However, the Lorentz invariant proxy is not yet stable across boost values:

- for `mu2=0.0`, `M_eff²/M0²` drops from `1.000` to about `0.990` at `v=0.4`.
- for `mu2=0.02`, `M_eff²/M0²` drops from `1.000` to about `0.987` at `v=0.4`.

Energy scaling is also weaker than ideal `gamma` scaling.

## Interpretation

This is a mixed result:

Positive:

- `P_x` scales strongly and systematically with boost.
- Energy and momentum are nearly conserved during evolution.
- Topological charge remains stable.
- Constraints remain stable.

Open issue:

- The continuum Lorentz relation `E²-P²=M²` is not yet reproduced accurately.

Likely causes:

1. finite circular boundary explicitly breaks Lorentz symmetry;
2. finite-difference discretization introduces lattice artifacts;
3. initial profile is still an approximate boosted ansatz, not an exact moving solution;
4. the potential and baby-Skyrme terms may require more careful relativistic normalization;
5. low resolution is too coarse for quantitative dispersion tests.

## Next Steps

1. Improve boundary handling or move to a larger computational domain.
2. Increase resolution.
3. Test periodic or absorbing boundary alternatives.
4. Derive the full Noether energy-momentum tensor for the chosen Lagrangian.
5. Compare numerical `P_x` against the Noether momentum, not only the canonical proxy.
6. Repeat the test with an analytically relaxed rest soliton rather than the simple hedgehog ansatz.
