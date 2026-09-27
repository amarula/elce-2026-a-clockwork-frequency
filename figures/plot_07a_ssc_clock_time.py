import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from plot_style import FIGSIZE, new_axes, style_title, style_labels, save, BLUE, ORANGE, GRAY, FILL_ALPHA, dimension

# The modulated clock itself, in the time domain: the companion of the
# spread-spectrum chart on the same slide, drawn in the idiom of the
# square-wave chart on the Digital Clock slide (same frame, title, amplitude
# ticks, time in ns). Two oscilloscope channels, one above the other, each
# with its own vertical scale and a shared time base (Dario's idea, after a
# dashed overlay, a full overlay and an offset overlay were rendered and
# found harder to read or open to misreading).
#
# A real 100 MHz clock has thousands of cycles in one modulation period, so
# the modulation cannot be drawn to scale: one sine of modulation spans the
# 100 ns window and swings the frequency by +-45 %. The clock's own period,
# 10 ns, is true. The spread clock starts in step with the fixed one, runs
# ahead while its frequency is above nominal, falls back in the second half
# and ends in step again.
fig, (ax_top, ax_bot) = plt.subplots(
    2, 1, sharex=True, figsize=FIGSIZE, facecolor="white",
    gridspec_kw=dict(hspace=0.12),
)
for a in (ax_top, ax_bot):
    a.set_facecolor("white")
    for spine in a.spines.values():
        spine.set_visible(True)
        spine.set_color("black")
        spine.set_linewidth(1.2)
    a.grid(True, linestyle=":", color="black", alpha=0.55, linewidth=0.9)
    a.tick_params(axis="both", labelsize=11)

# --voltage: the clock as a real 3.3 V CMOS signal (both pages use it since
# 2026-09-27, Dario: the two charts must match). --energy adds the proof of
# the Same Energy page: the time high filled, one 100 ns slot with the time
# high on each channel, a dimension arrow marking the swing. Without any
# flag the chart keeps Normalized Amplitude as the Sine Wave and Digital
# Clock charts (unused by the deck now).
VOLT = "--voltage" in sys.argv or "--energy" in sys.argv
ENERGY = "--energy" in sys.argv
VSW = 3.3
lo, hi = (0.0, VSW) if VOLT else (-1.0, 1.0)
span = hi - lo
for a in (ax_top, ax_bot):
    # Headroom above the trace for the one-entry legend.
    a.set_ylim(lo - 0.15 * span, hi + 0.55 * span)
    a.set_yticks([lo, hi] if VOLT else [-1, 0, 1])

