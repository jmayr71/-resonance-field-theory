import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

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
core = 1.0
sep = 6.0
out = Path("outputs/vortex_pair_dynamics")
out.mkdir(parents=True, exist_ok=True)


def defect(x0, y0, n):
    r = np.sqrt((X - x0) ** 2 + (Y - y0) ** 2)
    th = np.arctan2(Y - y0, X - x0)
    return np.tanh(r / core) * np.exp(1j * n * th)


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


def energy(z):
    gx = (np.roll(z, -1, axis=0) - np.roll(z, 1, axis=0)) / (2 * dx)
    gy = (np.roll(z, -1, axis=1) - np.roll(z, 1, axis=1)) / (2 * dx)
    dens = 0.5 * (np.abs(gx) ** 2 + np.abs(gy) ** 2) + 0.5 * g * (np.abs(z) ** 2 - rho0) ** 2
    return float(np.sum(dens) * dx * dx)


def winding(z, cx, cy, radius):
    a = np.linspace(-np.pi, np.pi, 720, endpoint=False)
    xs = cx + radius * np.cos(a)
    ys = cy + radius * np.sin(a)
    ix = np.clip(((xs + L / 2) / dx).astype(int), 0, N - 1)
    iy = np.clip(((ys + L / 2) / dx).astype(int), 0, N - 1)
    p = np.unwrap(np.angle(z[ix, iy]))
    return float((p[-1] - p[0]) / (2 * np.pi))


hist_e = []
hist_w = []
for step in range(steps + 1):
    if step % 40 == 0:
        hist_e.append((step, energy(phi)))
        hist_w.append((step, winding(phi, 0.0, 0.0, 7.0)))
    phi = evolve(phi)

extent = [-L / 2, L / 2, -L / 2, L / 2]
plt.figure(figsize=(6, 5))
plt.imshow(np.abs(phi).T, origin="lower", extent=extent)
plt.title("Final amplitude |phi|")
plt.colorbar(label="|phi|")
plt.savefig(out / "final_amplitude.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 5))
plt.imshow(np.angle(phi).T, origin="lower", extent=extent)
plt.title("Final phase arg(phi)")
plt.colorbar(label="phase")
plt.savefig(out / "final_phase.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in hist_e], [v for _, v in hist_e])
plt.title("Energy")
plt.xlabel("step")
plt.ylabel("energy")
plt.savefig(out / "energy.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 4))
plt.plot([s for s, _ in hist_w], [v for _, v in hist_w])
plt.title("Net winding around pair")
plt.xlabel("step")
plt.ylabel("winding")
plt.savefig(out / "net_winding.png", dpi=170, bbox_inches="tight")
plt.close()

print("Prototype complete")
print("Final energy:", energy(phi))
print("Final net winding:", winding(phi, 0.0, 0.0, 7.0))
print("Output directory:", out)
