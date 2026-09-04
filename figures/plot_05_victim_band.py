import numpy as np
import matplotlib.pyplot as plt
from plot_style import (
    style_title, style_labels, save, BLUE, ORANGE, RED, GREEN, FILL_ALPHA,
    dimension as plot_dimension,
)

BASE_HARMONICS = {100: 0, 200: -16, 300: 20 * np.log10(1 / 3), 400: -30, 500: 20 * np.log10(1 / 5)}

# The emission limit, chosen so the fundamental fails before SSC and clears
# after, and so does one harmonic -- two failing peaks make the "before" chart
# tell a richer story than one. It is pinned by SPREAD_DEPTH_PCT below: a
# shallower spread would not drop the fundamental far enough to clear it.
THRESHOLD = -12

# The depth these *conceptual* charts are drawn at.
#
# Deliberately NOT the depth slide 14 quotes. Slides 9-12 argue about what
# spreading does -- a spike becomes a band, the band clears the limit, the band
# reaches a neighbour -- and none of them names a number on screen. Their depth
# is therefore chosen for legibility: at +/-2% the bands are wide enough to read
# as bands on a 620 MHz axis and the newly-overlapped sliver on slide 12 is
# visible. At the realistic +/-0.5% every one of those pictures collapses into a
# hairline and the slides stop showing what they exist to show.
#
# Slide 14 is the one that puts the parameters on screen, so it carries a
# realistic value instead; see DEPTH_PCT in plot_08. Both call the same
# spread_half_width()/reduction_db() with their own depth, so there is still one
# formula behind every number in the deck -- just two illustrative settings.
SPREAD_DEPTH_PCT = 0.02

# Device B carries the "A New Issue ?" slide: its lower edge must sit clear of
# the bare 100 MHz line but inside the spread band, which reaches 102 here.
# 101 leaves the newly overlapped sliver at a quarter of the band.
DEVICE_B = (101, 118)
RBW_MHZ = 0.15  # nominal resolution bandwidth of the reference (non-spread) line
FLOOR = -60
YMAX = 30


def spread_half_width(f, depth_pct=SPREAD_DEPTH_PCT):
    """Half-width of the spread band around harmonic `f`.

    The n-th harmonic tracks the fundamental's modulation, so its absolute
    deviation is n times larger -- which is why the bands get wider as we go up.

    `depth_pct` defaults to the conceptual slides' setting; slide 14 passes its
    own so both derive from this one formula rather than from two copies of it.
    """
    return depth_pct * f


def reduction_db(f, depth_pct=SPREAD_DEPTH_PCT):
    """Peak reduction at harmonic `f`, from conservation of energy.

    The non-spread line concentrates the harmonic's power inside one
    resolution-bandwidth-sized bin; spreading it over `2 * half_width` drops the
    measured level by 10*log10(spread bandwidth / RBW). Because the band widens
    with harmonic number, higher harmonics benefit *more* from SSC.
    """
    return 10 * np.log10(2 * spread_half_width(f, depth_pct) / RBW_MHZ)


def dimension_line(ax, lo, hi, y, label, color, label_at=None, numbers=True,
                   runs_off_to=None):
    """A victim device's operating band, drawn as a standard dimension line.

    `plot_style.dimension` draws the measurement itself -- tick caps at both
    edges and a double-headed arrow between them, the same idiom every other
    measured span in the deck uses. On top of that this adds a pass/fail-marked
    label above and the two boundary frequencies under the ticks.

    An earlier version put the arrows *outside* the span pointing inwards. That
    is the engineering-drawing fallback for spans too narrow to contain their own
    arrowheads; none of these are, and mixing the two forms across slides made
    the deck look like it had two different notations for one thing.

    `runs_off_to` is the other standard variant: when the far edge lies outside
    the visible window, give the x to run to and the dimension gets one tick cap
    and a single arrowhead trailing off the view, instead of a false second edge.
    """
    if runs_off_to is None:
        plot_dimension(ax, (lo, y), (hi, y), color=color, linewidth=1.6)
        centre, edges = (lo + hi) / 2, (lo, hi)
    else:
        ax.plot([lo, lo], [y - 1.8, y + 1.8], color=color, linewidth=1.6)
        ax.annotate("", xy=(runs_off_to, y), xytext=(lo, y),
                    arrowprops=dict(arrowstyle="->", color=color, linewidth=1.6,
                                    shrinkA=0, shrinkB=0))
        centre, edges = (lo + runs_off_to) / 2, (lo,)

    mark = "✔" if color == GREEN else "✘"
    ax.text(label_at if label_at is not None else centre, y + 2.6,
            f"{mark} {label}", ha="center", va="bottom",
            fontsize=12, fontweight="bold", color=color)
    # Boundary frequencies sit just *outside* their own tick rather than centred
    # under it. Centred works only while the span is wide enough to hold both
    # labels: Device B is 17.8 MHz on a 620 MHz axis, where "100.2" and "118"
    # ran into each other and printed as "100.2118". Offsets are in points, so
    # this holds on the zoomed chart too.
    if numbers:
        for x, ha, dx in zip(edges, ("right", "left"), (-3, 3)):
            ax.annotate(f"{x:g}", xy=(x, y - 2.0), xytext=(dx, 0),
                        textcoords="offset points", ha=ha, va="top",
                        fontsize=8.5, fontweight="bold", color=color)


