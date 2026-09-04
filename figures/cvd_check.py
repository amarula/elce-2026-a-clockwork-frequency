"""Colour-vision-deficiency check for the EMC slides.

The palette's whole job is to keep BLUE (SSC off) apart from ORANGE (SSC on)
for a speaker who is colour-blind on the blue-green axis, so any palette change
has to be re-checked here rather than eyeballed. Export the deck first, then
run this:

    npx slidev export --format png --output /tmp/vcheck
    cd figures && ~/.venvs/ssc-figs/bin/python cvd_check.py

Writes two sheets next to the deck: slides 9-12 as seen under tritanopia (the
blue-green axis) and under deuteranopia (the commonest deficiency in a
conference audience).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

SRC = "/tmp/vcheck"
OUT = ".."
SLIDES = [9, 10, 11, 12]
TITLES = {9: "9 - How Do We Fix It? (SSC off)", 10: "10 - What Is It?",
          11: "11 - Fixed (SSC on)", 12: "12 - A New Issue?"}

# Machado et al. (2009) severity-1.0 matrices, applied in linear RGB.
MATRICES = {
    "tritan": np.array([[1.255528, -0.076749, -0.178779],
                        [-0.078411, 0.930809, 0.147602],
                        [0.004733, 0.691367, 0.303900]]),
    "deutan": np.array([[0.367322, 0.860646, -0.227968],
                        [0.280085, 0.672501, 0.047413],
                        [-0.011820, 0.042940, 0.968881]]),
}


def simulate(img, m):
    rgb = img[:, :, :3]
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    sim = np.clip(lin @ m.T, 0, 1)
    return np.clip(np.where(sim <= 0.0031308, sim * 12.92,
                            1.055 * sim ** (1 / 2.4) - 0.055), 0, 1)


for name, m in MATRICES.items():
    fig, axes = plt.subplots(2, 2, figsize=(19, 11), facecolor="white")
    for ax, n in zip(axes.ravel(), SLIDES):
        ax.imshow(simulate(mpimg.imread(f"{SRC}/{n}.png"), m))
        ax.set_title(TITLES[n], fontsize=13, fontweight="bold")
        ax.axis("off")
    fig.suptitle(f"slide 9-12 simulate: {name}opia", fontsize=17, fontweight="bold")
    fig.tight_layout()
    path = f"{OUT}/cvd-check-{name}.png"
    fig.savefig(path, dpi=90, facecolor="white")
    plt.close(fig)
    print("saved", path)
