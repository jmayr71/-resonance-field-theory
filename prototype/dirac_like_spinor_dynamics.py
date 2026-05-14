"""
Minimal Dirac-like spinor dynamics prototype.

This prototype introduces explicit Pauli-matrix-style coupling between two
spinor components in order to approximate relativistic/chiral propagation
patterns on a discrete resonance field.

The goal is exploratory only.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

N = 192
L = 24.0
dx = L / N
x = np.linspace(-L / 2, L / 2 - dx, N)
y = np.linspace(-L / 2, L / 2 - dx, N)
X, Y = np.meshgrid(x, y, indexing="ij")

mass = 0.4
c = 1.0
dt = 0.0015
steps = 2600
sample_every = 20
out = Path("outputs/dirac_like_spinor")
out.mkdir(parents=True, exist_ok=True)


# Initial localized packet
sigma = 1.2
k0 = 2.5
packet = np.exp(-(X**2 + Y**2) / (2 * sigma**2)) * np.exp(1j * k0 * X)

psi_up = packet.copy()
psi_down = 0.3j * packet.copy()


edge = np.minimum.reduce([X + L / 2, L / 2 - X, Y + L / 2, L / 2 - Y])
safe = np.clip(edge / 3.0, 0.0, 1.0)
rim = np.where(edge < 3.0, np.sin(0.5 * np.pi * safe) ** 0.05, 1.0)


def ddx(z):
    return (np.roll(z, -1, axis=0) - np.roll(z, 1, axis=0)) / (2 * dx)


def ddy(z):
    return (np.roll(z, -1, axis=1) - np.roll(z, 1, axis=1)) / (2 * dx)


# Dirac-like coupling using Pauli structure
# i dPsi/dt = (-i c sigma_x d/dx - i c sigma_y d/dy + m sigma_z) Psi


def evolve(a, b):
    dax = ddx(a)
    day = ddy(a)
    dbx = ddx(b)
    dby = ddy(b)

    rhs_a = -c * (dbx - 1j * dby) + mass * a
    rhs_b = -c * (dax + 1j * day) - mass * b

    new_a = a - 1j * dt * rhs_a
    new_b = b - 1j * dt * rhs_b

    return new_a * rim, new_b * rim


# Diagnostics

def density(a, b):
    return np.abs(a) ** 2 + np.abs(b) ** 2


# sigma_z expectation analogue

def chirality(a, b):
    return np.abs(a) ** 2 - np.abs(b) ** 2


# approximate probability current

def current_x(a, b):
    return 2 * np.real(np.conj(a) * b)


# center of packet

def center_of_mass(rho):
    norm = np.sum(rho)
    cx = np.sum(X * rho) / norm
    cy = np.sum(Y * rho) / norm
    return float(cx), float(cy)


energy_history = []
chirality_history = []
trajectory = []

for step in range(steps + 1):
    if step % sample_every == 0:
        rho = density(psi_up, psi_down)
        energy_est = float(np.sum(rho) * dx * dx)
        energy_history.append((step, energy_est))
        chirality_history.append((step, float(np.mean(chirality(psi_up, psi_down)))))
        trajectory.append((step, *center_of_mass(rho)))

    psi_up, psi_down = evolve(psi_up, psi_down)


extent = [-L / 2, L / 2, -L / 2, L / 2]

plt.figure(figsize=(6, 5))
plt.imshow(density(psi_up, psi_down).T, origin="lower", extent=extent)
plt.title("Final spinor density")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="density")
plt.savefig(out / "density.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
plt.imshow(chirality(psi_up, psi_down).T, origin="lower", extent=extent)
plt.title("Chirality-like density")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="chirality")
plt.savefig(out / "chirality.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
plt.imshow(current_x(psi_up, psi_down).T, origin="lower", extent=extent)
plt.title("Approximate current density Jx")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="Jx")
plt.savefig(out / "current_x.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in energy_history], [v for _, v in energy_history])
plt.title("Integrated density")
plt.xlabel("step")
plt.ylabel("norm")
plt.savefig(out / "norm.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in chirality_history], [v for _, v in chirality_history])
plt.title("Average chirality")
plt.xlabel("step")
plt.ylabel("chirality")
plt.savefig(out / "chirality_history.png", dpi=170, bbox_inches="tight")
plt.close()

traj = np.array(trajectory)
plt.figure(figsize=(6, 5))
plt.plot(traj[:, 1], traj[:, 2])
plt.title("Wave packet trajectory")
plt.xlabel("x")
plt.ylabel("y")
plt.savefig(out / "trajectory.png", dpi=170, bbox_inches="tight")
plt.close()

np.savetxt(out / "trajectory.csv", traj, delimiter=",", header="step,x,y", comments="")

print("Dirac-like spinor prototype complete")
print("Final packet center:", center_of_mass(density(psi_up, psi_down)))
print("Final mean chirality:", float(np.mean(chirality(psi_up, psi_down))))
print("Output directory:", out)
