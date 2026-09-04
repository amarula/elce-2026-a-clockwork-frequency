"""The modulation-parameter slide: one row per configuration, three cells each.

Left cell lists the parameters and their settings, top to bottom. Then the same
clock twice: the time domain -- what you actually configure -- and the resulting
spectrum, in the coarse idiom of the "What is it" chart.

Both chart cells share the same frequency window, vertical on the left and
horizontal on the right, so the sweep's excursion and the spread band are the
same span rotated ninety degrees. Keep the two ranges equal if you touch them.

Every knob a row moves from the row above is boxed in the parameter list, so
what the row is testing is readable at a glance. The first rows move one knob
each; the later ones move two, which they can afford because the slide before
this one has already told the audience which knobs set the peak and which one
only moves the band. A reader who knows that reads a two-knob row by
separating the effects: the band moving sideways is the type, the band
changing width and height is the depth.

What the chain must never lose is one pair of rows whose peak figure is
*identical*, because that is the only place the audience sees -- rather than
is told -- that some knobs do not touch the peak at all. Rows 3 and 4 hold the
depth and move type and rate together, and their peaks agree to the decibel.
Break that and the slide asserts its premise without ever showing it.

The time window is fixed across rows: drawing a constant number of cycles
instead would hide a change of rate completely, and row 4 is where the rate
finally becomes visible.

The panels are deliberately untitled -- which is the time domain and which the
frequency domain is obvious from the axes, and the speaker says it out loud.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import LinearSegmentedColormap
from plot_style import BLUE, ORANGE, GRAY, FILL_ALPHA, dimension
from plot_05_victim_band import RBW_MHZ, reduction_db

F0 = 100.0  # MHz, nominal clock frequency

# This slide's own depth, deliberately *not* the one the conceptual charts on
# slides 9-12 are drawn at. Those never name a number and are drawn deep enough
# to read; this is the slide that puts the parameters on screen, so it carries a
# value a real part would take. +/-1% sits inside what configurable clock
# generators offer, and it is deep enough that the profile still visibly matters:
# the sinusoid's horns depend on band/RBW, and at the serial standards' +/-0.5%
# the filter smooths them down to ~1 dB, which makes row 1 an anaemic argument.
DEPTH_PCT = 0.01

# Shared frequency window: the time cell's y-axis and the spectrum cell's x-axis.
# Sized for the *shifted* bands, not just the centred one: down- and up-spread
# move the band a full half-width either way, and the RBW skirt then reaches
# centre +/- (half_width + 6 sigma). Re-scale if the depths change -- too wide
# and the waveforms flatten into squiggles and the two profiles stop being
# distinguishable, too narrow and the skirts meet the frame still descending,
# which reads as a clipped band rather than a closed one. 0.12 MHz of clearance
# was tried once and looked clipped; this leaves a full MHz.
#
# The widest band on the slide is the centred +/-1 % pair at 99-101, so the
# window is that plus a margin, not the 97-103 the rows needed back when a
# +/-1 % band was also being shifted a full megahertz either way. Tightening it
# buys about 50 % more width on every band, and the same on the excursion in
# the time cells, where the shallow rows would otherwise read as flat.
F_LO, F_HI = 98.0, 102.0
F_TICKS = [98, 99, 100, 101, 102]
FSPAN = F_HI - F_LO  # offsets below are fractions of it, so the window can move

# Fixed observation window, so a change of rate would visibly change the number
# of cycles. Sized to hold ~3 cycles of the slowest rate on the slide.
T_WINDOW = 600.0  # us
T_MARGIN = 75.0   # us of clear space on the right for the depth arrow
T_TICKS = [0, 100, 200, 300, 400, 500, 600]

PSD_FLOOR = -40.0
PSD_TOP = 9.0  # headroom above 0 dB for the peak-reduction label

# Where the excursion sits relative to nominal, as a multiple of the half-width.
# This is the *spread type*, a separate knob from the profile: it only moves the
# band, it never changes its width or the peak reduction.
TYPE_OFFSET = {"down": -1.0, "center": 0.0, "up": +1.0}

LABELS = {"depth_pct": "depth", "rate_khz": "rate",
          "profile": "profile", "spread_type": "spread type"}


def sweep_norm(t, period, profile):
    """The modulation profile over time, normalised to [0, 1].

    Both profiles start at mid-excursion and rise first, so the waveforms of two
    rows line up in phase and can be compared by eye.
    """
    phase = 2 * np.pi * t / period
    if profile == "triangular":
        shape = (2 / np.pi) * np.arcsin(np.sin(phase))
    elif profile == "sinusoidal":
        shape = np.sin(phase)
    else:
        raise ValueError(f"unknown profile {profile!r}")
    return (shape + 1) / 2


def dwell_cdf(x, half_width, profile):
    """Fraction of one sweep spent below offset `x` from the band centre.

    This is where the profile earns its keep. A triangular sweep moves at a
    constant rate, so it spends equal time at every frequency -- a uniform
    distribution. A sinusoid slows to a stop at its turning points and lingers
    there, which is the arcsine law: the density diverges at the band edges.
    """
    u = np.clip(x / half_width, -1.0, 1.0)
    if profile == "triangular":
        return (u + 1.0) / 2.0
    if profile == "sinusoidal":
        return 0.5 + np.arcsin(u) / np.pi
    raise ValueError(f"unknown profile {profile!r}")


def spectrum_db(centre, half_width, profile, rate_khz, rbw=RBW_MHZ):
    """The swept clock's spectrum: `(freqs, level_db)`, 0 dB = unmodulated line.

    Frequency modulation puts the carrier's power into a **comb of sidebands
    spaced by the modulation rate**, and for a large modulation index the
    envelope of that comb is the sweep's dwell distribution -- the time spent per
    unit frequency. So each line k carries the dwell fraction of the f_m-wide
    slice it stands for, and the analyser reports the comb seen through its
    resolution filter.

    Both knobs that matter fall out of this one expression:

    - **profile** sets the envelope, through `dwell_cdf`. Triangular sweeps at a
      constant rate, so the dwell is uniform and the band is flat. A sinusoid
      lingers at its turning points, so the dwell follows the arcsine law and
      grows horns at the band edges.
    - **rate** sets the line spacing. While the spacing stays well inside the
      resolution bandwidth the filter merges the lines into a smooth band and the
      rate does not matter at all. Push it past the RBW and the analyser starts
      resolving individual lines -- and a resolved line is a narrow peak again,
      which is how a too-fast sweep gives back most of the reduction.

    The filter is Gaussian with `FWHM = RBW`, the usual instrument convention,
    normalised so a flat dwell distribution lands at exactly
    `RBW / (2*half_width)` -- i.e. this reproduces `reduction_db()` for a slow
    triangular sweep, keeping one derivation behind every spectrum in the deck.

    This is the quasi-static envelope sampled on the sideband comb, not a full FM
    synthesis: a real spectrum carries Bessel ripple this does not model, and the
    quasi-static limit slightly overstates the sinusoid's horns. The mechanisms
    and the signs are right; treat the decibels as the model's, not a
    measurement's.
    """
    f_m = rate_khz / 1000.0          # MHz, sideband spacing
    sigma = rbw / 2.3548             # FWHM -> sigma for a Gaussian

    k = np.arange(-int(np.ceil(half_width / f_m)) - 1,
                  int(np.ceil(half_width / f_m)) + 2)
    f_k = centre + k * f_m
    # Power per line, taken from the CDF rather than the density: the arcsine
    # density is infinite at the band edges, its integral is not.
    power = (dwell_cdf(k * f_m + f_m / 2, half_width, profile)
             - dwell_cdf(k * f_m - f_m / 2, half_width, profile))

    # Evaluated over the band itself plus enough margin for the filter skirts --
    # NOT over the display window. Deriving the grid from F_LO/F_HI meant the
    # band fell outside it as soon as the depth changed or another harmonic was
    # asked for, and the returned peak was then silently wrong.
    margin = half_width + 6 * sigma
    freqs = np.linspace(centre - margin, centre + margin, 4000)
    density = (power * np.exp(-0.5 * ((freqs[:, None] - f_k) / sigma) ** 2)
               / (sigma * np.sqrt(2 * np.pi))).sum(axis=1)
    return freqs, 10 * np.log10(np.maximum(density * rbw, 1e-12))


def style_axis(ax):
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.1)
    ax.grid(True, linestyle=":", color="black", alpha=0.55, linewidth=0.8)
    ax.tick_params(axis="both", labelsize=8.5)


def param_cell(ax, cfg, half_width, period, changed):
    """The four knobs and their settings, top to bottom.

    `changed` holds the keys that differ from the row above; each gets a box so
    the reader can see at a glance what this row is testing. An optional `note` on
    the config prints underneath -- use it whenever a row carries a value no real
    part would be configured with, so the slide never implies otherwise.
    """
    ax.axis("off")
    rows = [
        ("depth_pct", f"$\\pm${cfg['depth_pct'] * 100:g} %  ($\\pm${half_width:g} MHz)"),
        ("rate_khz", f"{cfg['rate_khz']:g} kHz  ({period:.3g} $\\mu$s)"),
        ("profile", cfg["profile"]),
        ("spread_type", cfg["spread_type"]),
    ]
    # Packed towards the top so an optional note still lands inside this row's
    # cell rather than drifting into the one below.
    y = 0.88
    for key, value in rows:
        boxed = key in changed
        ax.text(0.0, y, LABELS[key], ha="left", va="center", fontsize=8.5,
                color=GRAY, transform=ax.transAxes)
        ax.text(0.50, y, value, ha="left", va="center", fontsize=9,
                fontweight="bold", color="black", transform=ax.transAxes,
                bbox=dict(boxstyle="round,pad=0.22", facecolor="#E4E4E4",
                          edgecolor="none") if boxed else None)
        y -= 0.175
    if cfg.get("note"):
        ax.text(0.0, y - 0.01, cfg["note"], ha="left", va="top", fontsize=7.5,
                style="italic", color=GRAY, transform=ax.transAxes)


def time_cell(ax, half_width, period, profile, spread_type, show_xlabel, show_legend):
    """Frequency against time -- the knobs as you set them."""
    style_axis(ax)
    ax.set_xlim(0, T_WINDOW + T_MARGIN)
    ax.set_ylim(F_LO, F_HI)
    ax.set_yticks(F_TICKS)
    ax.set_xticks(T_TICKS)
    ax.set_ylabel("Frequency (MHz)", fontsize=9, fontweight="bold")
    if show_xlabel:
        ax.set_xlabel("Time ($\\mu$s)", fontsize=9.5, fontweight="bold")
    else:
        ax.tick_params(axis="x", labelbottom=False)

    centre = F0 + TYPE_OFFSET[spread_type] * half_width
    lo, hi = centre - half_width, centre + half_width

    # Nominal frequency: the clock as it runs with SSC off. Solid, and in the
    # non-spread colour, so it matches the spike on the spectrum cell.
    ax.axhline(F0, color=BLUE, linewidth=1.8)

    t = np.linspace(0, T_WINDOW, 8000)
    ax.plot(t, lo + 2 * half_width * sweep_norm(t, period, profile),
            color=ORANGE, linewidth=2.0)

    # Depth: the full peak-to-peak excursion, measured in the clear margin.
    # Positions are fractions of T_MARGIN so changing the window keeps the layout.
    x_dep = T_WINDOW + 0.30 * T_MARGIN
    x_guide = x_dep + 0.17 * T_MARGIN
    ax.plot([T_WINDOW, x_guide], [hi, hi], color=GRAY, linestyle=":", linewidth=1.0)
    ax.plot([T_WINDOW, x_guide], [lo, lo], color=GRAY, linestyle=":", linewidth=1.0)
    dimension(ax, (x_dep, lo), (x_dep, hi), color=GRAY, linewidth=1.3)
    ax.text(x_dep - 0.06 * T_MARGIN, centre, f"{2 * half_width:g} MHz",
            ha="right", va="center",
            rotation=90, fontsize=8, fontweight="bold", color=GRAY,
            bbox=dict(facecolor="white", edgecolor="none", pad=0.6))

    # Modulation period: one sweep cycle, in whichever half the waveform leaves
    # free. A fast sweep makes this arrow very short, which is the point -- so
    # the label moves beside it rather than being squeezed underneath.
    below = (lo - F_LO) >= (F_HI - hi)
    y_per = (lo - 0.09 * FSPAN) if below else (hi + 0.09 * FSPAN)
    short = period < 0.25 * T_WINDOW
    dimension(ax, (0, y_per), (period, y_per), color=GRAY, linewidth=1.3)
    if short:
        ax.text(period + 0.07 * T_MARGIN, y_per, f"{period:.3g} $\\mu$s",
                ha="left", va="center",
                fontsize=8, fontweight="bold", color=GRAY,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
    else:
        ax.text(period / 2, y_per + (0.035 * FSPAN) * (-1 if below else 1),
                f"{period:.3g} $\\mu$s",
                ha="center", va="top" if below else "bottom",
                fontsize=8, fontweight="bold", color=GRAY)

    if show_legend:
        ax.legend(handles=[
            mlines.Line2D([], [], color=BLUE, linewidth=2.6, label="Non-spread"),
            mlines.Line2D([], [], color=ORANGE, linewidth=2.6, label="Spread (SSC)"),
        ], loc="upper left", fontsize=7.5, frameon=True, borderpad=0.3,
            labelspacing=0.25, handlelength=1.5)
    return centre, lo, hi


# The fill under the spectrum is shaded by energy density, not painted flat
# (2026-09-03, Dario's ask): the dB axis makes a narrow band look like less
# energy than a wide one, when the total is identical in every row -- the
# area under the *linear* PSD -- and what changes is the density, the height.
# So the fill is darker where the linear PSD is higher, on one scale shared
# by all rows (DENSITY_VMAX_DB, just above the highest peak on the slide):
# rows 3 and 4 come out darker than row 2, and row 1's horns darker than its
# own middle, which is the sinusoidal-vs-triangular argument in colour.
DENSITY_CMAP = LinearSegmentedColormap.from_list(
    "density", ["#F7E3B0", ORANGE, "#9C5F00"])
DENSITY_VMAX_DB = -8.0


def density_fill(ax, xs, raw_db, level):
    """Fill under `level` shaded by linear density, clipped to the band."""
    density = 10 ** (raw_db / 10) / 10 ** (DENSITY_VMAX_DB / 10)
    img = np.tile(np.clip(density, 0, 1), (2, 1))
    im = ax.imshow(img, extent=[xs[0], xs[-1], PSD_FLOOR, PSD_TOP],
                   aspect="auto", origin="lower", cmap=DENSITY_CMAP,
                   vmin=0, vmax=1, interpolation="bilinear", zorder=1)
    clip = ax.fill_between(xs, PSD_FLOOR, level, facecolor="none",
                           edgecolor="none", linewidth=0)
    im.set_clip_path(clip.get_paths()[0], transform=ax.transData)


def spectrum_cell(ax, centre, half_width, lo, hi, profile, rate_khz,
                  show_xlabel, show_legend):
    """The same clock as a spectrum -- the consequence of those knobs."""
    style_axis(ax)
    ax.set_xlim(F_LO, F_HI)
    ax.set_ylim(PSD_FLOOR, PSD_TOP)
    ax.set_xticks(F_TICKS)
    ax.set_ylabel("PSD (dB)", fontsize=9, fontweight="bold")
    if show_xlabel:
        ax.set_xlabel("Frequency (MHz)", fontsize=9.5, fontweight="bold")
    else:
        ax.tick_params(axis="x", labelbottom=False)

    ax.plot([F_LO, F_HI], [PSD_FLOOR, PSD_FLOOR], color=BLUE, linewidth=1.8)

    xs, raw = spectrum_db(centre, half_width, profile, rate_khz)
    level = np.clip(raw, PSD_FLOOR, PSD_TOP)
    density_fill(ax, xs, raw, level)
    ax.plot(xs, level, color=ORANGE, linewidth=1.8)

    # Non-spread: the whole harmonic inside one resolution bandwidth.
    ax.vlines(F0, PSD_FLOOR, 0, color=BLUE, linewidth=2.6)

    # Peak reduction -- the payoff. Measured on whichever side of the band has
    # more clear space: up-spread pushes the band against the right edge of the
    # window, so a fixed right-hand position would run the label off the axis.
    peak = level.max()
    right, left = max(hi, F0), min(lo, F0)
    off = 0.13 * FSPAN
    x_red = (right + off) if (F_HI - right) >= (left - F_LO) else (left - off)
    ax.plot([xs[level.argmax()], x_red], [peak, peak],
            color=GRAY, linestyle="--", linewidth=1.1)
    ax.plot([F0, x_red], [0, 0], color=GRAY, linestyle="--", linewidth=1.1)
    dimension(ax, (x_red, 0), (x_red, peak), color=GRAY, linewidth=1.3)
    ax.text(x_red, 1.2, f"$-${abs(peak):.1f} dB", ha="center", va="bottom",
            fontsize=8.5, fontweight="bold", color=GRAY)

    if show_legend:
        ax.legend(handles=[
            mlines.Line2D([], [], color=BLUE, linewidth=2.6, label="Non-spread"),
            mlines.Line2D([], [], color=ORANGE, linewidth=2.6, label="Spread (SSC)"),
        ], loc="upper left", fontsize=7.5, frameon=True, borderpad=0.3,
            labelspacing=0.25, handlelength=1.5)
    return peak


# The chain. Sinusoidal leads so that every later row carries the profile that
# actually ships. Row 2 moves the profile alone; rows 3 and 4 then move two
# knobs each, and between them the spread type takes all three of its values.
#
# The rate rides on row 4 rather than getting a row of its own. On its own it
# would show nothing: inside the range real parts offer it changes the peak by
# nothing measurable (3, 30, 50 and 100 kHz all give -14.26 dB for a triangular
# sweep), and the values that would break the band into resolved sidebands --
# several hundred kHz -- are values no part will take. Paired with a change of
# type the row has a visible job, and "nothing" becomes the lesson instead of a
# defect: the sweep is plainly faster in the time cell, the band has moved, and
# the peak has not shifted by a decibel. The rate sets how you modulate, not
# what you gain.
#
# 5 kHz is the order of magnitude of SSC built into SoC PLLs (STM32, i.MX, TI
# DPLLs); 15 kHz is on the way to the 30-33 kHz the serial standards specify for
# links whose receiver tracks the wander with a CDR. Both land on round periods
# (200 us and 66.7 us), and 15 rather than 30 keeps the faster sweep at nine
# cycles in the window -- enough to read as "faster", few enough to still read
# as a waveform once the figure is scaled onto a slide.
RATE_KHZ = 5.0
RATE_KHZ_FAST = 15.0

# Row 3 drops the depth by half. +/-0.5 % is the figure the serial standards
# carry, so it is a number someone in the room recognises, and in up-spread it
# puts the band at 100-101 MHz -- comfortably inside F_LO/F_HI, so the window
# does not have to be re-scaled and the waveforms keep their shape.
DEPTH_PCT_SHALLOW = 0.005

CONFIGS = [
    dict(depth_pct=DEPTH_PCT, rate_khz=RATE_KHZ,
         profile="sinusoidal", spread_type="center"),
    dict(depth_pct=DEPTH_PCT, rate_khz=RATE_KHZ,
         profile="triangular", spread_type="center"),
    dict(depth_pct=DEPTH_PCT_SHALLOW, rate_khz=RATE_KHZ,
         profile="triangular", spread_type="down"),
    dict(depth_pct=DEPTH_PCT_SHALLOW, rate_khz=RATE_KHZ_FAST,
         profile="triangular", spread_type="up"),
]


def changed_keys(prev, cur):
    """The knobs this row moves. Guards the slide's own premise.

    Two is the ceiling. A reader separates two effects by attributing each to
    the knob the previous slide named for it; three would leave nothing to
    attribute by, and the row would stop being evidence of anything.

    Only the four knobs count -- `note` is annotation, not a setting.
    """
    if prev is None:
        return frozenset()
    diff = frozenset(k for k in LABELS if prev[k] != cur[k])
    if len(diff) > 2:
        raise ValueError(f"a row may move at most two knobs, not {sorted(diff)}")
    return diff


def render(out_path, configs=CONFIGS):
    n = len(configs)
    fig = plt.figure(figsize=(14.5, 1.72 * n), facecolor="white")
    gs = fig.add_gridspec(n, 3, width_ratios=[0.92, 2.15, 2.15],
                          hspace=0.20, wspace=0.26,
                          left=0.015, right=0.985,
                          top=1 - 0.10 / n, bottom=0.42 / n)

    prev = None
    for i, cfg in enumerate(configs):
        half_width = cfg["depth_pct"] * F0     # MHz, deviation either side
        period = 1000.0 / cfg["rate_khz"]      # us, one full sweep
        first, last = i == 0, i == n - 1

        param_cell(fig.add_subplot(gs[i, 0]), cfg, half_width, period,
                   changed_keys(prev, cfg))
        centre, lo, hi = time_cell(
            fig.add_subplot(gs[i, 1]), half_width, period,
            cfg["profile"], cfg["spread_type"],
            show_xlabel=last, show_legend=first)
        peak = spectrum_cell(
            fig.add_subplot(gs[i, 2]), centre, half_width, lo, hi,
            cfg["profile"], cfg["rate_khz"],
            show_xlabel=last, show_legend=first)
        print(f"  {i+1}. {cfg['profile']:11s} depth +/-{cfg['depth_pct']*100:g}% "
              f"rate {cfg['rate_khz']:>5g} kHz {cfg['spread_type']:6s} "
              f"band {lo:g}-{hi:g} MHz -> peak {peak:6.2f} dB")
        prev = cfg

    fig.savefig(out_path, dpi=150, facecolor="white")
    plt.close(fig)
    print("saved", out_path)


if __name__ == "__main__":
    render("../assets/ssc-modulation-parameters.png")
    # Sanity check: a slow triangular sweep must land on the analytic value the
    # rest of the deck quotes, or the two derivations have drifted apart.
    flat = -reduction_db(F0, DEPTH_PCT)
    xs, level = spectrum_db(F0, DEPTH_PCT * F0, "triangular", RATE_KHZ)
    mid = level[np.argmin(np.abs(xs - F0))]
    print(f"check: slow triangular mid-band {mid:.4f} dB vs analytic {flat:.4f} dB")
    assert abs(mid - flat) < 0.01, "triangular spectrum no longer matches reduction_db()"
