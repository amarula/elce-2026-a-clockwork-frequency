# A Clockwork Frequency: Bringing Spread Spectrum to the Linux Clock Subsystem

Slides for the ELCE 2026 talk, built with [Slidev](https://github.com/slidevjs/slidev)
and the Amarula theme (submodule).

The theme is a git submodule, so clone with it:

- `git clone --recursive <this repository>`
- or, in an existing clone, `git submodule update --init`

To start the slide show:

- `pnpm install`
- `pnpm dev`
- visit <http://localhost:3030>

Edit [slides.md](./slides.md) to see the changes.

Learn more about Slidev at the [documentation](https://sli.dev/).

## Export

To export:

- `pnpm add -D playwright-chromium`
- `pnpm export`

Learn more about exporting options [here](https://sli.dev/guide/exporting.html).
