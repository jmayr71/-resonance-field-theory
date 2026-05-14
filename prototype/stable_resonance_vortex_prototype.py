import numpy as np
import matplotlib.pyplot as plt

N = 192
L = 24.0
dx = L / N
x = np.linspace(-L/2, L/2 - dx, N)
y = np.linspace(-L/2, L/2 - dx, N)
X, Y = np.meshgrid(x, y, indexing="ij")
R = np.sqrt(X**2 + Y**2)
Theta = np.arctan2(Y, X)

kx = 2 * np.pi * np.fft.fftfreq(N, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(N, d=dx)
KX, KY = np.meshgrid(kx, ky, indexing="ij")
K2 = KX**2 + KY**2

winding = -1
core_size = 1.0
rho0 = 1.0
g = 1.0
dt = 0.005
steps = 2400

phi = np.sqrt(rho0) * np.tanh(R / core_size) * np.exp(1j * winding * Theta)
phi[N//2, N//2] = 0.0

rim_width = 3.0
edge_dist = np.minimum.reduce([X + L/2, L/2 - X, Y + L/2, L/2 - Y])
rim = np.where(edge_dist < rim_width, np.sin(0.5*np.pi*edge_dist/rim_width)**0.05, 1.0)
rim = np.clip(rim, 0.0, 1.0)

linear_half_step = np.exp(-0.5j * (0.5 * K2) * dt)

def evolve_split_step(phi):
    phik = np.fft.fft2(phi)
    phi = np.fft.ifft2(phik * linear_half_step)
    phi = phi * np.exp(-1j * g * (np.abs(phi)**2 - rho0) * dt)
    phik = np.fft.fft2(phi)
    phi = np.fft.ifft2(phik * linear_half_step)
    return phi * rim

def energy(phi):
    grad_x = (np.roll(phi, -1, axis=0) - np.roll(phi, 1, axis=0)) / (2 * dx)
    grad_y = (np.roll(phi, -1, axis=1) - np.roll(phi, 1, axis=1)) / (2 * dx)
    density = 0.5*(np.abs(grad_x)**2 + np.abs(grad_y)**2) + 0.5*g*(np.abs(phi)**2-rho0)**2
    return float(np.sum(density) * dx * dx)

def winding_number_around_center(phi, radius=3.5):
    samples = 720
    angles = np.linspace(-np.pi, np.pi, samples, endpoint=False)
    xs = radius * np.cos(angles)
    ys = radius * np.sin(angles)
    ix = np.clip(((xs + L/2) / dx).astype(int), 0, N-1)
    iy = np.clip(((ys + L/2) / dx).astype(int), 0, N-1)
    phases = np.angle(phi[ix, iy])
    unwrapped = np.unwrap(phases)
    return float((unwrapped[-1] - unwrapped[0]) / (2*np.pi))

energies = []
windings = []

for step in range(steps + 1):
    if step % 40 == 0:
        energies.append((step, energy(phi)))
        windings.append((step, winding_number_around_center(phi)))
    phi = evolve_split_step(phi)

print("Final energy:", energy(phi))
print("Final winding:", winding_number_around_center(phi))

plt.figure(figsize=(6, 5))
plt.imshow(np.abs(phi).T, origin="lower", extent=[-L/2, L/2, -L/2, L/2])
plt.title("Final amplitude |phi|")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="|phi|")
plt.show()

plt.figure(figsize=(6, 5))
plt.imshow(np.angle(phi).T, origin="lower", extent=[-L/2, L/2, -L/2, L/2])
plt.title("Final phase arg(phi)")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar(label="phase")
plt.show()

plt.figure(figsize=(6, 4))
plt.plot([s for s,_ in energies], [e for _,e in energies])
plt.title("Energy over simulation steps")
plt.xlabel("step")
plt.ylabel("energy")
plt.show()

plt.figure(figsize=(6, 4))
plt.plot([s for s,_ in windings], [w for _,w in windings])
plt.title("Approximate winding number around center")
plt.xlabel("step")
plt.ylabel("winding number")
plt.show()
