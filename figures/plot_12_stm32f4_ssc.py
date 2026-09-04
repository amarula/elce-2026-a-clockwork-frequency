"""The SSC hardware on the stm32f4 main PLL: two blocks and one register.

Same figure as plot_11_dpll_ssc, block for block, and that is the point: the
audience has already learned this drawing once, so everything that differs
between the two parts shows up as different *text* rather than as a different
picture. One PLL box, one SSC block, one arrow pointing **into** the PLL through
an enable switch, the same four knobs in slide 14's order.

A version of this figure drew the real topology -- the /M pre-divider, the VCO,
and the three post-dividers P, Q and R feeding SYSCLK, USB and I2S -- and it was
cut: the VCO and the fan-out are true but irrelevant here. The page is about
which register carries which knob, and the extra blocks only made the reader
work out that the drawing had changed.

The multiply/divide pair is off the figure as well, and for a reason worth
recording. ST's names invert the convention the rest of the deck uses: PLLN
multiplies and PLLM divides (GENMASK(14, 6) and bits [5:0], RM0386 §6.3.2),
where AM33xx multiplies by M and i.MX8M multiplies by M as well. Drawn, the
letters would have told a reader who had just learned the AM33xx box that M
now means the opposite -- and they earn nothing here: this page's argument is
that one register carries every knob, and nothing on it turns on the ratio.

Leaving them out also drops a claim the box could not keep. f_in x N / M is the
*VCO* frequency; the real outputs are that over P, Q or R. Naming it f_out was
off by the post-divider, which is harmless while nothing depends on the number
and wrong the moment anyone reads it as one.

RCC_SSCGR (offset 0x80) is the whole SSC interface: SSCGEN bit 31, SPREADSEL bit
30, INCSTEP [27:13], MODPER [12:0]. Bit positions stay off the figure, the same
choice slide 15 made; what is on it is which field carries which knob.

Only the main PLL has any of this -- stm32f4_rcc_init() hands pll_vco_hw and
nothing else to stm32f4_pll_init_ssc() -- which is what the slide's opening
sentence says.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from plot_style import ORANGE, GRAY, save

CX = 6.9               # both boxes are centred on this, so the arrow is vertical
Y_PLL = 0.0            # the signal lane
PLL_W, PLL_H = 4.6, 0.95     # just the label: the ratio is not on the figure
SSC_TOP = -1.85        # top edge of the modulator box, 0.95 below the PLL
SSC_H = 2.14           # four knob rows, profile included, plus the encoding line
SSC_L, SSC_R = 4.45, 9.35    # width set by the longest field name, centred on CX

# knob -> field, all four knobs from slide 14 in the same order, profile greyed
# because it is not a knob here either. Qualified names on every row: they all
# name the same register, and that is what the annotation beside the block is
# counting.
KNOBS = [
    ("depth", "RCC_SSCGR.INCSTEP", None, True),
    ("rate", "RCC_SSCGR.MODPER", None, True),
    ("type", "RCC_SSCGR.SPREADSEL", "0 = center · 1 = down", True),
    # Named, on AN4850's word rather than on an inference. The arithmetic in
    # stm32f4_pll_set_ssc() -- a constant INCSTEP accumulated over MODPER
    # reference cycles, MODPER being a quarter of the modulation period -- is the
    # signature of a linear ramp, and that alone would not have been enough to
    # print. AN4850 s2.1 states it outright: the SSCG modulates "with a
    # triangular profile", from an "internal triangular wave generator", and s2.3
    # calls MODPER a quarter of "the triangular wave period". RM0386 does not say
    # so; the application note does. Same wording as the AM33xx figure, so the
    # two rows read as the same fact about two parts.
    ("profile", "triangular (fixed in silicon)", None, False),
]

fig, ax = plt.subplots(figsize=(10.89, 4.45), facecolor="white")
ax.set_facecolor("white")
ax.set_xlim(0.61, 13.19)
ax.set_ylim(-4.19, 1.05)
ax.axis("off")

# ---- the PLL -------------------------------------------------------------
ax.add_patch(mpatches.FancyBboxPatch(
    (CX - PLL_W / 2, Y_PLL - PLL_H / 2), PLL_W, PLL_H,
    boxstyle="round,pad=0.02,rounding_size=0.10",
    facecolor="white", edgecolor="black", linewidth=1.6, zorder=3))
ax.text(CX, Y_PLL, "PLL", ha="center", va="center", zorder=4,
        fontsize=13, fontweight="bold", family="monospace")

# ---- in and out ----------------------------------------------------------
x_in = CX - PLL_W / 2 - 1.60
x_out = CX + PLL_W / 2 + 1.60
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

# Same place, size and weight as the counterpart annotation on the AM33xx
# figure, so flipping between the two slides puts the two claims in the same
# spot on screen. "One dedicated register" and not "One register": it is the
# word am33xx's line uses, and the parallel is the whole point of the slot.
# One line at 15 pt, like the other two; xlim and figsize were measured off the
# text extent and move together -- see the note in plot_11.
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

# The arrow runs SSC -> PLL: what is modulated is the multiplier, inside the
# loop. Broken by SSCGEN, drawn as an open switch.
y_gap_lo, y_gap_hi = SSC_TOP + 0.36, SSC_TOP + 0.68
ax.plot([CX, CX], [SSC_TOP, y_gap_lo], color=ORANGE, linewidth=2.2, zorder=2)
ax.annotate("", xy=(CX, Y_PLL - PLL_H / 2), xytext=(CX, y_gap_hi),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=2.2,
                            shrinkA=0, shrinkB=0), zorder=2)
ax.plot([CX, CX], [y_gap_lo, y_gap_hi], marker="o", markersize=5,
        linestyle="none", color=ORANGE, zorder=4)
ax.plot([CX, CX + 0.42], [y_gap_lo, y_gap_hi + 0.04], color=ORANGE,
        linewidth=2.0, zorder=3)

# Two pieces so the prefix can be grey, right-aligned on the x where the bit
# starts so they butt together whatever the font metrics turn out to be.
X_SPLIT = CX + 1.65
ax.text(X_SPLIT, (y_gap_lo + y_gap_hi) / 2, "RCC_SSCGR.", ha="right",
        va="center", fontsize=10.5, color=GRAY, family="monospace")
ax.text(X_SPLIT, (y_gap_lo + y_gap_hi) / 2, "SSCGEN", ha="left",
        va="center", fontsize=10.5, fontweight="bold", color=ORANGE,
        family="monospace")

save(fig, "../assets/stm32f4-pll-ssc.png")
print("done")
