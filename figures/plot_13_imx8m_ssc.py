"""The SSC hardware on an i.MX8M pll14xx: two blocks and one register.

Third instance of the plot_11 / plot_12 figure, same blocks in the same places, so
the differences land as text. Two of them are real and worth the space:

  - **The PLL is fractional.** pll14xx is not an integer M/N part: the output is
    f_in x (M + K/2^16) / (P x 2^S), four fields across two registers. The box
    carries all four because the SSC arithmetic uses two of them (the driver's
    __clk_pll1443x_set_spread_spectrum() takes pdiv and mdiv), and because "this
    one is harder" is part of why the section goes the way it does.
  - **Three spread types, not two.** SEL_PF is two bits: 0 down, 1 up, 2 centre.
    This is the only part in the talk that offers up-spread, and the type row
    spells the encoding out. It used to be the annotation beside the block as
    well; that slot now carries the register count, so all three hardware pages
    put the same kind of fact in the same place.

The M/K/P/S ratio is off the figure, as it is on the STM32 one. It was true --
cross-checked against drivers/clk/imx/clk-pll14xx.c, GNRL_CTL 0x0, DIV_CTL0 0x4
with MDIV [21:12], PDIV [9:4], SDIV [2:0], DIV_CTL1 0x8 with KDIV [15:0] -- but
this page's argument is which register carries which knob, and four fields of a
ratio nothing on the page depends on only made the box the busiest thing on it.
What replaced it is on the slide instead: the four PLLs that have SSC at all.

The SSC fields are cross-checked against the pending patch, which adds
SSCG_CTRL at 0xc:
SSCG_ENABLE [31], MFREQ_CTL [19:12], MRAT_CTL [9:4], SEL_PF [1:0]. Bit positions
stay off the figure, as on the other two hardware pages.

The profile row says only "fixed in silicon". The same linear-ramp inference could
be made here from mfr/mrr, but the reference manual has not been checked and an
inference is not good enough to print -- see the note on slide 19.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from plot_style import ORANGE, GRAY, save

CX = 6.9               # both boxes are centred on this, so the arrow is vertical
Y_PLL = 0.0            # the signal lane
PLL_W, PLL_H = 4.6, 0.95     # just the label, and the same box as the STM32 page
SSC_TOP = -2.05        # top edge of the modulator box, 0.95 below the PLL
SSC_H = 2.14
SSC_L, SSC_R = 4.45, 9.35    # width set by the longest field name, centred on CX

KNOBS = [
    ("depth", "SSCG_CTRL.MRAT_CTL", None, True),
    ("rate", "SSCG_CTRL.MFREQ_CTL", None, True),
    ("type", "SSCG_CTRL.SEL_PF", "0 = down · 1 = up · 2 = center", True),
    ("profile", "fixed in silicon", None, False),
]

fig, ax = plt.subplots(figsize=(10.89, 4.65), facecolor="white")
ax.set_facecolor("white")
ax.set_xlim(0.61, 13.19)
ax.set_ylim(-4.39, 1.15)
ax.axis("off")

# ---- the PLL -------------------------------------------------------------
ax.add_patch(mpatches.FancyBboxPatch(
    (CX - PLL_W / 2, Y_PLL - PLL_H / 2), PLL_W, PLL_H,
    boxstyle="round,pad=0.02,rounding_size=0.10",
    facecolor="white", edgecolor="black", linewidth=1.6, zorder=3))
ax.text(CX, Y_PLL, "PLL", ha="center", va="center", zorder=4,
        fontsize=13, fontweight="bold", family="monospace")

# ---- in and out ----------------------------------------------------------
x_in = CX - PLL_W / 2 - 1.30
x_out = CX + PLL_W / 2 + 1.30
ax.annotate("", xy=(CX - PLL_W / 2, Y_PLL), xytext=(x_in, Y_PLL),
            arrowprops=dict(arrowstyle="-|>", color="black", linewidth=2.0,
                            shrinkA=0, shrinkB=0), zorder=2)
ax.annotate("", xy=(x_out, Y_PLL), xytext=(CX + PLL_W / 2, Y_PLL),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=2.4,
                            shrinkA=0, shrinkB=0), zorder=2)
ax.text(x_in - 0.18, Y_PLL, "f$_{in}$", ha="right", va="center", fontsize=12)
ax.text(x_out + 0.18, Y_PLL, "f$_{out}$", ha="left", va="center", fontsize=12,
        fontweight="bold", color=ORANGE)

# ---- the modulator, and the switch on its arrow --------------------------
ax.add_patch(mpatches.FancyBboxPatch(
    (SSC_L, SSC_TOP - SSC_H), SSC_R - SSC_L, SSC_H,
    boxstyle="round,pad=0.02,rounding_size=0.10",
    facecolor="#FDF0D8", edgecolor=ORANGE, linewidth=2.2, zorder=3))
ax.text(CX, SSC_TOP - 0.30, "SSC", ha="center", va="center",
        fontsize=13, fontweight="bold", color=ORANGE, family="monospace",
        zorder=4)

# The register count, in the same slot and the same idiom as slides 15 and 19, so
# the three hardware pages can be compared field by field. The count is this
# part's own: SSCG_CTRL at 0xc is the only register the SSC patch adds, and it
# carries all four fields including the enable -- unlike TI, nothing lives in the
# PLL's own registers. So it is "one dedicated register, four fields", the same shape as
# STM32F4 and NOT am33xx's "two dedicated registers and two control bits".
# What this replaced was "Down, up and center". Up-spread is still on the page:
# the type row spells out 0 = down / 1 = up / 2 = center, so the only part in the
# talk that offers it still says so, just inside the block instead of beside it.
ax.text(SSC_R + 0.30, SSC_TOP - SSC_H / 2,
        "One dedicated register,\nfour fields", ha="left", va="center",
        fontsize=15, fontweight="bold", color=GRAY, linespacing=1.45)

COL_KNOB, COL_REG = SSC_L + 0.35, SSC_L + 1.75
y = SSC_TOP - 0.72
for knob, reg, note, in_hw in KNOBS:
    ax.text(COL_KNOB, y, knob, ha="left", va="center", fontsize=10.5,
            color=GRAY, zorder=4)
    ax.text(COL_REG, y, reg, ha="left", va="center", fontsize=10,
            family="monospace" if in_hw else "sans-serif",
            style="normal" if in_hw else "italic",
            color="black" if in_hw else GRAY, zorder=4)
    if note:
        y -= 0.24
        ax.text(COL_REG, y, note, ha="left", va="center", fontsize=8.5,
                color=GRAY, zorder=4)
        y -= 0.30
    else:
        y -= 0.34

# The arrow runs SSC -> PLL, broken by SSCG_ENABLE drawn as an open switch.
y_gap_lo, y_gap_hi = SSC_TOP + 0.36, SSC_TOP + 0.68
ax.plot([CX, CX], [SSC_TOP, y_gap_lo], color=ORANGE, linewidth=2.2, zorder=2)
ax.annotate("", xy=(CX, Y_PLL - PLL_H / 2), xytext=(CX, y_gap_hi),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=2.2,
                            shrinkA=0, shrinkB=0), zorder=2)
ax.plot([CX, CX], [y_gap_lo, y_gap_hi], marker="o", markersize=5,
        linestyle="none", color=ORANGE, zorder=4)
ax.plot([CX, CX + 0.42], [y_gap_lo, y_gap_hi + 0.04], color=ORANGE,
        linewidth=2.0, zorder=3)

X_SPLIT = CX + 1.75
ax.text(X_SPLIT, (y_gap_lo + y_gap_hi) / 2, "SSCG_CTRL.", ha="right",
        va="center", fontsize=10.5, color=GRAY, family="monospace")
ax.text(X_SPLIT, (y_gap_lo + y_gap_hi) / 2, "SSCG_ENABLE", ha="left",
        va="center", fontsize=10.5, fontweight="bold", color=ORANGE,
        family="monospace")

save(fig, "../assets/imx8m-pll-ssc.png")
print("done")
