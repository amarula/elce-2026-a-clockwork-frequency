import numpy as np
import matplotlib.lines as mlines
from plot_style import (
    new_axes, style_title, style_labels, save, BLUE, ORANGE, GRAY, FILL_ALPHA,
    dimension,
)
from plot_05_victim_band import SPREAD_DEPTH_PCT, RBW_MHZ, spread_half_width, reduction_db

fig, ax = new_axes()

floor = -50
f0 = 100  # MHz
# Depth and RBW come from the shared constants, so this chart and the
# full-spectrum ones on the following slides can never drift apart.
half_width = spread_half_width(f0)

freqs = np.linspace(96, 105, 4000)

ax.set_ylim(-50, 5)
ax.set_xlim(96, 105)
ax.set_xticks([96, 97, 98, 99, 100, 101, 102, 103, 104, 105])

# noise floor
ax.plot(freqs, np.full_like(freqs, floor), color=BLUE, linewidth=2.5)

# Non-spread: a single sharp spike at the exact clock frequency
ax.vlines(f0, floor, 0, color=BLUE, linewidth=3.5)

# Spread (SSC): the tone is swept across the band, so the same energy is
# spread over it evenly -- a flat-topped rectangle, not a spike. Total power
# is conserved: the non-spread spike concentrates it in one narrow
# resolution-bandwidth-sized bin, so spreading it over a band `spread_bw`
# wide must drop the level by 10*log10(spread_bw / rbw).
spread_bw = 2 * half_width  # MHz, width of the swept band
edge_peak_db = -reduction_db(f0)
x = (freqs - f0) / half_width
inside = np.abs(x) < 1
spread_db = np.where(inside, edge_peak_db, floor)
spread_db = np.clip(spread_db, floor, 5)
ax.fill_between(freqs, floor, spread_db, where=inside, color=ORANGE,
                alpha=FILL_ALPHA, linewidth=0)
# Outline drawn as an explicit four-point path rather than the whole clipped
# trace, so the band's own colour stops at its edges instead of running along
# the blue noise floor. Same idiom as the two victim-band charts. Same hex as
# the fill at full strength: the outline is the fill's bold, not a second colour.
ax.plot([f0 - half_width, f0 - half_width, f0 + half_width, f0 + half_width],
        [floor, edge_peak_db, edge_peak_db, floor], color=ORANGE, linewidth=2.8)

# "Reduction in spectral amplitude" annotation, matching the reference figure.
# Neutral gray, not green: this is a measurement of how far the peak dropped,
# not a verdict on anybody's compliance.
ax.plot([f0, f0 + half_width], [0, 0], color=GRAY, linestyle="--", linewidth=1.4)
ax.plot([f0, f0 + half_width], [edge_peak_db, edge_peak_db], color=GRAY, linestyle="--", linewidth=1.4)
dimension(ax, (f0 + half_width, 0), (f0 + half_width, edge_peak_db),
          color=GRAY, linewidth=1.6)
ax.text(f0 + half_width + 0.15, edge_peak_db / 2, "reduction in\nspectral amplitude",
        ha="left", va="center", fontsize=10.5, fontweight="bold", color=GRAY)

legend_handles = [
    mlines.Line2D([], [], color=BLUE, linewidth=3.5, label="Non-spread"),
    mlines.Line2D([], [], color=ORANGE, linewidth=3.5, label="Spread (SSC)"),
]
ax.legend(handles=legend_handles, loc="upper left", fontsize=11, frameon=True)

style_title(ax, "100 MHz Clock")
style_labels(ax, "Frequency (MHz)", "Normalized PSD (dB)")

path = "../assets/ssc-spread-spectrum.png"
save(fig, path)
print("done")
