# Fully Covariant Baby-Skyrme Solver Specification

## 1. Purpose

This note defines the next theoretical and numerical step for the project: replacing the current partially relativistic CP1/S2 solver with a fully covariant baby-Skyrme solver.

The current relativistic prototypes already show:

- stable CP1/S2 topology,
- propagating boosted solitons,
- Lorentz-like contraction signals,
- stable constraints,
- systematic momentum response.

However, the Noether diagnostic showed that the current evolution equations are not yet fully Lorentz covariant because they evolve with a spatial Skyrme energy but do not include the full time-space Skyrme coupling in the dynamics.

The goal of the next solver is therefore:

> evolve the field using the fully covariant baby-Skyrme Lagrangian, including the correct canonical momentum and time-space Skyrme terms.

---

## 2. Field and Constraints

The fundamental field remains a normalized three-component internal field:

```text
s(x,y,t) in S^2
```

with:

```text
s · s = 1
```

The velocity field is:

```text
p = ∂t s
```

and must remain tangent to the target sphere:

```text
s · p = 0
```

The topological charge is still:

```text
Q = 1/(4π) ∫ s · (∂x s × ∂y s) dx dy
```

This remains the topological sector label.

---

## 3. Covariant Lagrangian

Use metric convention:

```text
η = diag(+1, -1, -1)
```

in 2+1 dimensions.

Define:

```text
∂0 s = p
∂1 s = sx = ∂x s
∂2 s = sy = ∂y s
```

The covariant baby-Skyrme Lagrangian density is:

```text
L = 1/2 ∂μs · ∂^μs
    - κ/4 (∂μs × ∂νs) · (∂^μs × ∂^νs)
    - V(s)
```

With the chosen metric, this can be written in 2+1 form as:

```text
L = 1/2 |p|^2
    - 1/2 (|sx|^2 + |sy|^2)
    + κ/2 (|p × sx|^2 + |p × sy|^2 - |sx × sy|^2)
    - V(s)
```

Typical stabilizing potential:

```text
V(s) = μ² (1 - sz)
```

but the solver must support `μ²=0` as a diagnostic case.

---

## 4. Canonical Momentum

The canonical momentum is not equal to `p` once the covariant Skyrme term is active.

It is:

```text
π = ∂L/∂p
```

Using the 2+1 form:

```text
π = p + κ [ sx × (p × sx) + sy × (p × sy) ]
```

Equivalently, using the identity:

```text
a × (p × a) = |a|² p - (a · p) a
```

we can write:

```text
π = A(s) p
```

where:

```text
A(s) = I
     + κ [ |sx|² I - sx sxᵀ
           + |sy|² I - sy syᵀ ]
```

Therefore the velocity is obtained from canonical momentum by solving:

```text
p = A(s)^(-1) π
```

pointwise on the grid.

This is the key structural change from the current solver.

---

## 5. Hamiltonian Density

The Hamiltonian density is:

```text
H = π · p - L
```

where `p = A(s)^(-1) π`.

Substituting the Lagrangian:

```text
H = 1/2 |p|²
    + 1/2 (|sx|² + |sy|²)
    + κ/2 (|p × sx|² + |p × sy|² + |sx × sy|²)
    + V(s)
```

Important difference to earlier prototypes:

> The time-space Skyrme terms `|p × sx|²` and `|p × sy|²` now appear in the energy and in the momentum relation.

---

## 6. Noether Energy and Momentum

The correct energy is:

```text
E = ∫ H dx dy
```

The spatial momentum is:

```text
P_i = -∫ π · ∂i s dx dy
```

Therefore:

```text
Px = -∫ π · sx dx dy
Py = -∫ π · sy dx dy
```

The Lorentz diagnostic becomes:

```text
M_eff² = E² - Px² - Py²
```

For a good relativistic solver and good boundaries, `M_eff²` should be approximately boost independent.

---

## 7. Numerical State Variables

The new solver should evolve:

```text
(s, π)
```

not:

```text
(s, p)
```

At each step:

1. Enforce `s · s = 1`.
2. Project `π` to the tangent cotangent space if needed:

```text
π ← π - (π · s) s
```

3. Recover velocity:

```text
p = A(s)^(-1) π
```

4. Evolve:

```text
∂t s = p
∂t π = -δH/δs + constraint terms
```

The derivative `δH/δs` should initially be computed by PyTorch autograd from the discrete Hamiltonian. Later, an analytic operator can replace autograd.

---

## 8. Minimal First Implementation Strategy

