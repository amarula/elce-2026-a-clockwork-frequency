import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from plot_style import style_title, style_labels, save, BLUE, RED, GREEN

fig, ax = plt.subplots(figsize=(11.5, 5.6), facecolor="white")
ax.set_facecolor("white")
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color("black")
    spine.set_linewidth(1.2)
ax.grid(True, linestyle=":", color="black", alpha=0.55, linewidth=0.9)
ax.tick_params(axis="both", labelsize=11)

floor = -50
xmax = 750
freqs = np.linspace(0, xmax, 4000)

ax.set_ylim(-50, 0)
ax.set_xlim(0, xmax)
ax.set_xticks([0, 100, 200, 300, 400, 500, 600, 700])

# noise floor
ax.plot(freqs, np.full_like(freqs, floor), color=BLUE, linewidth=2.5)

# Ideal: perfectly sharp edges, exactly 50% duty cycle -> only odd harmonics
ideal = {100: 0, 300: 20 * np.log10(1 / 3), 500: 20 * np.log10(1 / 5), 700: 20 * np.log10(1 / 7)}
for f, level in ideal.items():
    ax.vlines(f, floor, level, color=BLUE, linewidth=3.5)

# Real clock: duty cycle slightly off 50% (even harmonics reappear) + finite
# edge speed (higher harmonics roll off faster than the ideal 1/n envelope).
# Offset a few MHz to the right so the two data sets don't overlap visually.
offset = 8
real = {100: -0.5, 200: -16, 300: -12, 400: -30, 500: -34, 600: -38, 700: -44}
for f, level in real.items():
    ax.vlines(f + offset, floor, level, color=RED, linewidth=3.5)

ann1 = ax.annotate(
    "even harmonics appear\n(duty cycle ≠ 50%)",
    xy=(200 + offset, -16), xytext=(272, -1.5), ha="left", va="top",
    fontsize=10.5, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)
ann2 = ax.annotate(
    "higher harmonics roll off\nfaster (finite edge speed)",
    xy=(500 + offset, -34), xytext=(525, -13), ha="left", va="top",
    fontsize=10.5, fontweight="bold", color=GREEN,
    arrowprops=dict(arrowstyle="->", color=GREEN, linewidth=1.6),
)

legend_handles = [
    mlines.Line2D([], [], color=BLUE, linewidth=3.5, label="Ideal"),
    mlines.Line2D([], [], color=RED, linewidth=3.5, label="Real"),
]
legend = ax.legend(handles=legend_handles, loc="upper right", fontsize=11, frameon=True)

style_title(ax, "100 MHz Clock")
style_labels(ax, "Frequency (MHz)", "Normalized PSD (dB)")

path = "../assets/clock-ideal-vs-real-spectrum.png"
save(fig, path)

# --- Programmatic overlap check -------------------------------------------
from matplotlib.backends.backend_agg import FigureCanvasAgg
canvas = FigureCanvasAgg(fig)
canvas.draw()
renderer = canvas.get_renderer()
inv = ax.transData.inverted()


def text_only_bbox(x, y, s, fontsize, ha, va):
    t = ax.text(x, y, s, ha=ha, va=va, fontsize=fontsize, fontweight="bold")
    canvas.draw()
    bbox = t.get_window_extent(renderer=renderer)
    (x0, y0), (x1, y1) = inv.transform([(bbox.x0, bbox.y0), (bbox.x1, bbox.y1)])
    t.remove()
    return min(x0, x1), max(x0, x1), min(y0, y1), max(y0, y1)


def segment_crosses_column(p0, p1, col_x, col_ymin, col_ymax, tol=1.5):
    x0, y0 = p0
    x1, y1 = p1
    if x1 == x0:
        return abs(col_x - x0) < tol
    t = (col_x - x0) / (x1 - x0)
    if -0.02 <= t <= 1.02:
        y_at = y0 + t * (y1 - y0)
        if col_ymin - tol <= y_at <= col_ymax + tol:
            return True
    return False


tops_all = {**{f: lvl for f, lvl in ideal.items()}, **{f + offset: lvl for f, lvl in real.items()}}

leg_bbox = legend.get_window_extent(renderer=renderer)
(lx0, ly0), (lx1, ly1) = inv.transform([(leg_bbox.x0, leg_bbox.y0), (leg_bbox.x1, leg_bbox.y1)])
lx0, lx1 = min(lx0, lx1), max(lx0, lx1)
ly0, ly1 = min(ly0, ly1), max(ly0, ly1)
print(f"legend data-bbox: x=[{lx0:.1f},{lx1:.1f}] y=[{ly0:.1f},{ly1:.1f}]")
for lx, ltop in tops_all.items():
    if lx0 - 1.5 <= lx <= lx1 + 1.5 and ly1 >= floor and ly0 <= ltop:
        print(f"  !! legend overlaps line at x={lx}")

specs = [
    ("ann1", 272, -1.5, "even harmonics appear\n(duty cycle ≠ 50%)", (200 + offset, -16)),
    ("ann2", 525, -13, "higher harmonics roll off\nfaster (finite edge speed)", (500 + offset, -34)),
]

def point_to_segment_dist(px, py, x0, y0, x1, y1):
    dx, dy = x1 - x0, y1 - y0
    if dx == 0 and dy == 0:
        return ((px - x0) ** 2 + (py - y0) ** 2) ** 0.5
    t = max(0, min(1, ((px - x0) * dx + (py - y0) * dy) / (dx * dx + dy * dy)))
    projx, projy = x0 + t * dx, y0 + t * dy
    return ((px - projx) ** 2 + (py - projy) ** 2) ** 0.5
for name, x, y, s, xy in specs:
    x0, x1, ylo, yhi = text_only_bbox(x, y, s, 10.5, "left", "top")
    print(f"{name} text data-bbox: x=[{x0:.1f},{x1:.1f}] y=[{ylo:.1f},{yhi:.1f}]")
    clean = True
    for lx, ltop in tops_all.items():
        if x0 - 1.5 <= lx <= x1 + 1.5 and yhi >= floor and ylo <= ltop:
            clean = False
            print(f"  !! TEXT overlaps line at x={lx} (line top={ltop:.1f})")
    if not (x1 < lx0 or x0 > lx1 or yhi < ly0 or ylo > ly1):
        clean = False
        print(f"  !! {name} text OVERLAPS legend box")
    for lx, ltop in tops_all.items():
        if abs(lx - xy[0]) < 1:
            continue
        if segment_crosses_column((x, y), xy, lx, floor, ltop):
            clean = False
            print(f"  !! {name} ARROW crosses column at x={lx}")
        # proximity check -- flag if the arrow passes visually close to a
        # column it doesn't target (not just literal overlap)
        min_d = min(
            point_to_segment_dist(lx, sample_y, x, y, xy[0], xy[1])
            for sample_y in np.linspace(floor, ltop, 12)
        )
        if min_d < 15:
            print(f"  ~ {name} arrow passes close ({min_d:.1f} units) to column at x={lx}")
    if x0 < 0 or x1 > xmax or ylo < floor or yhi > 0:
        clean = False
        print(f"  !! {name} text runs OUTSIDE plot bounds (xmax={xmax})")
    if clean:
        print("  OK -- fully clean")

print("check complete")
