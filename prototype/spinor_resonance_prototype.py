"""
Minimal two-component spinor resonance prototype.

This prototype extends the scalar resonance field into a two-component field:

    Psi = (psi_up, psi_down)

The goal is not yet a full Dirac simulation. The purpose is to explore whether
coupled two-component vortex structures can produce stable chiral/spin-like
patterns in the resonance-field sandbox.
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

kx = 2 * np.pi * np.fft.fftfreq(N, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(N, d=dx)
KX, KY = np.meshgrid(kx, ky, indexing="ij")
K2 = KX**2 + KY**2

rho0 = 1.0
g = 1.0
coupling = 0.35
dt = 0.003
steps = 2600
sample_every = 40
core = 1.0
out = Path("outputs/spinor_resonance")
out.mkdir(parents=True, exist_ok=True)


def vortex(winding, shift_x=0.0):
    r = np.sqrt((X - shift_x) ** 2 + Y**2)
    th = np.arctan2(Y, X - shift_x)
    return np.tanh(r / core) * np.exp(1j * winding * th)


psi_up = np.sqrt(rho0) * vortex(-1, -1.0)
psi_down = 0.7 * np.sqrt(rho0) * vortex(+1, +1.0)

edge = np.minimum.reduce([X + L / 2, L / 2 - X, Y + L / 2, L / 2 - Y])
safe = np.clip(edge / 3.0, 0.0, 1.0)
rim = np.where(edge < 3.0, np.sin(0.5 * np.pi * safe) ** 0.05, 1.0)
lin = np.exp(-0.5j * (0.5 * K2) * dt)


def evolve(a, b):
    a = np.fft.ifft2(np.fft.fft2(a) * lin)
    b = np.fft.ifft2(np.fft.fft2(b) * lin)

    density = np.abs(a) ** 2 + np.abs(b) ** 2

    a = a * np.exp(-1j * (g * (density - rho0) + coupling * np.abs(b) ** 2) * dt)
    b = b * np.exp(-1j * (g * (density - rho0) + coupling * np.abs(a) ** 2) * dt)

    mix_a = a + 1j * coupling * b * dt
    mix_b = b + 1j * coupling * a * dt

    a = np.fft.ifft2(np.fft.fft2(mix_a) * lin)
    b = np.fft.ifft2(np.fft.fft2(mix_b) * lin)

    return a * rim, b * rim


def energy(a, b):
    gx1 = (np.roll(a, -1, axis=0) - np.roll(a, 1, axis=0)) / (2 * dx)
    gy1 = (np.roll(a, -1, axis=1) - np.roll(a, 1, axis=1)) / (2 * dx)

    gx2 = (np.roll(b, -1, axis=0) - np.roll(b, 1, axis=0)) / (2 * dx)
    gy2 = (np.roll(b, -1, axis=1) - np.roll(b, 1, axis=1)) / (2 * dx)

    density = np.abs(a) ** 2 + np.abs(b) ** 2

    grad = (
        np.abs(gx1) ** 2
        + np.abs(gy1) ** 2
        + np.abs(gx2) ** 2
        + np.abs(gy2) ** 2
    )

    interaction = 0.5 * g * (density - rho0) ** 2

    return float(np.sum(0.5 * grad + interaction) * dx * dx)


def spin_density(a, b):
    return np.abs(a) ** 2 - np.abs(b) ** 2


energy_history = []
spin_history = []

for step in range(steps + 1):
    if step % sample_every == 0:
        energy_history.append((step, energy(psi_up, psi_down)))
        spin_history.append((step, float(np.mean(spin_density(psi_up, psi_down)))))

    psi_up, psi_down = evolve(psi_up, psi_down)


extent = [-L / 2, L / 2, -L / 2, L / 2]

plt.figure(figsize=(6, 5))
plt.imshow(np.abs(psi_up).T, origin="lower", extent=extent)
plt.title("Spinor component |psi_up|")
plt.colorbar(label="amplitude")
plt.savefig(out / "psi_up.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
plt.imshow(np.abs(psi_down).T, origin="lower", extent=extent)
plt.title("Spinor component |psi_down|")
plt.colorbar(label="amplitude")
plt.savefig(out / "psi_down.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
plt.imshow(spin_density(psi_up, psi_down).T, origin="lower", extent=extent)
plt.title("Effective spin density")
plt.colorbar(label="spin density")
plt.savefig(out / "spin_density.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in energy_history], [v for _, v in energy_history])
plt.title("Energy")
plt.xlabel("step")
plt.ylabel("energy")
plt.savefig(out / "energy.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in spin_history], [v for _, v in spin_history])
plt.title("Average spin density")
plt.xlabel("step")
plt.ylabel("spin density")
plt.savefig(out / "spin_history.png", dpi=170, bbox_inches="tight")
plt.close()

print("Spinor resonance prototype complete")
print("Final energy:", energy(psi_up, psi_down))
print("Final mean spin density:", float(np.mean(spin_density(psi_up, psi_down))))
print("Output directory:", out)
