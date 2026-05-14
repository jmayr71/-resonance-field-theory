import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

out = Path("outputs/two_spinor_exchange_test")
out.mkdir(parents=True, exist_ok=True)

N = 220
L = 24.0
dx = L / N
x = np.linspace(-L/2, L/2 - dx, N)
y = np.linspace(-L/2, L/2 - dx, N)
X, Y = np.meshgrid(x, y, indexing="ij")

sigma = 1.15
sep_values = np.linspace(8.0, 0.2, 90)

spinor = np.array([1.0 + 0j, 0.55j])
spinor = spinor / np.sqrt(np.vdot(spinor, spinor).real)


def gaussian_packet(x0, y0, kx=0.0, ky=0.0):
    phase = np.exp(1j * (kx * X + ky * Y))
    env = np.exp(-((X - x0)**2 + (Y - y0)**2) / (2*sigma**2))
    return env * phase


def spinor_packet(x0, y0, kx=0.0, ky=0.0):
    g = gaussian_packet(x0, y0, kx, ky)
    return spinor[0] * g, spinor[1] * g


def density(psi):
    a, b = psi
    return np.abs(a)**2 + np.abs(b)**2


def norm(psi):
    return float(np.sum(density(psi)) * dx * dx)


def normalize(psi):
    n = np.sqrt(norm(psi))
    return psi[0] / n, psi[1] / n


def combine(psi1, psi2, sign=+1):
    a = psi1[0] + sign * psi2[0]
    b = psi1[1] + sign * psi2[1]
    return normalize((a, b))


def overlap(psi1, psi2):
    a1, b1 = psi1
    a2, b2 = psi2
    return complex(np.sum(np.conj(a1)*a2 + np.conj(b1)*b2) * dx * dx)


def center_density(psi, radius=0.8):
    rho = density(psi)
    mask = X**2 + Y**2 <= radius**2
    return float(np.mean(rho[mask]))


def rms_radius(psi):
    rho = density(psi)
    n = np.sum(rho)
    cx = np.sum(X * rho) / n
    cy = np.sum(Y * rho) / n
    r2 = np.sum(((X-cx)**2 + (Y-cy)**2) * rho) / n
    return float(np.sqrt(r2))


def max_density(psi):
    return float(np.max(density(psi)))


rows = []
for sep in sep_values:
    psi_left = normalize(spinor_packet(-sep/2, 0.0))
    psi_right = normalize(spinor_packet(+sep/2, 0.0))
    ov = overlap(psi_left, psi_right)

    psi_sym = combine(psi_left, psi_right, sign=+1)
    psi_asym = combine(psi_left, psi_right, sign=-1)

    rows.append({
        "separation": sep,
        "overlap_abs": abs(ov),
        "overlap_real": ov.real,
        "sym_center_density": center_density(psi_sym),
        "asym_center_density": center_density(psi_asym),
        "sym_radius": rms_radius(psi_sym),
        "asym_radius": rms_radius(psi_asym),
        "sym_max_density": max_density(psi_sym),
        "asym_max_density": max_density(psi_asym),
    })

with (out / "two_spinor_exchange_results.csv").open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

sep_arr = np.array([r["separation"] for r in rows])
overlap_abs = np.array([r["overlap_abs"] for r in rows])
sym_center = np.array([r["sym_center_density"] for r in rows])
asym_center = np.array([r["asym_center_density"] for r in rows])
sym_radius = np.array([r["sym_radius"] for r in rows])
asym_radius = np.array([r["asym_radius"] for r in rows])

plt.figure(figsize=(6,4))
plt.plot(sep_arr, overlap_abs)
plt.gca().invert_xaxis()
plt.title("Overlap of two identical spinor packets")
plt.xlabel("separation")
plt.ylabel("|overlap|")
plt.savefig(out / "overlap_vs_separation.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6,4))
plt.plot(sep_arr, sym_center, label="symmetric")
plt.plot(sep_arr, asym_center, label="antisymmetric")
plt.gca().invert_xaxis()
plt.title("Central density during packet approach")
plt.xlabel("separation")
plt.ylabel("central density")
plt.legend()
plt.savefig(out / "central_density_vs_separation.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6,4))
plt.plot(sep_arr, sym_radius, label="symmetric")
plt.plot(sep_arr, asym_radius, label="antisymmetric")
plt.gca().invert_xaxis()
plt.title("RMS radius during packet approach")
plt.xlabel("separation")
plt.ylabel("RMS radius")
plt.legend()
plt.savefig(out / "radius_vs_separation.png", dpi=170, bbox_inches="tight")
plt.close()

sep_close = float(sep_values[-1])
psi_l = normalize(spinor_packet(-sep_close/2, 0.0))
psi_r = normalize(spinor_packet(+sep_close/2, 0.0))
psi_sym_close = combine(psi_l, psi_r, sign=+1)
psi_asym_close = combine(psi_l, psi_r, sign=-1)

extent = [-L/2, L/2, -L/2, L/2]

plt.figure(figsize=(6,5))
plt.imshow(density(psi_sym_close).T, origin="lower", extent=extent)
plt.title("Symmetric density at closest separation")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="density")
plt.savefig(out / "symmetric_density_close.png", dpi=170, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6,5))
plt.imshow(density(psi_asym_close).T, origin="lower", extent=extent)
plt.title("Antisymmetric density at closest separation")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="density")
plt.savefig(out / "antisymmetric_density_close.png", dpi=170, bbox_inches="tight")
plt.close()

print("Two-spinor exchange test complete.")
print("Closest separation:", sep_close)
print("Symmetric central density:", center_density(psi_sym_close))
print("Antisymmetric central density:", center_density(psi_asym_close))
print("Outputs:", out)
