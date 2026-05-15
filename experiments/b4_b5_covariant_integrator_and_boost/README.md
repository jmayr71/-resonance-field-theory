# B4/B5 — Covariant Integrator and Relaxed-State Boost Retest

## Purpose

This experiment combines B4 and B5 from the Lorentz-validation roadmap.

B4 checks whether reducing the time step improves the covariant Hamiltonian evolution.

B5 repeats the covariant boost diagnostics using a short-relaxed rest profile instead of the raw hedgehog ansatz.

## Model

The solver evolves canonical variables:

```text
(s, pi)
```

with velocity recovered from:

```text
p = A(s)^-1 pi
```

and canonical momentum initialized from the boosted velocity:

```text
pi = A(s) p
```

The Hamiltonian includes the covariant time-space Skyrme terms:

```text
|p × s_x|² and |p × s_y|²
```

## Test Setup

Two time-step configurations are compared:

```text
baseline_dt = 0.00012, steps = 12
small_dt    = 0.00006, steps = 24
```

The physical time window is therefore comparable.

Boost values:

```text
v = 0.0, 0.2, 0.4
```

The rest profile is first relaxed with projected static gradient descent and then used as the boost source.

## Results

### Integrator effect

The baseline and small-step runs produce essentially identical Lorentz diagnostics. This indicates that, within this short run, the time-step/integrator error is not the dominant source of the remaining Lorentz mismatch.

### Energy scaling

Energy scaling improves strongly compared with earlier non-relaxed runs:

```text
v=0.4: E/E0 ≈ 1.0774
expected gamma ≈ 1.0911
```

This is significantly closer to the expected gamma scaling than previous tests.

### Invariant proxy

The invariant proxy behaves mixed:

```text
v=0.2: M²/M0² ≈ 0.9938
v=0.4: M²/M0² ≈ 1.0139
```

The v=0.2 result is good. The v=0.4 result overshoots above 1, suggesting that the boosted relaxed-state interpolation, boundary, and/or low resolution still introduce systematic artifacts.

### Width contraction

The contraction proxy remains qualitatively correct but weaker than the ideal expectation:

```text
v=0.2: sigma_x/sigma_x0 ≈ 0.9951, expected 1/gamma ≈ 0.9798
v=0.4: sigma_x/sigma_x0 ≈ 0.9627, expected 1/gamma ≈ 0.9165
```

### Stability

The evolution remains highly stable:

- energy drift during each run is near numerical precision,
- Q drift is approximately 1e-7,
- |s|, pi·s and p·s constraints remain near machine precision.

## Interpretation

This is a mixed but valuable result.

Positive:

- relaxed rest states improve energy scaling substantially;
- covariant Hamiltonian evolution is highly stable;
- smaller time step does not materially change the result, so the integrator is likely not the leading error;
- v=0.2 gives a good invariant proxy.

Open issue:

- v=0.4 overshoots in M²/M0², indicating that boost initialization, boundary effects and low resolution remain significant.

## Main conclusion

The next dominant error source is not the short-time integrator. The next step should focus on:

1. better boost initialization of the relaxed state,
2. larger domain and boundary margin,
3. higher resolution,
4. possibly a smoother boundary instead of hard circular projection.

## Files

- `b4_b5_covariant_integrator_and_boost.py`: full experiment code.
- `b4_b5_summary.csv`: boost summary diagnostics.
- `b4_b5_timeseries.csv`: sampled time evolution diagnostics.
- `relaxed_rest_profile_used.npy`: rest profile used for the boost test.
