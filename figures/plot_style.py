"""Shared MATLAB-like plot style for the SSC talk figures, matching the
reference screenshots (Nonspread vs Spread Spectra / Triangular Spreading
Profile): white background, boxed black axes, dotted grid, bold labels,
thick classic-MATLAB-palette lines.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# One meaning per role, declared once. Scripts import these -- they must not
# re-declare hex values, which is how three slightly different reds and two
# greens crept in before.
#
# The palette is chosen for colour-vision deficiency, not just for looks. The
# pair that carries the whole argument is BLUE vs ORANGE (SSC off vs on), so it
# is the pair that must survive every deficiency: dE 191 in normal vision and
# still 78 under tritanopia, where the teal this replaced fell to 36 and
# collapsed into both BLUE and GREEN. Blue-vs-orange is the Okabe-Ito
# CVD-safe contrast; do not "improve" it towards a green or a cyan.
BLUE = "#0000EE"     # the clock's spectrum, SSC off
ORANGE = "#E69F00"   # the clock's spectrum, SSC on
RED = "#CC0000"      # the emission limit, and the fail mark
GREEN = "#1C7A1C"    # a victim device's band, the check mark, the PASS badge
MAGENTA = "#8E1A6B"  # the newly-overlapped sliver on the zoom chart

# Neutral colour for measurement callouts that assert nothing about
# pass/fail -- e.g. the "reduction in spectral amplitude" dimension arrow.
GRAY = "#444444"

# Filled bands are the role's own colour at this alpha, outlined in the *same*
# hex at full strength -- regular and bold of one colour, never two colours.
# Anything below ~0.4 washes the fill out until it reads as a second, unrelated
# colour, which is the effect this constant exists to prevent.
FILL_ALPHA = 0.45

FIGSIZE = (7.2, 5.4)


def new_axes():
    fig, ax = plt.subplots(figsize=FIGSIZE, facecolor="white")
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.2)
    ax.grid(True, linestyle=":", color="black", alpha=0.55, linewidth=0.9)
    ax.tick_params(axis="both", labelsize=11)
    return fig, ax


def style_title(ax, text):
    ax.set_title(text, fontsize=15, fontweight="bold", pad=12)


def style_labels(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel, fontsize=12, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=12, fontweight="bold")


def dimension(ax, xy_from, xy_to, color=GRAY, linewidth=1.4, cap=0.6):
    """The deck's one and only way to draw a measurement.

    An engineering dimension line: perpendicular tick caps at both ends and a
    double-headed arrow spanning between them. This is the ISO/ASME form --
    arrows *inside* the span pointing out at the extension lines. Arrows placed
    outside a span pointing inwards are the fallback for dimensions too narrow to
    hold their own arrowheads, and nothing in this deck is that narrow, so it is
    not used anywhere.

    Both patches are drawn in display space via arrowstyle, so caps and heads
    come out the same visual size on every chart regardless of its data range --
    which is the whole point of having one helper rather than per-axes constants.

    Works in either orientation: pass the two endpoints of whatever is measured.
    """
    for style in (f"|-|,widthA={cap},widthB={cap}", "<->"):
        ax.annotate("", xy=xy_to, xytext=xy_from,
                    arrowprops=dict(arrowstyle=style, color=color,
                                    linewidth=linewidth, shrinkA=0, shrinkB=0))


def save(fig, path):
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor="white")
    plt.close(fig)
