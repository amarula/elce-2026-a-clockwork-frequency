import numpy as np
from scipy import signal
from plot_style import new_axes, style_title, style_labels, save, BLUE

fig, ax = new_axes()

f0 = 100e6  # 100 MHz
t = np.linspace(0, 30e-9, 4000)
y = signal.square(2 * np.pi * f0 * t)

ax.plot(t * 1e9, y, color=BLUE, linewidth=3)
ax.set_xlim(0, 30)
ax.set_ylim(-1.3, 1.3)
ax.set_yticks([-1, -0.5, 0, 0.5, 1])

style_title(ax, "100 MHz Clock")
style_labels(ax, "Time (ns)", "Normalized Amplitude")

save(fig, "../assets/square-wave-time-domain.png")
print("done")
