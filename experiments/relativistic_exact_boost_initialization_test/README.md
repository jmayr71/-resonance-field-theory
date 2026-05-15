# Lorentz-Transformed Initialization Test

## Purpose

This experiment is a stricter Lorentz-structure test than the earlier heuristic boost `p = -v ∂x s`.

For a static profile `s0(x,y)`, the boosted initial state is approximated as:

```text
s_v(x,y,0) = s0(gamma * x, y)
p_v(x,y,0) = -gamma * v * ∂x s0(gamma * x, y)
```

with:

```text
gamma = 1 / sqrt(1 - v^2)
```

## Expected Lorentz Signals

An ideal Lorentz-invariant continuum model should approximately show:

```text
sigma_x(v) / sigma_x(0) ≈ 1/gamma
E(v) / E(0) ≈ gamma
```

## Result

The width contraction proxy shows a clear qualitative signal:

```text
v=0.0: sigma_x/sigma_x0 = 1.000000, expected 1/gamma = 1.000000
v=0.1: sigma_x/sigma_x0 = 0.996844, expected 1/gamma = 0.994987
v=0.2: sigma_x/sigma_x0 = 0.987207, expected 1/gamma = 0.979796
v=0.3: sigma_x/sigma_x0 = 0.970553, expected 1/gamma = 0.953939
v=0.4: sigma_x/sigma_x0 = 0.945878, expected 1/gamma = 0.916515
```

This is not exact, but the trend is correct and much stronger than in the heuristic boost test.

The measured center velocity also scales strongly with the intended boost parameter:

```text
v=0.1 -> vx_eff ≈ 0.090
v=0.2 -> vx_eff ≈ 0.180
v=0.3 -> vx_eff ≈ 0.272
v=0.4 -> vx_eff ≈ 0.365
```

Energy scaling is still too weak compared with ideal `gamma` scaling, indicating that discretization, finite boundary, the potential term, and non-exact boosted solutions still matter.

## Interpretation

This is the strongest Lorentz-structure evidence so far:

- boosted profiles propagate coherently,
- topological charge remains stable,
- the x-width contracts qualitatively according to the expected `1/gamma` trend,
- measured propagation velocity tracks the boost parameter.

However, it is not yet a full Lorentz invariance proof. The next steps are higher resolution, better boundaries, better energy-momentum diagnostics, and analytic momentum evaluation.