def arg(name, default):
    return type(default)(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default

f0 = 100e6
cycles = arg("--cycles", 20)             # clock cycles in the window
mod_periods = arg("--mod-periods", 2)    # modulation periods in the window
window_ns = cycles * 1e9 / f0            # 10 cycles = 100 ns
depth_drawn = 0.45
t = np.linspace(0, 1, 4000 * max(1, cycles // 10))
phase_flat = 2 * np.pi * cycles * t
f_inst = cycles * (1 + depth_drawn * np.sin(2 * np.pi * mod_periods * t))
phase_ssc = 2 * np.pi * np.cumsum(f_inst) * (t[1] - t[0])
sq_flat = np.sign(np.sin(phase_flat))
sq_ssc = np.sign(np.sin(phase_ssc))

mid, amp = (lo + hi) / 2, span / 2
ax_top.plot(t * window_ns, mid + amp * sq_flat, color=BLUE, linewidth=2.5)
ax_bot.plot(t * window_ns, mid + amp * sq_ssc, color=ORANGE, linewidth=2.5)
if ENERGY:
    # The energy argument made visible: fill the time spent at the high
    # level. Same voltage, and the same total time high (50 % duty cycle,
    # and the window holds the same number of cycles on both channels),
    # so the same amount of colour on both: SSC only moves it around.
    ax_top.fill_between(t * window_ns, lo, mid + amp * sq_flat, where=sq_flat > 0,
                        color=BLUE, alpha=FILL_ALPHA, linewidth=0)
    ax_bot.fill_between(t * window_ns, lo, mid + amp * sq_ssc, where=sq_ssc > 0,
                        color=ORANGE, alpha=FILL_ALPHA, linewidth=0)
    x_dim = window_ns * 1.035
    # One time slot, the first modulation period (100 ns): inside it both
    # clocks complete the same number of cycles, so they are high for the
    # same total time, 50 ns. The slot is the thing the simple relation
    # E ~ V^2 * t_high is applied to.
    slot = window_ns / mod_periods
    s0 = 0.3 * window_ns              # any interval will do: not the first one
    s1 = s0 + slot
    dt = t[1] - t[0]
    for a, sq, c in ((ax_top, sq_flat, BLUE), (ax_bot, sq_ssc, ORANGE)):
        dimension(a, (x_dim, lo), (x_dim, hi), color=GRAY, linewidth=1.4)
        a.text(x_dim + window_ns * 0.012, mid, f"{VSW} V", rotation=90,
               ha="left", va="center", fontsize=9.5, fontweight="bold", color=GRAY)
        a.axvspan(s0, s1, color=GRAY, alpha=0.07, linewidth=0)
        for x in (s0, s1):
            a.axvline(x, color=GRAY, linestyle="--", linewidth=1.2)
        tt = t * window_ns
        t_high = ((sq > 0) & (tt >= s0) & (tt <= s1)).sum() * dt * window_ns
        a.text(s1 - 2, hi + 0.17 * span, f"high for {t_high:.0f} ns", ha="right",
               va="center", fontsize=10.5, fontweight="bold", color=c)
    y_slot = hi + 0.44 * span
    dimension(ax_top, (s0, y_slot), (s1, y_slot), color=GRAY, linewidth=1.4)
    ax_top.text((s0 + s1) / 2, y_slot, f"{slot:.0f} ns", ha="center", va="center",
                fontsize=10, fontweight="bold", color=GRAY,
                bbox=dict(facecolor="white", edgecolor="none", pad=0.6))

# One one-entry legend per channel, in the style of the spectrum chart's
# two-entry legend beside it: same words, same box, same corner.
LEG = "upper left"
ax_top.legend(handles=[mlines.Line2D([], [], color=BLUE, linewidth=3.5, label="Non-spread")],
              loc=LEG, fontsize=11, frameon=True)
ax_bot.legend(handles=[mlines.Line2D([], [], color=ORANGE, linewidth=3.5, label="Spread (SSC)")],
              loc=LEG, fontsize=11, frameon=True)

ax_bot.set_xlim(0, window_ns * (1.09 if ENERGY else 1))
ax_bot.set_xticks(np.arange(0, window_ns + 1, 20 * max(1, cycles // 10)))
ax_bot.set_xlabel("Time (ns)", fontsize=12, fontweight="bold")

style_title(ax_top, "100 MHz Clock")

# The pair must sit in the same box as the spectrum chart beside it, so that
# the two titles and the two time/frequency labels are level on the slide:
# lay out a throwaway copy of that chart's frame and take its bounds.
ref_fig, ref_ax = new_axes()
ref_ax.set_ylim(-50, 5)
ref_ax.set_xlim(96, 105)
style_title(ref_ax, "100 MHz Clock")
style_labels(ref_ax, "Frequency (MHz)", "Normalized PSD (dB)")
ref_fig.tight_layout()
box = ref_ax.get_position()
gap = 0.04
half = (box.height - gap) / 2
ax_top.set_position([box.x0, box.y1 - half, box.width, half])
ax_bot.set_position([box.x0, box.y0, box.width, half])
# One amplitude label for the pair, where the spectrum chart puts its own.
ref_label = ref_ax.yaxis.label.get_window_extent(ref_fig.canvas.get_renderer())
label_x = (ref_label.x0 + ref_label.x1) / 2 / ref_fig.get_size_inches()[0] / ref_fig.dpi
fig.text(label_x, (box.y0 + box.y1) / 2, "Voltage (V)" if VOLT else "Normalized Amplitude", rotation=90,
         ha="center", va="center", fontsize=12, fontweight="bold")
plt.close(ref_fig)

# The modulation is exaggerated by three orders of magnitude, and both pages
# print numbers next to it: say so on the chart (Dario, 2026-09-27), in the
# quiet corner under the time axis, grey italic like the parameter chart's
# footnotes.
fig.text(0.985, 0.012, "modulation exaggerated, not to scale", ha="right", va="bottom",
         fontsize=9, style="italic", color=GRAY)

out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "../assets/ssc-clock-time-domain.png"
fig.savefig(out, dpi=150, facecolor="white")
plt.close(fig)
print("done")
