import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from plot_style import BLUE, RED, GRAY

fig, ax = plt.subplots(figsize=(12, 5.4), facecolor="white")
ax.set_facecolor("white")
ax.set_xlim(0, 12)
ax.set_ylim(0, 5.4)
ax.axis("off")

# --- Clock chip -----------------------------------------------------------
chip = mpatches.FancyBboxPatch(
    (0.6, 2.1), 1.6, 1.2, boxstyle="round,pad=0.08,rounding_size=0.08",
    facecolor="#e8e8e8", edgecolor=GRAY, linewidth=1.6,
)
ax.add_patch(chip)
ax.text(1.4, 3.0, "Clock", ha="center", va="center", fontsize=13, fontweight="bold")

# small square-wave glyph inside the chip
t = np.linspace(0, 1.1, 400)
sq = 2.35 + 0.16 * np.sign(np.sin(2 * np.pi * 4 * t))
ax.plot(0.75 + t, sq, color=BLUE, linewidth=1.6)

# --- PCB trace acting as an unintentional antenna --------------------------
trace_y = 2.7
ax.plot([2.2, 5.4], [trace_y, trace_y], color=BLUE, linewidth=3.5, solid_capstyle="round")
ax.text(3.8, trace_y + 0.45, "PCB trace", ha="center", va="bottom",
        fontsize=12, fontweight="bold", color=BLUE)

# --- Radiated emission: concentric arcs fading outward ---------------------
radiation_origin = (5.4, trace_y)
for i, r in enumerate([0.5, 0.95, 1.4, 1.85, 2.3]):
    arc = mpatches.Arc(
        radiation_origin, 2 * r, 2 * r, angle=0, theta1=-45, theta2=45,
        color=BLUE, linewidth=2.2, alpha=max(0.15, 0.85 - i * 0.16),
    )
    ax.add_patch(arc)

ax.text(6.7, 4.05, "radiated energy", ha="center", va="bottom",
        fontsize=12, fontweight="bold", color=BLUE)

# --- Nearby (victim) device ------------------------------------------------
device = mpatches.FancyBboxPatch(
    (9.6, 2.05), 1.8, 1.3, boxstyle="round,pad=0.08,rounding_size=0.08",
    facecolor="#e8e8e8", edgecolor=RED, linewidth=1.6,
)
ax.add_patch(device)
ax.text(10.5, 2.7, "Nearby\ndevice", ha="center", va="center", fontsize=12, fontweight="bold")

# "disturbed" spark above the device
spark_x, spark_y = 10.5, 3.75
spark = np.array([
    [0, 0.42], [0.11, 0.12], [0.30, 0.12], [0.08, -0.18],
    [0.18, -0.45], [-0.20, -0.05], [-0.02, -0.05], [-0.22, 0.30],
])
ax.fill(spark_x + spark[:, 0] * 0.9, spark_y + spark[:, 1] * 0.9,
        color=RED, linewidth=0)
ax.text(10.5, 4.55, "disturbed!", ha="center", va="bottom",
        fontsize=12, fontweight="bold", color=RED)

# connecting arrow from radiated energy toward the device
ax.annotate("", xy=(9.5, trace_y), xytext=(7.9, trace_y),
            arrowprops=dict(arrowstyle="->", color=BLUE, linewidth=1.8))

path = "../assets/antenna-radiation-diagram.png"
fig.tight_layout()
fig.savefig(path, dpi=150, facecolor="white")
print("done")
