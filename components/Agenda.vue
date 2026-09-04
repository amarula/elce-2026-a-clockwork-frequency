<script setup>
// The talk's outline, in one place. The Agenda slide renders it whole; each
// section divider renders it again with `current` set, so the audience sees the
// same list they were shown at the start with one section still lit. Keeping it
// a component rather than copied markup means the outline cannot drift between
// the agenda and the dividers -- there is only one copy to edit.
defineProps({
  // Index into SECTIONS of the section about to start, or null for the full
  // agenda with nothing dimmed.
  current: { type: Number, default: null },
})

const tiLogo = new URL('../assets/ti-logo.svg', import.meta.url).href
const nxpLogo = new URL('../assets/nxp-logo.svg', import.meta.url).href

// Vendor mark replaces the bullet, same idiom as the About Us slide. Brand
// colours, not the deck's chart palette: different semantic area. Marks come
// from each vendor's own site, so the hexes are theirs: TI #CC0000
// (ti.com/favicon.svg, a square mark - their full wordmark is 280x36 and
// unusable here), NXP tri-colour N/X/P #f9b500 / #0eafe0 / #69ca00
// (nxp.com/resources/images/nxp-logo.svg), ST #03234B via simple-icons.
// simple-icons' NXP glyph is the monochrome wordmark and throws the colour
// away, hence the local asset. Tux is logos:linux-tux, the drawn penguin in its
// own colours, and not simple-icons:linux: that one is a monochrome silhouette
// whose brand hex is #FCC624 -- the deck's own accent yellow, unreadable on
// white -- and a black mark among three coloured ones reads as an oversight
// rather than as a choice. It is 256x295, so it is sized by height and lets its
// width follow.
const SECTIONS = [
  { title: 'Understanding Spread Spectrum Clocking (SSC)' },
  {
    title: 'Linux SSC Case Studies',
    items: [
      { img: tiLogo, alt: 'Texas Instruments', size: 'h-8', label: 'AM33xx/AM43xx' },
      { st: true, label: 'STM32F4/STM32F7' },
      { img: nxpLogo, alt: 'NXP', size: 'h-5', label: 'i.MX8M Mini/Nano/Plus' },
    ],
  },
  {
    title: 'Towards Generic SSC Support',
    items: [
      // No vendor mark on the first item, a Tux instead: this is the
      // sub-section where SSC stops belonging to anyone's silicon. The two
      // that follow are NXP's, and the contrast is the point.
      { linux: true, label: 'Generic SSC' },
      { img: nxpLogo, alt: 'NXP', size: 'h-5', label: 'i.MX95' },
      { img: nxpLogo, alt: 'NXP', size: 'h-5', label: 'Back to i.MX8M' },
    ],
  },
  { title: 'Conclusions' },
]
</script>

<template>
  <!-- Left-aligned, with the bullets sitting on the title's own left edge so they
       form one vertical with the title and the accent rule under it. The 59px was
       measured off the render, not derived: the body slot starts at the layout's
       p-8 while the title is pushed right by the logo, and the gap between them is
       not expressible in the spacing scale. Re-measure if the theme's TopBar
       changes. -->
  <div class="flex justify-start pl-[59px]">
    <ul class="list-disc pl-5 text-2xl space-y-6 [&>li]:!my-0">
      <!-- Sections other than the current one fade rather than change colour, so
           the "you are here" reading survives a colour-blind viewer and a
           projector that crushes hue. -->
      <li v-for="(section, i) in SECTIONS" :key="section.title"
          :class="current !== null && current !== i ? 'opacity-30' : ''">
        {{ section.title }}
        <!-- The w-16 slot is what keeps the text column straight: the marks have
             very different aspect ratios (TI and ST square, NXP 2.9:1, Tux taller
             than wide), so they are
             sized by optical weight - NXP shorter but wider - and left-aligned in
             one fixed-width box instead of sitting inline. -->
        <ul v-if="section.items" class="list-none pl-6 mt-2 text-lg [&>li]:!my-0 space-y-2">
          <li v-for="item in section.items" :key="item.label" class="flex items-center gap-3">
            <span class="w-16 shrink-0 flex items-center">
              <simple-icons-stmicroelectronics v-if="item.st" class="w-8 h-8 text-[#03234B]" />
              <logos-linux-tux v-else-if="item.linux" class="h-8 w-auto" />
              <img v-else :src="item.img" :class="item.size" :alt="item.alt" />
            </span>{{ item.label }}
          </li>
        </ul>
      </li>
    </ul>
  </div>
</template>
