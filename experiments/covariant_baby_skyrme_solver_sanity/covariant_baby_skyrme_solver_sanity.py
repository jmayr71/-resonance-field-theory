"""
Sanity prototype for the fully covariant baby-Skyrme Hamiltonian solver.

This is intentionally very small. It validates the core structural change:
state variables are (s, pi), velocity is recovered by p = A(s)^-1 pi,
and the Hamiltonian includes time-space Skyrme terms.

Validation checks:
- p = A^-1 pi works numerically
- dH/dpi ≈ p
- constraints |s|=1 and pi·s=0
- short rest-soliton energy and Q stability
"""

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch


def run(output_dir="/mnt/data/covariant_baby_skyrme_solver_sanity"):
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    device = torch.device("cpu")
    dtype = torch.float64

    N = 14
    L = 20.0
    dx = L / N
    x = np.linspace(-L/2, L/2 - dx, N)
    y = np.linspace(-L/2, L/2 - dx, N)
    X, Y = np.meshgrid(x, y, indexing="ij")
    R = np.sqrt(X**2 + Y**2)
    Phi = np.arctan2(Y, X)

    dt = 0.00015
    steps = 20
    sample_every = 5

    kappa = 0.20
    mu2 = 0.02
    size = 3.2
    free_np = R < (L * 0.32)
    free = torch.tensor(free_np, dtype=torch.bool, device=device)
    north = torch.tensor([0.0, 0.0, 1.0], dtype=dtype, device=device).view(3,1)

    def normalize_np(a):
        return a/(np.sqrt(np.sum(a*a, axis=0))+1e-12)

    f = 2*np.arctan(size/(R+1e-9))
    s0 = normalize_np(np.stack([
        np.sin(f)*np.cos(Phi),
        np.sin(f)*np.sin(Phi),
        np.cos(f)
    ], axis=0))
    s0[0, ~free_np] = 0
    s0[1, ~free_np] = 0
    s0[2, ~free_np] = 1

    pi0 = np.zeros_like(s0)

    s = torch.tensor(s0, dtype=dtype, device=device)
    pi = torch.tensor(pi0, dtype=dtype, device=device)

    def normalize_s(s):
        return s/(torch.linalg.norm(s, dim=0, keepdim=True)+1e-12)

    def project(v, s):
        return v - torch.sum(v*s, dim=0, keepdim=True)*s

    def constrain(s, pi):
        s = normalize_s(s.clone())
        s[:, ~free] = north
        pi = project(pi.clone(), s)
        pi[:, ~free] = 0.0
        return s, pi

    s, pi = constrain(s, pi)

    def gx(u): return (torch.roll(u, -1, 1)-torch.roll(u, 1, 1))/(2*dx)
    def gy(u): return (torch.roll(u, -1, 2)-torch.roll(u, 1, 2))/(2*dx)

    def velocity_from_momentum(s, pi):
        sx = gx(s).permute(1,2,0)
        sy = gy(s).permute(1,2,0)
        piv = pi.permute(1,2,0)

        I = torch.eye(3, dtype=dtype, device=device).view(1,1,3,3)
        sx2 = torch.sum(sx*sx, dim=2).view(N,N,1,1)
        sy2 = torch.sum(sy*sy, dim=2).view(N,N,1,1)
        A = I + kappa*((sx2*I - sx[:,:,:,None]*sx[:,:,None,:]) +
                        (sy2*I - sy[:,:,:,None]*sy[:,:,None,:]))
        pv = torch.linalg.solve(A, piv[:,:,:,None]).squeeze(-1)
        p = pv.permute(2,0,1)
        p = project(p, s)
        p[:, ~free] = 0.0
        return p

    def H_torch(s, pi):
        p = velocity_from_momentum(s, pi)
        sx = gx(s)
        sy = gy(s)
        sxsy = torch.cross(sx.permute(1,2,0), sy.permute(1,2,0), dim=2).permute(2,0,1)
        psx = torch.cross(p.permute(1,2,0), sx.permute(1,2,0), dim=2).permute(2,0,1)
        psy = torch.cross(p.permute(1,2,0), sy.permute(1,2,0), dim=2).permute(2,0,1)
        Hd = (
            0.5*torch.sum(p*p, dim=0)
            + 0.5*(torch.sum(sx*sx, dim=0)+torch.sum(sy*sy, dim=0))
            + 0.5*kappa*(torch.sum(psx*psx, dim=0)+torch.sum(psy*psy, dim=0)+torch.sum(sxsy*sxsy, dim=0))
            + mu2*(1-s[2])
        )
        return torch.sum(Hd[free])*dx*dx

    def grad_H(s, pi):
        st = s.detach().clone().requires_grad_(True)
        pit = pi.detach().clone().requires_grad_(True)
        H = H_torch(st, pit)
        gs, gpi = torch.autograd.grad(H, (st, pit), create_graph=False)
        return H.detach(), gs.detach(), gpi.detach()

    def q_np(snp):
        sx = (np.roll(snp,-1,axis=1)-np.roll(snp,1,axis=1))/(2*dx)
        sy = (np.roll(snp,-1,axis=2)-np.roll(snp,1,axis=2))/(2*dx)
        cr = np.cross(sx.transpose(1,2,0), sy.transpose(1,2,0)).transpose(2,0,1)
        return np.sum(snp*cr, axis=0)/(4*np.pi)

    def diagnostics(s, pi):
        H, gs, gpi = grad_H(s, pi)
        p = velocity_from_momentum(s, pi)
        snp = s.detach().cpu().numpy()
        pinp = pi.detach().cpu().numpy()
        pnp = p.detach().cpu().numpy()
        gpinp = gpi.detach().cpu().numpy()
        q = q_np(snp)
        return {
            "E_total": float(H.cpu().item()),
            "Q_signed": float(np.sum(q[free_np])*dx*dx),
            "Q_abs": float(np.sum(np.abs(q[free_np]))*dx*dx),
            "max_norm_deviation": float(np.max(np.abs(np.sqrt(np.sum(snp*snp,axis=0))[free_np]-1))),
            "max_pi_s_deviation": float(np.max(np.abs(np.sum(snp*pinp,axis=0)[free_np]))),
            "max_p_s_deviation": float(np.max(np.abs(np.sum(snp*pnp,axis=0)[free_np]))),
            "max_dH_dpi_minus_p": float(np.max(np.abs((gpinp-pnp)[:,free_np]))),
            "max_p_abs": float(np.max(np.sqrt(np.sum(pnp*pnp, axis=0))[free_np])),
            "max_pi_abs": float(np.max(np.sqrt(np.sum(pinp*pinp, axis=0))[free_np])),
        }

    def step(s, pi):
        H, gs, gpi = grad_H(s, pi)
        force = -project(gs, s)
        force[:, ~free] = 0

        pi_half = pi + 0.5*dt*force
        s, pi_half = constrain(s, pi_half)

        _, _, gpi_half = grad_H(s, pi_half)
        dsdt = project(gpi_half, s)
        dsdt[:, ~free] = 0

        s_new = s + dt*dsdt
        s_new, pi_half = constrain(s_new, pi_half)

        _, gs_new, _ = grad_H(s_new, pi_half)
        force_new = -project(gs_new, s_new)
        force_new[:, ~free] = 0

        pi_new = pi_half + 0.5*dt*force_new
        return constrain(s_new, pi_new)

    rows = []
    for n in range(steps+1):
        if n % sample_every == 0:
            d = diagnostics(s, pi)
            d.update({"step": n, "time": n*dt})
            rows.append(d)
        if n < steps:
            s, pi = step(s, pi)
            s, pi = s.detach(), pi.detach()

    df = pd.DataFrame(rows)
    df["relative_energy_change"] = (df.E_total-df.E_total.iloc[0])/abs(df.E_total.iloc[0])
    df["Q_drift"] = df.Q_signed-df.Q_signed.iloc[0]
    df.to_csv(out/"covariant_solver_sanity_timeseries.csv", index=False)

    summary = {
        "prototype_type": "Sanity prototype for fully covariant baby-Skyrme Hamiltonian solver",
        "N": N,
        "L": L,
        "dt": dt,
        "steps": steps,
        "kappa": kappa,
        "mu2": mu2,
        "initial_E_total": float(df.E_total.iloc[0]),
        "final_E_total": float(df.E_total.iloc[-1]),
        "relative_energy_change": float(df.relative_energy_change.iloc[-1]),
        "initial_Q_signed": float(df.Q_signed.iloc[0]),
        "final_Q_signed": float(df.Q_signed.iloc[-1]),
        "Q_drift": float(df.Q_signed.iloc[-1]-df.Q_signed.iloc[0]),
        "max_norm_deviation": float(df.max_norm_deviation.max()),
        "max_pi_s_deviation": float(df.max_pi_s_deviation.max()),
        "max_p_s_deviation": float(df.max_p_s_deviation.max()),
        "max_dH_dpi_minus_p": float(df.max_dH_dpi_minus_p.max()),
        "final_max_p_abs": float(df.max_p_abs.iloc[-1]),
        "final_max_pi_abs": float(df.max_pi_abs.iloc[-1]),
    }
    (out/"summary.txt").write_text("\n".join(f"{k}: {v}" for k,v in summary.items()), encoding="utf-8")
    return summary


if __name__ == "__main__":
    summary = run()
    for k,v in summary.items():
        print(f"{k}: {v}")
