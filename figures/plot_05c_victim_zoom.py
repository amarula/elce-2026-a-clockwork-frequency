import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from plot_style import (
    style_title, style_labels, save, BLUE, ORANGE, RED, GREEN, MAGENTA, FILL_ALPHA,
)
from plot_05_victim_band import (
    dimension_line, DEVICE_B, THRESHOLD, FLOOR, spread_half_width, reduction_db,
)

# This slide answers one question: does the spread band reach into a device that
# was previously unaffected? Only Device B is relevant -- Device A was already
# sitting on the non-spread line, so it adds nothing here and its 85-115 MHz
# span would force a window wide enough to shrink the overlap to nothing.
#
# Dropping it lets the window close to 24 MHz and makes the overlap ~4% of the
# chart, with no change to the band definitions used on the other slides.
F0 = 100
DEVICE_B_LO, DEVICE_B_HI = DEVICE_B

fig, ax = plt.subplots(figsize=(12.5, 6.7), facecolor="white")
ax.set_facecolor("white")
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color("black")
    spine.set_linewidth(1.2)
ax.grid(True, linestyle=":", color="black", alpha=0.55, linewidth=0.9)
ax.tick_params(axis="both", labelsize=11)

xmin, xmax = 96, 120
ymax = 14
ax.set_xlim(xmin, xmax)
ax.set_ylim(FLOOR, ymax)
ax.set_xticks([96, 100, 104, 108, 112, 116, 120])

freqs = np.linspace(xmin, xmax, 2000)
ax.plot(freqs, np.full_like(freqs, FLOOR), color=BLUE, linewidth=2.5)

# Same visual language as the "What is it" chart, so the two figures read as a
# pair: non-spread is a solid blue line, spread is an orange band.
hw = spread_half_width(F0)
level = 0 - reduction_db(F0)
overlap_lo, overlap_hi = DEVICE_B_LO, F0 + hw
# The fill stops where the sliver starts instead of running underneath it: two
# translucent fills stacked would blend into a third colour that means nothing.
# The outline still spans the whole band, so it reads as one object with an
# inset region rather than two separate bands.
band = np.linspace(F0 - hw, overlap_lo, 400)
ax.fill_between(band, FLOOR, level, color=ORANGE, alpha=FILL_ALPHA, linewidth=0)
ax.plot([F0 - hw, F0 - hw, F0 + hw, F0 + hw], [FLOOR, level, level, FLOOR],
        color=ORANGE, linewidth=2.8)

# The non-spread clock: one line at f0 carrying the whole harmonic inside a
# single RBW bin, so it reaches the full 0 dB -- above the emission limit, which
# is where slide 9 started. The height difference *is* the peak reduction.
ax.vlines(F0, FLOOR, 0, color=BLUE, linewidth=3.5)

# Device B: at this scale the whole dimension line fits -- both caps, the arrow
# and both frequency labels, exactly as on the previous slides.
dimension_line(ax, DEVICE_B_LO, DEVICE_B_HI, 8, "Device B", GREEN)

# The slice of spread energy that now falls inside Device B's band. Same
# fill/outline discipline as the band: one hex, translucent fill, bold outline.
ax.fill_between([overlap_lo, overlap_hi], FLOOR, level,
                color=MAGENTA, alpha=FILL_ALPHA, linewidth=0)
ax.plot([overlap_lo, overlap_lo, overlap_hi, overlap_hi],
        [FLOOR, level, level, FLOOR], color=MAGENTA, linewidth=2.8)
# No callout text: the magenta block inside the orange band already shows the
# overlap, and the legend names it. The colours carry the message.

# EMC / victim emission threshold
ax.axhline(THRESHOLD, color=RED, linestyle="--", linewidth=2)
ax.text(xmax - 0.2, THRESHOLD + 1.0, "emission limit", ha="right", va="bottom",
        fontsize=10.5, fontweight="bold", color=RED)

# Legend built exactly like the "What is it" chart's, with the overlap added.
legend_handles = [
    mlines.Line2D([], [], color=BLUE, linewidth=3.5, label="Non-spread"),
    mlines.Line2D([], [], color=ORANGE, linewidth=3.5, label="Spread (SSC)"),
    mlines.Line2D([], [], color=MAGENTA, linewidth=3.5, label="Inside Device B"),
]
ax.legend(handles=legend_handles, loc="upper left", fontsize=11, frameon=True)

style_title(ax, "100 MHz Clock — Zoom on Device B")
style_labels(ax, "Frequency (MHz)", "Normalized PSD (dB)")

path = "../assets/victim-band-zoom.png"
save(fig, path)
print("saved", path)
print(f"window {xmax-xmin} MHz | band {F0-hw}-{F0+hw} | overlap {overlap_lo}-{overlap_hi} "
      f"= {(overlap_hi-overlap_lo)/(xmax-xmin):.1%} of window")
