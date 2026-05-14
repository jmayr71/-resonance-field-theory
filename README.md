# Resonance Field Theory

Exploratory numerical sandbox for resonance-/field-based particle models.

The project is **not established physics** and does **not** claim to replace the Standard Model or General Relativity. It is a research notebook in code form: a sequence of toy models used to test whether stable, particle-like structures can arise as topological or quasi-topological field configurations.

## Current status

The project has moved from scalar vortex experiments to a clearer topological formulation:

1. Scalar nonlinear field models produced stable vortex-like defects, but no clean braiding.
2. Two-component chiral spinor models produced stable defects and non-trivial global phases, but the signed Skyrmion-like charge was not quantized.
3. A CP¹ / nonlinear sigma model with fixed boundary conditions produced robust, nearly integer topological sectors.
4. Multi-sector tests now show stable families with approximately `Q = ±1, ±2, ±3`.

The current best-supported theoretical direction is therefore:

> particle-like structures should be modelled as extended topological spin textures, not merely as orbiting scalar vortices.

## Repository structure

```text
docs/
  theory_status.md
  results_log.md

simulations/
  cp1_fixed_boundary.py
  cp1_multi_sector_test.py

experiments/
  cp1_multi_sector/
    multi_sector_summary.csv
  q_stability/
    q_stability_summary.csv
  skyrme_prototypes/
    skyrme_stabilized_summary.txt
    variational_skyrme_force_summary.txt
```

## Main result so far

The CP¹ fixed-boundary sector test produced:

```text
Q: -0.998794 -> -0.998791
```

The multi-sector test produced stable topological sectors:

```text
Q ≈ ±1, ±2, ±3
```

This is the first point in the project where the numerical model shows a genuinely robust topological charge family.

## Run examples

```bash
pip install numpy pandas matplotlib scipy
python simulations/cp1_fixed_boundary.py
python simulations/cp1_multi_sector_test.py
```

## Scientific caution

All models here are exploratory. The CP¹/Sigma results demonstrate robust mathematical topological sectors in a toy field model; they do not yet demonstrate physical elementary particles, quantum statistics, or a validated theory of spacetime.
