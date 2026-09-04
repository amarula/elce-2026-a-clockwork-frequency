"""The SSC hardware on an am33xx/am43xx DPLL: two blocks and the registers.

Deliberately **not** the display clock path. An earlier version of this figure
drew the whole chain -- sys_clkin, the DPLL, the M2 divider, lcd_gclk, the LCDC,
and the ti,set-rate-parent request running back the other way. It was accurate
but it made the reader learn the LCD subsystem in order to learn SSC, and the
only blocks that touch an SSC register field are the first two. So this keeps the
DPLL and the modulator and nothing else: everything on screen is something a bit
in these four registers acts on.

The one thing that must stay right is the **direction**. SSC is not a stage the
clock passes through on the way out -- there is no "SSC block" between the DPLL
and its consumers. It is a modulator inside the loop that sweeps the feedback
multiplier M, so its arrow points *into* the DPLL, and SSC_EN is a switch on that
arrow rather than a mux on the output. Drawing it in cascade would put the deck's
reference hardware page at odds with the reference manual (spruh73x §8.1.6.7).

Fields come from spruh73x (am33xx) / spruhl7x (am43xx); the addresses are on the
slide rather than here, so the figure stays about topology.

Colour: ORANGE is "SSC on" everywhere in this deck, so the modulator and its
arrow carry it and the DPLL stays neutral -- the same grammar as the spectra.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from plot_style import ORANGE, GRAY, save

CX = 6.9               # both boxes are centred on this, so the arrow is vertical
Y_DPLL = 0.0           # the signal lane
DPLL_W, DPLL_H = 4.6, 1.75   # tall enough to hold M and N inside it
SSC_TOP = -1.85        # top edge of the modulator box, 0.95 below the DPLL
SSC_H = 2.14           # four knob rows, profile included, plus the encoding line
SSC_L, SSC_R = 4.45, 9.35   # width set by the longest register name, kept centred on CX

# M and N as two named fields of CM_CLKSEL, written out *inside* the DPLL box --
# the same rule the SSC block follows, where each knob sits next to the register
# that carries it. A register belongs to the block that owns it, so nothing on
# this figure floats between blocks any more.
#
# This was briefly drawn as a 32-bit register map -- proportional cells, reserved
# fields greyed, bit ranges under each name -- and cut back to these two lines:
# the bit widths were not what the page is for, and the qualified names match
# CM_CLKMODE.SSC_EN and CM_CLKMODE.SSC_DOWNSPREAD elsewhere. The off-by-one is
# real: omap3_noncore_dpll_program() writes (n - 1) into DPLL_DIV.
CLKSEL_LINES = "M = CM_CLKSEL.DPLL_MULT\nN = CM_CLKSEL.DPLL_DIV + 1"

# knob -> which register. All **four** knobs from the conceptual half are listed,
# in slide 14's order, so the audience reads this as "the theory, in hardware"
# rather than as a new list to learn -- profile is here too, greyed, precisely
# because it is the one you do not get.
#
# Two columns, not three. A middle column has been tried twice and removed twice:
# first with the hardware's own notation ($\pm\Delta$M, f$_{mod}$), which invited
# the question of how the modulator walks the multiplier step by step, and then
# with each knob's general-theory effect (band width / sweeps per second / where
# it sits / peak reduction), which restated slide 14 for an audience that had
# just seen it. The knob names alone carry the link back.
KNOBS = [
    ("depth", "CM_SSC_DELTAMSTEP", None, True),
    ("rate", "CM_SSC_MODFREQDIV", None, True),
    ("type", "CM_CLKMODE.SSC_DOWNSPREAD", "0 = center · 1 = down", True),
    # named, not just "fixed": the modulator adds a constant increment to the
    # multiplier on every phase-comparison cycle, and a constant increment is a
    # linear ramp -- so the profile TI wired in is the triangular one, which is
    # the profile slide 14 measured as the best. Worth saying rather than leaving
    # "fixed in silicon" to imply the audience got the leftovers.
    ("profile", "triangular (fixed in silicon)", None, False),
]

# xlim spans the content plus a small margin; the width keeps the original
# 1.155 data-units-per-inch so nothing changes scale when the frame is cropped
fig, ax = plt.subplots(figsize=(10.89, 4.45), facecolor="white")
ax.set_facecolor("white")
ax.set_xlim(0.61, 13.19)
ax.set_ylim(-4.19, 1.05)
ax.axis("off")

# ---- the DPLL ------------------------------------------------------------
ax.add_patch(mpatches.FancyBboxPatch(
    (CX - DPLL_W / 2, Y_DPLL - DPLL_H / 2), DPLL_W, DPLL_H,
    boxstyle="round,pad=0.02,rounding_size=0.10",
    facecolor="white", edgecolor="black", linewidth=1.6, zorder=3))
# "PLL", not "DPLL", even though TI's own name for this block is the latter and
# its register fields say so (DPLL_MULT / DPLL_DIV, both still drawn inside the
# box). The deck settled on one word across all three vendors: ST and NXP do not
# call their blocks DPLLs, so "always DPLL" would have been wrong on two pages out
# of three, while "always PLL" costs nothing here -- the TI-ness is carried by the
# register names, which are quotations and keep their own spelling.
ax.text(CX, Y_DPLL + 0.49, "PLL", ha="center", va="center", zorder=4,
        fontsize=13, fontweight="bold", family="monospace")
ax.text(CX, Y_DPLL + 0.09, "f$_{out}$ = f$_{in}$ $\\times$ M / N", ha="center",
        va="center", zorder=4, fontsize=12)
# left-aligned as a block under the formula: two equations centred individually
# would read as ragged. The three rows sit low in the box on purpose -- the block
# is optically centred, which is not the same as centring the text extents
ax.text(CX - 1.30, Y_DPLL - 0.37, CLKSEL_LINES, ha="left", va="center",
        fontsize=10, color=GRAY, family="monospace", linespacing=1.55, zorder=4)

# ---- in and out ----------------------------------------------------------
# Short stubs, not arrows running to the edge of the figure. They used to reach
# 0.85 and 14.15 because they carried "reference clock" / "output clock" at their
# far ends; once the labels moved next to the box, all that length was dead
# space. The xlim and the figure width below are cropped to match -- the axes are
# not isotropic, so shortening the arrows without shrinking both would simply
# stretch every box sideways.
x_in = CX - DPLL_W / 2 - 1.60
x_out = CX + DPLL_W / 2 + 1.60
ax.annotate("", xy=(CX - DPLL_W / 2, Y_DPLL), xytext=(x_in, Y_DPLL),
            arrowprops=dict(arrowstyle="-|>", color="black", linewidth=2.0,
                            shrinkA=0, shrinkB=0), zorder=2)
ax.annotate("", xy=(x_out, Y_DPLL), xytext=(CX + DPLL_W / 2, Y_DPLL),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=2.4,
                            shrinkA=0, shrinkB=0), zorder=2)
# The arrows are labelled with the same two symbols the box's formula uses, each
# at the far end of its own arrow -- f_in before the tail, f_out past the head --
# so the label reads as the signal entering and leaving, and the eye follows the
# arrow to find it. Words were tried first --
# "reference clock" and "output clock", and before that "spread clock" -- but
# f_in / f_out say the same thing and tie the arrow to the arithmetic. Correct on
# both counts: omap2_get_dpll_rate() computes clk_ref * DPLL_MULT / (DPLL_DIV+1),
# so f_in really is the reference and f_out really is this PLL's rate. What sits
# further downstream (the M2 post-divider, muxes) is out of frame on purpose.
ax.text(x_in - 0.18, Y_DPLL, "f$_{in}$", ha="right", va="center", fontsize=12)
ax.text(x_out + 0.18, Y_DPLL, "f$_{out}$", ha="left", va="center", fontsize=12,
        fontweight="bold", color=ORANGE)

# ---- the modulator, and the switch on its arrow --------------------------
ax.add_patch(mpatches.FancyBboxPatch(
    (SSC_L, SSC_TOP - SSC_H), SSC_R - SSC_L, SSC_H,
    boxstyle="round,pad=0.02,rounding_size=0.10",
    facecolor="#FDF0D8", edgecolor=ORANGE, linewidth=2.2, zorder=3))
# centred and set like DPLL, so the two block titles read as siblings; only the
# colour tells them apart, which is the deck's grammar doing the work
ax.text(CX, SSC_TOP - 0.30, "SSC", ha="center", va="center",
        fontsize=13, fontweight="bold", color=ORANGE, family="monospace",
        zorder=4)

# What the block costs, beside the block itself. Every annotation on this figure
# sits to the right -- SSC_EN above, this one level with the SSC box -- so the
# blocks keep the centre line and the reader always knows where the commentary is.
# Set larger and bold: this is the page's takeaway, not a footnote, and the space
# to the right of the block was empty anyway. Still GRAY rather than black, so it
# stays an annotation *about* the block and does not compete with the block titles.
#
# ONE LINE at 15 pt, and the two go together: the line is what sets this figure's
# width. xlim's right edge and figsize's width were measured off the rendered text
# extent and must move together -- the axes are not isotropic, so widening one
# without the other stretches every box sideways. Re-measure both if this string
# or its size ever changes; at 17 pt the figure reaches 910 px of the 960 px
# canvas, which is the practical ceiling.
ax.text(SSC_R + 0.30, SSC_TOP - SSC_H / 2,
        "Two dedicated registers\nand two control bits", ha="left", va="center",
        fontsize=15, fontweight="bold", color=GRAY, linespacing=1.45)

COL_KNOB, COL_REG = SSC_L + 0.35, SSC_L + 1.75
y = SSC_TOP - 0.72
for knob, reg, note, in_hw in KNOBS:
    ax.text(COL_KNOB, y, knob, ha="left", va="center", fontsize=10.5,
            color=GRAY, zorder=4)
    # the profile row names no register, so it is set in the body face, italic
    # and grey: the column still reads as "and this one you do not get"
    ax.text(COL_REG, y, reg, ha="left", va="center", fontsize=10,
            family="monospace" if in_hw else "sans-serif",
            style="normal" if in_hw else "italic",
            color="black" if in_hw else GRAY, zorder=4)
    if note:
        # a one-bit field is worth decoding on the spot: which value is which
        # spread type is the first thing anyone writing the DT wants to know
        y -= 0.24
        ax.text(COL_REG, y, note, ha="left", va="center", fontsize=8.5,
                color=GRAY, zorder=4)
        y -= 0.30
    else:
        y -= 0.34

# The arrow runs modulator -> DPLL: SSC sweeps the multiplier, it does not
# post-process the output. The break in it is SSC_EN, drawn as an open switch.
y_gap_lo, y_gap_hi = SSC_TOP + 0.36, SSC_TOP + 0.68
ax.plot([CX, CX], [SSC_TOP, y_gap_lo], color=ORANGE, linewidth=2.2, zorder=2)
ax.annotate("", xy=(CX, Y_DPLL - DPLL_H / 2), xytext=(CX, y_gap_hi),
            arrowprops=dict(arrowstyle="-|>", color=ORANGE, linewidth=2.2,
                            shrinkA=0, shrinkB=0), zorder=2)
ax.plot([CX, CX], [y_gap_lo, y_gap_hi], marker="o", markersize=5,
        linestyle="none", color=ORANGE, zorder=4)
ax.plot([CX, CX + 0.42], [y_gap_lo, y_gap_hi + 0.04], color=ORANGE,
        linewidth=2.0, zorder=3)

# Fully qualified, on one line: the switch is a bit in a register, and splitting
# the name over two lines made it read as two separate things. Only the bit is
# ORANGE -- the register that contains it is not an SSC register, it is the PLL's
# own control register with two SSC bits added, and the colour says so.
# Drawn as two pieces so the prefix can be grey: the prefix is right-aligned on
# the same x where the bit starts, which butts them together exactly whatever the
# font metrics turn out to be.
X_SPLIT = CX + 1.73
ax.text(X_SPLIT, (y_gap_lo + y_gap_hi) / 2, "CM_CLKMODE.", ha="right",
        va="center", fontsize=10.5, color=GRAY, family="monospace")
ax.text(X_SPLIT, (y_gap_lo + y_gap_hi) / 2, "SSC_EN", ha="left",
        va="center", fontsize=10.5, fontweight="bold", color=ORANGE,
        family="monospace")

# Nothing is written next to the arrow. Three captions were tried here and all
# three went: "sweeps M $\pm\Delta$M" and "M must stay in [20, 2045]" pulled the
# audience into the modulator's arithmetic (the range comes back on the next
# slide, where ti,min-div gives it a reason to exist), and "from inside the loop,
# not after the output" only restated what the arrow's direction already shows.
# The geometry is the claim: modulator below, arrow pointing up into the DPLL.

save(fig, "../assets/am33xx-dpll-ssc.png")
print("done")
