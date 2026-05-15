"""
Relativistic boosted baby-Skyrme prototype.

Purpose
-------
Test whether a CP1/S2 topological soliton can propagate coherently under
relativistic second-order constrained dynamics.

Model
-----
Field:
    s(x,y,t) in S^2, |s| = 1
Momentum:
    p = ∂t s, with s·p = 0

Energy:
    E = ∫ [ 1/2 |p|^2 + 1/2 |∇s|^2
            + κ/2 |∂x s × ∂y s|^2
            + μ²(1 - s_z) ] dxdy

Initial boost approximation:
    p = -v ∂x s
projected to the tangent space of S^2.

Numerics
--------
- PyTorch autograd for the exact discrete gradient of the field potential.
- Projected velocity-Verlet style update.
- Hard fixed north-pole boundary outside a circular free region.
- Diagnostics: Q, energy, constraints, center of topological density.
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch


def run(output_dir="/mnt/data/relativistic_boosted_skyrmion_small"):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    device = torch.device("cpu")
    dtype = torch.float64

    N = 28
    L = 24.0
    dx = L / N
    x = np.linspace(-L/2, L/2 - dx, N)
    y = np.linspace(-L/2, L/2 - dx, N)
    X, Y = np.meshgrid(x, y, indexing="ij")
    R = np.sqrt(X**2 + Y**2)
    Phi = np.arctan2(Y, X)

    dt = 0.00045
    steps = 160
    sample_every = 10

    kappa = 0.20
    mu2 = 0.02
    size = 3.5
    boost_v = 0.20
    radius = L * 0.36

    free_np = R < radius
    free = torch.tensor(free_np, dtype=torch.bool, device=device)
    north = torch.tensor([0.0, 0.0, 1.0], dtype=dtype, device=device).view(3, 1)

    def norm_np(s):
        return s/(np.sqrt(np.sum(s*s, axis=0))+1e-12)

    f = 2*np.arctan(size/(R+1e-9))
    s0 = norm_np(np.stack([
        np.sin(f)*np.cos(Phi),
        np.sin(f)*np.sin(Phi),
        np.cos(f)
    ], axis=0))
    s0[0, ~free_np] = 0
    s0[1, ~free_np] = 0
    s0[2, ~free_np] = 1

    ds_dx = (np.roll(s0, -1, axis=1) - np.roll(s0, 1, axis=1))/(2*dx)
    p0 = -boost_v * ds_dx
    p0[:, ~free_np] = 0

    s = torch.tensor(s0, dtype=dtype, device=device)
    p = torch.tensor(p0, dtype=dtype, device=device)

    def normalize_s(s):
        return s/(torch.linalg.norm(s, dim=0, keepdim=True)+1e-12)

    def project(v, s):
        return v - torch.sum(v*s, dim=0, keepdim=True)*s

    def constrain(s, p):
        s = normalize_s(s.clone())
        s[:, ~free] = north
        p = project(p.clone(), s)
        p[:, ~free] = 0.0
        return s, p

    s, p = constrain(s, p)

    def gx(u):
        return (torch.roll(u,-1,1)-torch.roll(u,1,1))/(2*dx)

    def gy(u):
        return (torch.roll(u,-1,2)-torch.roll(u,1,2))/(2*dx)

    def V_torch(s):
        sx = gx(s)
        sy = gy(s)
        sigma = 0.5*torch.sum(sx*sx+sy*sy, dim=0)
        cross = torch.cross(sx.permute(1,2,0), sy.permute(1,2,0), dim=2).permute(2,0,1)
        sk = 0.5*kappa*torch.sum(cross*cross, dim=0)
        pot = mu2*(1-s[2])
        return torch.sum((sigma+sk+pot)[free])*dx*dx

    def force(s):
        st = s.detach().clone().requires_grad_(True)
        V = V_torch(st)
        grad, = torch.autograd.grad(V, st, create_graph=False)
        F = -grad.detach()
        F[:, ~free] = 0
        return project(F, s)

    def e_np(snp, pnp):
        sx = (np.roll(snp,-1,axis=1)-np.roll(snp,1,axis=1))/(2*dx)
        sy = (np.roll(snp,-1,axis=2)-np.roll(snp,1,axis=2))/(2*dx)
        sigma = 0.5*np.sum(sx*sx+sy*sy, axis=0)
        cross = np.cross(sx.transpose(1,2,0), sy.transpose(1,2,0)).transpose(2,0,1)
        sk = 0.5*kappa*np.sum(cross*cross, axis=0)
        pot = mu2*(1-snp[2])
        kin = 0.5*np.sum(pnp*pnp, axis=0)
        return {
            "E_kinetic": float(np.sum(kin[free_np])*dx*dx),
            "E_field": float(np.sum((sigma+sk+pot)[free_np])*dx*dx),
            "E_total": float(np.sum((kin+sigma+sk+pot)[free_np])*dx*dx)
        }

    def q_np(snp):
        sx = (np.roll(snp,-1,axis=1)-np.roll(snp,1,axis=1))/(2*dx)
        sy = (np.roll(snp,-1,axis=2)-np.roll(snp,1,axis=2))/(2*dx)
        cross = np.cross(sx.transpose(1,2,0), sy.transpose(1,2,0)).transpose(2,0,1)
        return np.sum(snp*cross, axis=0)/(4*np.pi)

    def center_from_q(q):
        w = np.abs(q) * free_np
        total = np.sum(w)
        if total <= 1e-12:
            return np.nan, np.nan
        return float(np.sum(X*w)/total), float(np.sum(Y*w)/total)

    def step_verlet(s, p):
        F = force(s)
        p_half = p + 0.5*dt*F
        p_half = project(p_half, s)
        p_half[:, ~free] = 0

        s_new = s + dt*p_half
        s_new, p_half = constrain(s_new, p_half)

        F_new = force(s_new)
        p_new = p_half + 0.5*dt*F_new
        s_new, p_new = constrain(s_new, p_new)
        return s_new.detach(), p_new.detach()

    records = []
    snaps = {}
    for n in range(steps+1):
        if n % sample_every == 0:
            snp = s.detach().cpu().numpy()
            pnp = p.detach().cpu().numpy()
            q = q_np(snp)
            cx, cy = center_from_q(q)
            en = e_np(snp, pnp)
            records.append({
                "step": n,
                "time": n*dt,
                "Q_signed": float(np.sum(q[free_np])*dx*dx),
                "Q_abs": float(np.sum(np.abs(q[free_np]))*dx*dx),
                "center_x": cx,
                "center_y": cy,
                "max_norm_deviation": float(np.max(np.abs(np.sqrt(np.sum(snp*snp,axis=0))[free_np]-1))),
                "max_sp_deviation": float(np.max(np.abs(np.sum(snp*pnp,axis=0)[free_np]))),
                "min_sz": float(np.min(snp[2,free_np])),
                **en
            })
        if n in [0, 80, 160]:
            snaps[n] = s.detach().cpu().numpy()
        if n < steps:
            s, p = step_verlet(s,p)

    df = pd.DataFrame(records)
    df["relative_energy_change"] = (df.E_total-df.E_total.iloc[0])/abs(df.E_total.iloc[0])
    df["Q_drift"] = df.Q_signed-df.Q_signed.iloc[0]
    df["center_dx"] = df.center_x-df.center_x.iloc[0]
    df["center_dy"] = df.center_y-df.center_y.iloc[0]
    df.to_csv(out/"boosted_relativistic_skyrmion_timeseries.csv", index=False)

    summary = {
        "prototype_type": "Small boosted relativistic baby-Skyrme CP1/S2 prototype",
        "N": N, "L": L, "dt": dt, "steps": steps, "kappa": kappa, "mu2": mu2,
        "boost_v": boost_v,
        "initial_Q_signed": float(df.Q_signed.iloc[0]),
        "final_Q_signed": float(df.Q_signed.iloc[-1]),
        "Q_drift": float(df.Q_signed.iloc[-1]-df.Q_signed.iloc[0]),
        "initial_E_total": float(df.E_total.iloc[0]),
        "final_E_total": float(df.E_total.iloc[-1]),
        "relative_energy_change": float(df.relative_energy_change.iloc[-1]),
        "max_norm_deviation": float(df.max_norm_deviation.max()),
        "max_sp_deviation": float(df.max_sp_deviation.max()),
        "initial_center_x": float(df.center_x.iloc[0]),
        "final_center_x": float(df.center_x.iloc[-1]),
        "center_dx": float(df.center_dx.iloc[-1]),
        "initial_center_y": float(df.center_y.iloc[0]),
        "final_center_y": float(df.center_y.iloc[-1]),
        "center_dy": float(df.center_dy.iloc[-1]),
        "initial_E_kinetic": float(df.E_kinetic.iloc[0]),
        "final_E_kinetic": float(df.E_kinetic.iloc[-1]),
    }
    (out/"summary.txt").write_text("\n".join(f"{k}: {v}" for k,v in summary.items()), encoding="utf-8")
    return summary


if __name__ == "__main__":
    summary = run()
    for k, v in summary.items():
        print(f"{k}: {v}")