The smallest viable fully covariant prototype should do the following:

### Step 1 — Pointwise A-matrix inversion

Implement function:

```text
p = velocity_from_momentum(s, π)
```

For each grid cell, compute:

```text
A = I
  + κ [ |sx|² I - sx sxᵀ
        + |sy|² I - sy syᵀ ]
```

and solve:

```text
A p = π
```

Since this is a 3x3 system per grid point, it is cheap and GPU-friendly.

### Step 2 — Hamiltonian functional

Implement:

```text
H[s, π] = ∫ H_density(s, p(s,π)) dxdy
```

with:

```text
H_density = 1/2 |p|²
          + 1/2 (|sx|² + |sy|²)
          + κ/2 (|p × sx|² + |p × sy|² + |sx × sy|²)
          + V(s)
```

### Step 3 — Autograd force

Use autograd to compute:

```text
δH/δs
δH/δπ
```

and verify:

```text
δH/δπ ≈ p
```

This is a critical internal consistency test.

### Step 4 — Time integration

Initial prototype can use projected leapfrog / symplectic Euler:

```text
π_half = π - dt/2 * projected(δH/δs)
s_new  = normalize(s + dt * δH/δπ_half)
π_new  = π_half - dt/2 * projected(δH/δs_new)
```

This is not yet an ideal geometric integrator, but it is sufficient for the first validation.

### Step 5 — Constraints

After each substep:

```text
s ← s / |s|
π ← π - (π · s) s
```

Boundary values remain fixed initially, but this must later be improved.

---

## 9. Validation Plan

### Validation 1 — static rest soliton

Start with a rest soliton:

```text
π = 0
```

Check:

- `Q` remains stable,
- `E` remains stable,
- `|s|=1`,
- `π·s=0`,
- `p=0` initially.

### Validation 2 — velocity recovery

For a known test velocity `p_test`, compute:

```text
π = A(s) p_test
```

then recover:

```text
p_recovered = A(s)^(-1) π
```

Check:

```text
||p_recovered - p_test|| ≈ 0
```

### Validation 3 — boosted initialization

Use Lorentz-initialized state:

```text
s_v(x,y,0) = s0(γx,y)
p_v(x,y,0) = -γv ∂x s0(γx,y)
π_v = A(s_v) p_v
```

Then measure:

```text
E/E0 ≈ γ
E² - P² ≈ constant
σx/σx0 ≈ 1/γ
```

### Validation 4 — potential sensitivity

Run with:

```text
μ² = 0
μ² = 0.02
```

to isolate the impact of the potential.

### Validation 5 — domain and boundary sensitivity

Repeat on larger domains and with wider boundary margins.

---

## 10. Expected Risks

### Risk 1 — Instability from Hamiltonian projection

Projection after each step may break symplecticity and energy conservation.

Mitigation:

- start with very small time steps;
- monitor energy drift;
- later implement a better constrained symplectic integrator.

### Risk 2 — Boundary still breaks Lorentz invariance

Fixed circular boundaries remain a major limitation.

Mitigation:

- increase domain size;
- move soliton far from boundary;
- test absorbing or soft boundary layers later.

### Risk 3 — Autograd cost

The Hamiltonian depends on `p=A(s)^(-1)π`, so autograd is heavier than before.

Mitigation:

- small first grid;
- later analytic gradients;
- GPU execution.

### Risk 4 — Static ansatz is not relaxed

The hedgehog profile is not the exact energy minimizer.

Mitigation:

- relax rest soliton first;
- use relaxed state as boost input.

---

## 11. Success Criteria for First Prototype

The first fully covariant prototype is successful if it shows:

```text
|s| deviation <= 1e-10
π·s deviation <= 1e-10
Q drift <= 1e-4
relative E drift <= 1e-4 over short run
```

and if the Lorentz diagnostic improves compared with the previous solver:

```text
M_eff²/M0² closer to 1 across boosts
```

The first goal is not perfection. The first goal is to confirm that including canonical momentum and time-space Skyrme terms improves Lorentz consistency.

---

## 12. Strategic Meaning for the Theory

This step is essential because it decides whether the current theory is merely Lorentz-like or can be formulated as a genuinely Lorentz-covariant topological field theory.

If successful, the theory can continue toward:

- relativistic soliton scattering,
- controlled energy-momentum relations,
- later gauge coupling,
- and eventually quantization.

If unsuccessful, the theory may still describe useful topological quasiparticles, but not fundamental relativistic particle analogues.