def render(ssc_enabled, out_path):
    fig, ax = plt.subplots(figsize=(12.5, 6.7), facecolor="white")
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.2)
    ax.grid(True, linestyle=":", color="black", alpha=0.55, linewidth=0.9)
    ax.tick_params(axis="both", labelsize=11)

    xmax = 620
    freqs = np.linspace(0, xmax, 4000)

    ax.set_ylim(FLOOR, YMAX)
    ax.set_xlim(0, xmax)
    ax.set_xticks([0, 100, 200, 300, 400, 500, 600])

    # noise floor
    ax.plot(freqs, np.full_like(freqs, FLOOR), color=BLUE, linewidth=2.5)

    harmonics = {}
    for f, base_level in BASE_HARMONICS.items():
        harmonics[f] = base_level - (reduction_db(f) if ssc_enabled else 0.0)

    for f, level in harmonics.items():
        if ssc_enabled:
            # SSC doesn't just lower the peak -- it spreads that same energy
            # across a band around each harmonic, wider for higher harmonics.
            # Orange, matching the "What is it" and zoom charts: blue is the
            # clock without SSC, orange is the same clock with it on.
            hw = spread_half_width(f)
            band = np.linspace(f - hw, f + hw, 200)
            ax.fill_between(band, FLOOR, level, color=ORANGE,
                            alpha=FILL_ALPHA, linewidth=0)
            ax.plot([f - hw, f - hw, f + hw, f + hw], [FLOOR, level, level, FLOOR],
                    color=ORANGE, linewidth=2.2)
        else:
            ax.vlines(f, FLOOR, level, color=BLUE, linewidth=3.5)

    # EMC / victim emission threshold -- dashed horizontal line
    ax.axhline(THRESHOLD, color=RED, linestyle="--", linewidth=2)
    ax.text(xmax - 10, THRESHOLD + 1.2, "emission limit", ha="right", va="bottom",
            fontsize=10.5, fontweight="bold", color=RED)

    # Pass/fail mark for each peak -- a check if it's under the emission
    # limit, a cross if it exceeds it. Drawn as a clean row well above the
    # device-band annotations, directly over each peak's own frequency.
    for f, level in harmonics.items():
        ok = level <= THRESHOLD
        mark = "✔" if ok else "✘"
        color = GREEN if ok else RED
        ax.text(f, 26, mark, ha="center", va="center",
                fontsize=22, fontweight="bold", color=color)

    # Five victim devices -- their operating bands, civil-drawing style.
    # Red = disturbed (a peak inside the band exceeds the emission limit).
    # Green = not disturbed (either clean, or in-band but under the limit).
    # Device B's lower edge sits just above 100 MHz: clear of the non-spread
    # line, but inside the band once SSC spreads the fundamental.
    a_color = GREEN if harmonics[100] <= THRESHOLD else RED
    c_color = GREEN if harmonics[300] <= THRESHOLD else RED
    e_color = GREEN if harmonics[500] <= THRESHOLD else RED
    dimension_line(ax, 85, 115, 6, "Device A", a_color)
    dimension_line(ax, 290, 320, 6, "Device C", c_color)
    dimension_line(ax, 485, 515, 6, "Device E", e_color)
    dimension_line(ax, *DEVICE_B, 17, "Device B", GREEN)
    dimension_line(ax, 340, 370, 17, "Device D", GREEN)

    # Overall EMC compliance badge -- top left corner, clear of the peak
    # marks row and the device annotations
    any_fail = any(level > THRESHOLD for level in harmonics.values())
    badge_color = RED if any_fail else GREEN
    badge_text = "EMC: FAIL" if any_fail else "EMC: PASS"
    ax.text(8, YMAX - 1, badge_text, ha="left", va="top",
            fontsize=15, fontweight="bold", color="white",
            bbox=dict(boxstyle="round,pad=0.35", facecolor=badge_color, edgecolor="none"))

    style_title(ax, "100 MHz Clock")
    style_labels(ax, "Frequency (MHz)", "Normalized PSD (dB)")

    save(fig, out_path)
    print("saved", out_path)


if __name__ == "__main__":
    base = "../assets"
    render(False, f"{base}/victim-band-threshold.png")
    render(True, f"{base}/victim-band-threshold-ssc.png")
    for f in sorted(BASE_HARMONICS):
        print(f"{f:4d} MHz: band {2*spread_half_width(f):5.1f} MHz  "
              f"reduction {reduction_db(f):5.2f} dB  "
              f"level {BASE_HARMONICS[f] - reduction_db(f):6.2f} dB")
