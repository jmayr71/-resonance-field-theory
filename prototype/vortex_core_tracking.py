"""
Vortex core tracking prototype.

This script extends the 2D resonance-field sandbox with automatic detection of
phase winding defects on plaquettes. It records defect positions over time and
plots the resulting trajectories.
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
dt = 0.004
steps = 2200
sample_every = 20
core = 1.0
sep = 6.0
out = Path("outputs/vortex_core_tracking")
out.mkdir(parents=True, exist_ok=True)


def wrap_phase(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def defect(x0, y0, winding):
    r = np.sqrt((X - x0) ** 2 + (Y - y0) ** 2)
    th = np.arctan2(Y - y0, X - x0)
    return np.tanh(r / core) * np.exp(1j * winding * th)


phi = np.sqrt(rho0) * defect(-sep / 2, 0.0, -1) * defect(sep / 2, 0.0, 1)
phi *= np.exp(-1j * 0.10 * np.abs(X))

edge = np.minimum.reduce([X + L / 2, L / 2 - X, Y + L / 2, L / 2 - Y])
safe = np.clip(edge / 3.0, 0.0, 1.0)
rim = np.where(edge < 3.0, np.sin(0.5 * np.pi * safe) ** 0.05, 1.0)
lin = np.exp(-0.5j * (0.5 * K2) * dt)


def evolve(z):
    z = np.fft.ifft2(np.fft.fft2(z) * lin)
    z = z * np.exp(-1j * g * (np.abs(z) ** 2 - rho0) * dt)
    z = np.fft.ifft2(np.fft.fft2(z) * lin)
    return z * rim


def detect_defects(z, threshold=0.5):
    phase = np.angle(z)
    defects = []
    for i in range(N - 1):
        for j in range(N - 1):
            d1 = wrap_phase(phase[i + 1, j] - phase[i, j])
            d2 = wrap_phase(phase[i + 1, j + 1] - phase[i + 1, j])
            d3 = wrap_phase(phase[i, j + 1] - phase[i + 1, j + 1])
            d4 = wrap_phase(phase[i, j] - phase[i, j + 1])
            winding = (d1 + d2 + d3 + d4) / (2 * np.pi)
            if winding > threshold or winding < -threshold:
                cx = x[i] + dx / 2
                cy = y[j] + dx / 2
                charge = int(np.round(winding))
                defects.append((cx, cy, charge))
    return defects


def energy(z):
    gx = (np.roll(z, -1, axis=0) - np.roll(z, 1, axis=0)) / (2 * dx)
    gy = (np.roll(z, -1, axis=1) - np.roll(z, 1, axis=1)) / (2 * dx)
    dens = 0.5 * (np.abs(gx) ** 2 + np.abs(gy) ** 2) + 0.5 * g * (np.abs(z) ** 2 - rho0) ** 2
    return float(np.sum(dens) * dx * dx)


trajectory = []
energy_history = []
count_history = []

for step in range(steps + 1):
    if step % sample_every == 0:
        defects = detect_defects(phi)
        for cx, cy, charge in defects:
            trajectory.append((step, cx, cy, charge))
        energy_history.append((step, energy(phi)))
        count_history.append((step, len(defects)))
    phi = evolve(phi)

np.savetxt(out / "defect_trajectory.csv", np.array(trajectory), delimiter=",", header="step,x,y,charge", comments="")
np.savetxt(out / "energy.csv", np.array(energy_history), delimiter=",", header="step,energy", comments="")
np.savetxt(out / "defect_count.csv", np.array(count_history), delimiter=",", header="step,count", comments="")

if trajectory:
    arr = np.array(trajectory)
    plt.figure(figsize=(6, 5))
    positive = arr[:, 3] > 0
    negative = arr[:, 3] < 0
    plt.scatter(arr[positive, 1], arr[positive, 2], s=8, label="positive winding")
    plt.scatter(arr[negative, 1], arr[negative, 2], s=8, label="negative winding")
    plt.title("Detected defect positions")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.savefig(out / "defect_positions.png", dpi=170, bbox_inches="tight")
    plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in energy_history], [e for _, e in energy_history])
plt.title("Energy over time")
plt.xlabel("step")
plt.ylabel("energy")
plt.savefig(out / "energy.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in count_history], [c for _, c in count_history])
plt.title("Detected defect count")
plt.xlabel("step")
plt.ylabel("count")
plt.savefig(out / "defect_count.png", dpi=170, bbox_inches="tight")
plt.close()

print("Core tracking prototype complete")
print("Final detected defects:", detect_defects(phi))
print("Output directory:", out)
