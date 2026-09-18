<script setup>
import { useDarkMode } from '@slidev/client'

const { isDark } = useDarkMode()

// Constants for length thresholds
const TITLE_LONG = 80
const TITLE_MEDIUM = 50

function getTitleSizeClass(title = '') {
  const len = title.length
  if (len > TITLE_LONG) return 'text-3xl'
  if (len > TITLE_MEDIUM) return 'text-4xl'
  return 'text-5xl'
}

function getDividerWidthClass(title = '') {
  return title.length > TITLE_LONG ? 'w-4' : 'w-2'
}

const logoDark = new URL('../slidev-theme-amarula/assets/logo-small-dark.svg', import.meta.url).href
const logoWhite = new URL('../slidev-theme-amarula/assets/logo-small-white.svg', import.meta.url).href
// The -ssc render: same drawing as tux-beethoven.png in every pixel except the
// screen, where the square wave's period visibly varies. That is spread
// spectrum, which is what the title promises, so the cover shows the modulated
// clock and not the constant one. The plain render stays in assets on purpose.
const tuxBeethoven = new URL('../assets/tux-beethoven-ssc.png', import.meta.url).href
</script>

<template>
  <div class="slidev-layout relative w-full h-full p-8 flex flex-col justify-between">

    <!-- Event Header -->
    <div class="text-3xl font-semibold">
      {{ $slidev.configs.event || '' }}
    </div>

    <!-- Main Content -->
    <div class="flex flex-row justify-center items-center space-x-16">

      <!-- Logo -->
      <img :src="isDark ? logoWhite : logoDark" class="w-64"
        alt="Amarula Logo" />

      <!-- Divider -->
      <div :class="[getDividerWidthClass($slidev.configs.title), 'bg-accent rounded-sm h-full mx-8']"></div>

      <!-- Text Content -->
      <div class="flex flex-col justify-center space-y-4 text-left">

        <!-- Title -->
        <div :class="[getTitleSizeClass($slidev.configs.title), 'font-bold leading-tight']">
          {{ $slidev.configs.title || '' }}
        </div>

        <!-- Author -->
        <div class="text-3xl font-medium">
          {{ $slidev.configs.author || '' }}
        </div>

        <!-- Website -->
        <a href="https://www.amarulasolutions.com/" target="_blank" rel="noopener"
          class="inline-flex items-center gap-2 text-2xl text-blue-500 underline !border-b-0">
          <mdi-web />
          www.amarulasolutions.com
        </a>
      </div>

    </div>

    <!-- Tux-Beethoven conducting a clock: nods to "A Clockwork Orange" via the
         Beethoven motif, with a modulated square wave on the music stand
         instead of a score -- the same emblem the EMI Mitigation and Q&A pages
         use, so the talk opens and closes on it. Sized in the 960x540 design canvas (Slidev scales it up 2x for
         a 1080p export), so keep it small or it swamps the logo. -->
    <img :src="tuxBeethoven"
      class="absolute right-6 bottom-4 h-44 pointer-events-none select-none"
      alt="Tux dressed as Beethoven conducting, with a square-wave clock signal whose period visibly varies on the music stand" />

    <!-- Footer: the talk's repository (Dario, 2026-09-16: the URL on the
         first page too, not only in Resources) and under it the licence
         line of the theme's cover -- repository first since 2026-09-17,
         the same order as the Q&A page's footer, and the same sizes (URL
         and icon text-lg, licence text-base). Since 2026-09-18 the
         repository is amarula/elce-2026-a-clockwork-frequency: the short
         name lets the link take text-lg, the size of the Q&A contacts, and
         the block is centred on the page as on the Q&A page (the
         pr-[120px] that kept the long URL off Tux-Beethoven is gone: the
         link ends 170 px, at 2x, before the cartoon). Same link idiom as
         the website above. -->
    <div class="text-center text-base font-light mt-4 space-y-1">
      <a href="https://github.com/amarula/elce-2026-a-clockwork-frequency"
        target="_blank" rel="noopener"
        class="inline-flex items-center gap-1.5 text-lg text-blue-500 underline !border-b-0 font-normal">
        <mdi-github class="text-lg" />
        github.com/amarula/elce-2026-a-clockwork-frequency
      </a>
      <div>Slides under Creative Commons license BY-SA 3.0.</div>
    </div>
  </div>
</template>
