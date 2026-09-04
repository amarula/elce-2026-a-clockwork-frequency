import numpy as np
from plot_style import new_axes, style_title, style_labels, save, BLUE, GREEN

fig, ax = new_axes()

f0 = 100
floor = -50
freqs = np.linspace(0, 520, 4000)

ax.set_ylim(-50, 0)
ax.set_xlim(0, 520)
ax.set_xticks([0, 100, 200, 300, 400, 500])

# noise floor
ax.plot(freqs, np.full_like(freqs, floor), color=BLUE, linewidth=2.5)

# ideal square wave: only odd harmonics, amplitude 1/n -> power 20*log10(1/n) dB
harmonics = [1, 3, 5]  # 100, 300, 500 MHz all fall inside the 0-500 MHz window
for n in harmonics:
    level = 20 * np.log10(1.0 / n)
    ax.vlines(f0 * n, floor, level, color=BLUE, linewidth=3.5)

ax.annotate(
    "fundamental",
    xy=(f0, 0), xytext=(f0 + 40, -6),
    fontsize=11, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)
ax.annotate(
    "3rd harmonic\n(weaker)",
    xy=(300, 20 * np.log10(1 / 3)), xytext=(330, -20),
    fontsize=11, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)
ax.annotate(
    "5th harmonic\n(weaker still)",
    xy=(500, 20 * np.log10(1 / 5)), xytext=(370, -32), ha="center",
    fontsize=11, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)
ax.annotate(
    "no even harmonics\nat 200, 400... MHz",
    xy=(200, floor), xytext=(200, -38), ha="center",
    fontsize=11, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)

style_title(ax, "100 MHz Clock")
style_labels(ax, "Frequency (MHz)", "Normalized PSD (dB)")

save(fig, "../assets/square-wave-spectrum.png")
print("done")
