# Resonance Field Theory

This repository contains early exploratory prototypes for a hypothetical resonance-based field model.

The current prototype is **not established physics**. It is a numerical toy model used to explore whether stable topological vortex configurations can be represented as resonance-like field defects.

## Current prototype

The first prototype simulates a two-dimensional nonlinear resonance field using a split-step Fourier method for a defocusing Gross-Pitaevskii / nonlinear Schrödinger-type equation.

The simulation initializes a vortex with winding number `n = -1` and tracks:

- field amplitude,
- field phase,
- approximate winding number,
- energy,
- vortex core position.

## Initial result

The first stable run preserved the topological winding:

- Final approximate winding number: `-1.0000`
- Final energy: `~180.35`

This is only a first numerical sanity check. It does not prove a physical electron model. It shows that the selected toy dynamics can preserve a topological vortex-like defect under time evolution.

## Repository structure

```text
prototype/
  stable_resonance_vortex_prototype.py

requirements.txt
README.md
```

## Run

```bash
pip install -r requirements.txt
python prototype/stable_resonance_vortex_prototype.py
```

## Next steps

1. Add a vortex/anti-vortex simulation with `n = -1` and `n = +1`.
2. Track annihilation-like behavior and emitted wave energy.
3. Extend the scalar field to a two-component spinor field.
4. Investigate whether spinor-like transformation behavior can be represented.
5. Refactor into reusable simulation modules and automated experiments.

## Scientific caution

This project is exploratory and speculative. It should be treated as a sandbox for mathematical and numerical model-building, not as a validated alternative to the Standard Model or General Relativity.
