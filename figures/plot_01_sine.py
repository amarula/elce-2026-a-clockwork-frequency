import numpy as np
from plot_style import new_axes, style_title, style_labels, save, BLUE, GREEN

fig, ax = new_axes()

f0 = 100  # MHz -- same fundamental used later for the harmonics figure
freqs = np.linspace(0, 520, 4000)
floor = -50

ax.set_ylim(-50, 0)
ax.set_xlim(0, 520)
ax.set_xticks([0, 100, 200, 300, 400, 500])

# noise floor
ax.plot(freqs, np.full_like(freqs, floor), color=BLUE, linewidth=2.5)
# single spectral line at f0
ax.vlines(f0, floor, 0, color=BLUE, linewidth=3.5)

ax.annotate(
    "all energy at 100 MHz",
    xy=(f0, 0), xytext=(f0 + 40, -12),
    fontsize=11, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)
ax.annotate(
    "no energy at 200, 300, 400, 500... MHz",
    xy=(320, floor), xytext=(175, -34),
    fontsize=11, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)

style_title(ax, "100 MHz Sine Wave")
style_labels(ax, "Frequency (MHz)", "Normalized PSD (dB)")

save(fig, "../assets/sine-wave-single-frequency.png")
print("done")
