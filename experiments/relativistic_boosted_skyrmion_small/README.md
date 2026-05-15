# Relativistic Boosted Baby-Skyrme Prototype

## Goal

Test whether a topological CP1/S2 soliton can propagate coherently under a relativistic second-order constrained dynamics.

This experiment is the next step after the first relativistic baby-Skyrme prototype and addresses Lorentz-structure topic A of the theory roadmap.

## Model

Field:

s(x,y,t) in S^2

Constraint:

|s| = 1

Momentum field:

p = ∂t s

with tangent-space constraint:

s · p = 0

Energy density:

E = 1/2 |p|^2 + 1/2 |∇s|^2
    + κ/2 |∂x s × ∂y s|^2
    + μ²(1 - s_z)

## Initial Condition

A degree-1 Skyrmion-like configuration is initialized.

A boost-like initial momentum is added via:

p = -v ∂x s

followed by tangent-space projection.

## Numerical Method

- PyTorch autograd for exact discrete field gradients.
- Projected velocity-Verlet style integrator.
- Circular fixed north-pole boundary.
- Constraint re-normalization after every substep.

## Diagnostics

- Topological charge Q
- Total energy
- Constraint preservation
- Topological density center trajectory

## Main Result

The boosted topological structure propagates coherently in x direction while preserving:

- topological charge approximately,
- S² normalization,
- tangent momentum constraint.

This is the first evidence in the project that the topological CP1/S2 structure is compatible with relativistic propagation rather than only nonrelativistic Landau-Lifshitz precession.

## Current Limitations

- Small grid.
- No true Lorentz-boost initial state yet.
- Energy conservation still limited by simple Verlet integrator.
- No explicit Lorentz contraction measurement yet.
- CPU-only execution.

## Next Steps

1. Improve symplectic constrained integration.
2. Increase resolution.
3. Construct analytically boosted initial states.
4. Measure dispersion relation.
5. Test relativistic scattering.
6. Investigate emergence of causal propagation speed.
