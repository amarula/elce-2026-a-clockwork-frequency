---
theme: ./slidev-theme-amarula
title: "A Clockwork Frequency: Bringing Spread Spectrum to the Linux Clock Subsystem"
author: Dario Binacchi
event: ELCE 2026
drawings:
  persist: false
transition: slide-left
mdc: true
# No copy button on code blocks: they are exhibits to read, not source to
# take away, and some of them -- the ssc_program() body on the AM33xx slide --
# are pseudocode that would not compile if anyone did take it. Slidev gates
# the button on this with a v-if, so it leaves the DOM entirely.
codeCopy: false
# How the code pages are built, for anyone reading this file:
# - code panels are hand-laid HTML, not fenced blocks: one <div> per source
#   line, indentation as &nbsp; runs, tabs expanded to 8, line breaks where
#   the kernel file breaks them; bold marks the names the page is about;
# - the grey labels in the left margin ("eyebrows") are grid cells that sit
#   beside the line they name -- an empty <div></div> is a cell left blank;
# - a body with an explicit h-[440px] is pinned to the top on purpose: the
#   theme centres a short body vertically otherwise;
# - an HTML comment next to a code line explains why the line looks wrong
#   but is not.
fonts:
  sans: Roboto
  serif: Roboto Slab
  mono: Fira Code
---

---
title: About Us - Amarula Solutions
---

::title::

About Us - Amarula Solutions

::body::

<div class="flex flex-row justify-around">
  <div class="flex flex-col justify-center items-center h-full">
    <ul class="flex flex-col gap-4 text-2xl">
      <li class="font-semibold">
        Software Consulting Across Europe
        <ul class="text-lg font-normal">
          <li>Offices in multiple European countries</li>
          <li>Focused on mobile apps, cloud platforms, and embedded systems</li>
        </ul>
      </li>
      <li class="font-semibold">
        Full-Stack Embedded Expertise
        <ul class="text-lg font-normal">
          <li>From bootloaders & kernels to UI applications</li>
          <li>Deep knowledge of Android & Linux OS</li>
        </ul>
      </li>
      <li class="font-semibold">
        Open Source at our Core
        <ul class="text-lg font-normal">
          <li>Active upstream contributions</li>
          <li>Solutions built for security and long-term maintainability</li>
        </ul>
      </li>
    </ul>
  </div>
  <div class="flex flex-col space-y-2">
    <img src="./assets/amarula-offices-map.svg" class="w-54 h-54 rounded-xl shadow p-2" alt="Amarula offices map" />
    <div class="flex flex-col items-start gap-1 mt-4">
      <a href="mailto:info@amarulasolutions.com" class="inline-flex items-center gap-2 text-lg text-blue-500 underline !border-b-0">
        <mdi-email />
        info@amarulasolutions.com
      </a>
      <a href="www.amarulasolutions.com" class="inline-flex items-center gap-2 text-lg text-blue-500 underline !border-b-0">
        <mdi-web />
        www.amarulasolutions.com
      </a>
    </div>
  </div>
</div>

---
title: About Us - Dario Binacchi
---

::title::

About Us - Dario Binacchi

::body::

<div class="flex flex-row justify-around">
  <div class="flex flex-col justify-center items-center h-full">
    <ul class="flex flex-col gap-4 text-3xl font-medium">
      <li class="flex items-center gap-4">
        <img src="./assets/buildroot_logo.png" class="w-10 h-10" alt="Buildroot logo" />
        Buildroot
      </li>
      <li class="flex items-center gap-4">
        <img src="./assets/yocto_icon.png" class="w-10 h-10" alt="Yocto logo" />
        Yocto
      </li>
      <li class="flex items-center gap-4">
        <logos-linux-tux class="w-10 h-10" />
        Linux
      </li>
      <li class="flex items-center gap-4">
        <img src="./assets/uboot_logo.png" class="w-10 h-10" alt="U-Boot logo" />
        U-Boot
      </li>
      <li class="flex items-center gap-4">
        <img src="./assets/zephyr_icon.png" class="w-10 h-10" alt="Zephyr logo" />
        Zephyr
      </li>
    </ul>
  </div>
  <div class="flex flex-col space-y-2">
    <img src="./assets/dario-binacchi-photo-white-background.jpeg" alt="Binacchi-avatar" class="w-54 h-54 rounded-xl shadow object-cover" />
    <div class="flex flex-col items-start gap-1 mt-4">
      <a href="mailto:dario.binacchi@amarulasolutions.com" class="inline-flex items-center gap-2 text-lg text-blue-500 underline !border-b-0">
        <mdi-email />
        dario.binacchi@amarulasolutions.com
      </a>
      <a href="https://passgat.github.io/" class="inline-flex items-center gap-2 text-lg text-blue-500 underline !border-b-0">
        <mdi-github />
        https://passgat.github.io/
      </a>
    </div>
  </div>
</div>

---
title: Agenda
---

::title::

Agenda

::body::

<Agenda />

---
title: Understanding SSC - Sine Wave
---

::title::

Understanding SSC - Sine Wave

::body::

<div class="flex flex-col items-center gap-6">
  <div class="text-2xl text-center max-w-3xl">
    The only waveform at a <strong>single</strong>, <strong>exact</strong> <strong>frequency</strong>
  </div>
  <div class="flex flex-row items-center justify-center gap-4">
    <img src="./assets/sine-wave-time-domain.png" class="max-w-md rounded shadow" alt="100 MHz sine wave in the time domain" />
    <img src="./assets/sine-wave-single-frequency.png" class="max-w-md rounded shadow" alt="Sine wave spectrum: a single frequency line" />
  </div>
</div>

---
title: Understanding SSC - Digital Clock
---

::title::

Understanding SSC - Digital Clock

::body::

<div class="flex flex-col items-center gap-6">
  <div class="text-2xl text-center max-w-3xl">
    A sum of sine waves: the <strong>fundamental</strong> plus its <strong>harmonics</strong>
  </div>
  <div class="flex flex-row items-center justify-center gap-4">
    <img src="./assets/square-wave-time-domain.png" class="max-w-md rounded shadow" alt="100 MHz square wave in the time domain" />
    <img src="./assets/square-wave-spectrum.png" class="max-w-md rounded shadow" alt="Square wave spectrum: fundamental plus odd harmonics" />
  </div>
</div>

---
title: Understanding SSC - Real Digital Clock
---

::title::

Understanding SSC - Real Digital Clock

::body::

<div class="flex flex-col items-center gap-6">
  <div class="text-2xl text-center max-w-3xl">
    finite edges, duty cycle &ne; 50%
  </div>
  <img src="./assets/clock-ideal-vs-real-spectrum.png" class="max-w-3xl rounded shadow" alt="Ideal vs real clock spectrum: even harmonics and faster high-frequency rolloff" />
</div>

---
title: Understanding SSC - EMI
---

::title::

Understanding SSC - EMI

::body::

<div class="flex flex-col items-center gap-4">
  <ul class="list-disc pl-5 text-2xl space-y-4 max-w-4xl">
    <li>A digital clock: energy spikes at the fundamental and its harmonics</li>
    <li>PCB traces: unintentional antennas radiating that energy</li>
    <li>Nearby devices: can be disturbed</li>
  </ul>
  <img src="./assets/antenna-radiation-diagram.png" class="max-w-xl rounded shadow" alt="Clock signal traveling down a PCB trace that acts as an unintentional antenna, radiating energy toward a nearby device that becomes disturbed" />
</div>

---
title: Understanding SSC - How Do We Fix It ?
---

::title::

Understanding SSC - How Do We Fix It ?

::body::

<div class="flex flex-col items-center gap-6">
  <div class="text-2xl text-center max-w-3xl">
    <strong>Drop</strong> the peak below the limit <strong>enabling</strong> <strong>SSC</strong>
  </div>
  <img src="./assets/victim-band-threshold.png" class="max-w-2xl rounded shadow" alt="Spectrum with five victim device bands and an emission limit; peaks at 100 and 300 MHz exceed the limit, marked with a red cross and an overall EMC: FAIL badge" />
</div>

---
title: Understanding SSC - What Is It ?
---

::title::

Understanding SSC - What Is It ?

::body::

<div class="flex flex-col items-center gap-6">
  <div class="text-2xl text-center max-w-3xl">
    A technique to spread the spectral energy over a band of frequencies
  </div>
  <img src="./assets/ssc-spread-spectrum.png" class="max-w-lg rounded shadow" alt="Non-spread clock spectrum: a single sharp spike, versus spread spectrum clocking: the same energy spread over a band, with a lower peak" />
</div>

---
title: Understanding SSC - Fixed
---

::title::

Understanding SSC - Fixed

::body::

<div class="flex flex-col items-center gap-6">
  <img src="./assets/victim-band-threshold-ssc.png" class="max-w-2xl rounded shadow" alt="Same spectrum as before, but with SSC enabled: every peak is now a wider spread band, dropped by 14 to 21 dB depending on the harmonic, all five devices and all five peaks show a green check, and the overall badge reads EMC: PASS" />
</div>

---
title: Understanding SSC - A New Issue ?
---

::title::

Understanding SSC - A New Issue ?

::body::

<div class="flex flex-col items-center gap-6">
  <div class="text-2xl text-center max-w-3xl">
    Energy can now reach previously unaffected frequency bands
  </div>
  <img src="./assets/victim-band-zoom.png" class="max-w-2xl rounded shadow" alt="Zoomed view from 96 to 120 MHz: the fundamental now spreads from 98 to 102 MHz, and the slice from 101 to 102 MHz falls inside Device B's 101-118 MHz operating band, which the single non-spread line at 100 MHz never touched" />
</div>

---
title: Understanding SSC - How Does It Work ?
---

::title::

Understanding SSC - How Does It Work ?

::body::

<div class="flex flex-col items-center h-[446px]">
  <ul class="list-disc pl-5 mt-[23px] text-2xl space-y-3 max-w-4xl">
    <li>The clock frequency is <strong>frequency-modulated</strong> around its nominal value</li>
    <li><strong>Four</strong> parameters configure the spread:
      <ul class="list-none pl-0 mt-2 space-y-1">
        <li class="flex items-start gap-3">
          <mdi-arrow-up-down-bold class="w-10 h-10 shrink-0 text-[#fdcb0e]" />
          <span>Spreading <strong>depth</strong></span>
        </li>
        <li class="flex items-start gap-3">
          <mdi-minus-thick class="w-10 h-10 shrink-0 text-[#fdcb0e]" />
          <span>Modulation <strong>rate</strong></span>
        </li>
        <li class="flex items-start gap-3">
          <mdi-arrow-up-down-bold class="w-10 h-10 shrink-0 text-[#fdcb0e]" />
          <span>Modulation <strong>profile</strong>: Triangular, Sinusoidal or Hershey-kiss</span>
        </li>
        <li class="flex items-start gap-3">
          <mdi-swap-horizontal-bold class="w-10 h-10 shrink-0 text-[#fdcb0e]" />
          <span><strong>Spread type</strong>: Down, Center or Up</span>
        </li>
      </ul>
    </li>
    <li>The total energy remains <strong>unchanged</strong></li>
  </ul>
  <div class="mt-auto flex items-center justify-center gap-4 text-2xl">
    <mdi-alert class="w-11 h-11 text-[#fdcb0e] shrink-0" />
    <span><b>Increases clock jitter</b> <span class="text-gray-400">&mdash;</span> <span class="text-gray-600">not suitable for timing-sensitive peripherals</span></span>
  </div>
</div>

---
title: Understanding SSC - In Action
---

::title::

Understanding SSC - In Action

::body::

<div class="flex flex-col items-center h-[446px]">
  <img src="./assets/ssc-modulation-parameters.png" class="max-h-[385px] w-auto rounded shadow" alt="Four configurations of the same 100 MHz clock, one per row, each listed on the left and then shown as frequency against time and as the resulting spectrum. Every setting a row changes from the row above is boxed in its list. Row one, depth plus or minus 1 percent, 5 kilohertz rate, sinusoidal profile, center spread: the sweep lingers at its turning points and the band grows horns at its edges, peak 8.6 dB down. Row two switches the profile to triangular: constant sweep rate, a flat band from 99 to 101 megahertz, and the best result on the slide at 11.2 dB down. Row three changes two settings at once, the depth to plus or minus 0.5 percent and the spread type to down: the band halves in width and moves to 99 to 100 megahertz, sitting entirely below the nominal frequency, and the shallower spread gives back reduction, down to 8.2 dB. Row four again changes two, the rate to 15 kilohertz and the spread type to up: the sweep is visibly three times faster in the time panel, the band moves to 100 to 101 megahertz, and the peak is unchanged at 8.2 dB, because neither the rate nor the spread type touches it" />
  <div class="flex-1 flex items-center justify-center gap-4 text-2xl pt-3">
    <mdi-scale-balance class="w-11 h-11 text-[#fdcb0e] shrink-0" />
    <span><b>Total energy unchanged</b> <span class="text-gray-400">&mdash;</span> <span class="text-gray-600">half the band, twice the density</span></span>
    <span class="flex items-center gap-2 text-sm text-gray-500 ml-2"><span>low</span><span class="inline-block w-[110px] h-[13px] rounded-sm" style="background: linear-gradient(90deg, #F7E3B0, #E69F00, #9C5F00)"></span><span>high</span></span>
  </div>
</div>

---
title: Linux SSC Case Studies
---

::title::

Linux SSC Case Studies

::body::

<Agenda :current="1" />

---
title: AM33xx/AM43xx - Hardware
---

::title::

AM33xx/AM43xx - Hardware

::body::

<div class="flex flex-col gap-6">
  <div class="text-2xl text-center">
    SSC is supported for the <b>DISP</b> and <b>MPU</b> PLLs
  </div>

  <img src="./assets/am33xx-dpll-ssc.png" class="max-h-[320px] w-auto self-center" alt="Block diagram. Along the top, two lines saying that M is CM_CLKSEL.DPLL_MULT and N is CM_CLKSEL.DPLL_DIV plus one. Below them a reference clock enters a PLL whose output is the input times M over N, and leaves as the output clock. Under the PLL an SSC block drives an arrow back up into it, so the modulation happens inside the PLL rather than after it; the arrow is broken by an open switch labelled CM_CLKMODE.SSC_EN. The SSC block lists the same four knobs as the earlier parameter slide, each against the register that carries it: depth in CM_SSC_DELTAMSTEP, rate in CM_SSC_MODFREQDIV, type in CM_CLKMODE.SSC_DOWNSPREAD where 0 is center spread and 1 is down spread, and profile greyed out because it is not configurable: it is triangular, fixed in silicon. Beside the SSC block, a note reads: two dedicated registers and two control bits" />

  <div class="flex items-center justify-center gap-4 text-2xl">
    <mdi-hand-pointing-right class="w-11 h-11 text-[#fdcb0e] shrink-0" />
    <span>Enabling SSC restricts the valid range of the PLL multiplier (M)</span>
  </div>
</div>

---
title: AM33xx/AM43xx - Linux Integration
---

::title::

AM33xx/AM43xx - Linux Integration

::body::

<div class="flex flex-col gap-3 pl-[59px] pr-10 pt-[7px] h-[446px]">
  <div class="relative rounded-lg border border-gray-300 px-4 py-0.5 mb-2">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
    <span class="inline-block rounded-full bg-[#3AA83A]" style="width: 0.8em; height: 0.8em; position: relative; top: 0.02em; margin-right: 0.15em"></span>
    Upstream status
    <span class="font-mono font-normal normal-case tracking-normal text-gray-500">Add am33xx/am43xx spread spectrum clock support</span>
  </div>
    <div class="flex items-baseline gap-4 text-lg">
      <span><b>Mar 2021</b></span>
      <span class="text-gray-400">&rarr;</span>
      <span><b>v7 Jun 2021</b></span>
      <span class="text-gray-400">&rarr;</span>
      <span><b>Merged</b></span>
      <span class="text-gray-400">&rarr;</span>
      <span><b>Linux 5.14</b></span>
      <span class="text-gray-400">&middot;</span>
      <span class="text-base"><span class="text-gray-500">author</span> <b>Dario Binacchi</b></span>
    </div>
  </div>

  <div class="relative rounded-lg border border-gray-300 px-4 py-1">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      <span class="font-mono normal-case font-normal tracking-normal text-gray-500 [font-variant-ligatures:none]">Documentation/devicetree/bindings/clock/ti/dpll.txt</span>
    </div>
    <div class="grid grid-cols-[auto_1fr] gap-x-6 gap-y-0 text-[13px] leading-[1.15] items-baseline">
      <div class="font-mono">ti,ssc-deltam</div>
      <div>spreading depth, in tenths of a percent</div>
      <div class="font-mono">ti,ssc-modfreq-hz</div>
      <div>modulation rate</div>
      <div class="font-mono">ti,ssc-downspread</div>
      <div>spread type, boolean &mdash; down-spread instead of center</div>
      <div class="font-mono">ti,min-div</div>
      <div>floor for N, so the rounded M stays in range <span class="text-gray-500">&mdash;</span> <b>not about EMI at all</b></div>
    </div>
  </div>

  <div class="relative rounded-lg border border-gray-300 px-4 pt-2 pb-1 mt-2">
  <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
    <span class="font-mono normal-case font-normal tracking-normal text-gray-500">drivers/clk/ti/dpll3xxx.c</span>
  </div>
    <div class="grid grid-cols-[185px_1fr] gap-x-5 font-mono text-[11.5px] leading-[1.27] whitespace-nowrap [font-variant-ligatures:none]">
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; on rate change</div>
      <div class="text-gray-500">int&nbsp;<b>omap3_noncore_dpll_set_rate</b>(struct&nbsp;clk_hw&nbsp;*hw,&nbsp;unsigned&nbsp;long&nbsp;rate,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unsigned&nbsp;long&nbsp;parent_rate)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ret&nbsp;=&nbsp;<b>omap3_noncore_dpll_program</b>(clk,&nbsp;freqsel);</div>
      <div></div>
      <div class="h-1.5"></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; after M, N calculation</div>
      <div class="text-gray-500">static&nbsp;int&nbsp;<b>omap3_noncore_dpll_program</b>(struct&nbsp;clk_hw_omap&nbsp;*clk,&nbsp;u16&nbsp;freqsel)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(dd-&gt;ssc_enable_mask)</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#22863a">omap3_noncore_dpll_ssc_program</b>(clk);</div>
      <div></div>
      <div class="h-1.5"></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">3 &mdash; SSC setup</div>
      <div class="text-gray-500">static&nbsp;void&nbsp;<b style="color:#22863a">omap3_noncore_dpll_ssc_program</b>(struct&nbsp;clk_hw_omap&nbsp;*clk)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ctrl&nbsp;|=&nbsp;dd-&gt;ssc_enable_mask;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(dd-&gt;<b style="color:#22863a">ssc_downspread</b>)</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ctrl&nbsp;|=&nbsp;dd-&gt;ssc_downspread_mask;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mod_freq_divider&nbsp;=</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(ref_rate&nbsp;/&nbsp;dd-&gt;<b style="color:#22863a">last_rounded_n</b>)&nbsp;/&nbsp;(4&nbsp;*&nbsp;dd-&gt;<b style="color:#22863a">ssc_modfreq</b>);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;deltam_step&nbsp;=&nbsp;dd-&gt;<b style="color:#22863a">last_rounded_m</b>&nbsp;*&nbsp;dd-&gt;<b style="color:#22863a">ssc_deltam</b>;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti_clk_ll_ops-&gt;clk_writel(v,&nbsp;&amp;dd-&gt;ssc_deltam_reg);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti_clk_ll_ops-&gt;clk_writel(ctrl,&nbsp;&amp;dd-&gt;control_reg);</div>
    </div>
  </div>
</div>

---
title: AM33xx/AM43xx - SSC In Action
---

::title::

AM33xx/AM43xx - SSC In Action

::body::

<div class="flex flex-col gap-4">
  <div class="text-2xl text-center mb-2">
    Custom board: two panels, two overlays
  </div>

<div class="grid grid-cols-2 gap-6 items-start pl-[59px] pr-10">
<div class="relative rounded-lg border border-gray-300 px-4 pt-2 pb-1 [font-variant-ligatures:none]">
<div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
<span class="font-mono font-normal normal-case tracking-normal text-gray-500">LCD panel 800x480 @ 33 MHz &middot; SSC: &plusmn;11.4 %, 6 kHz</span>
</div>
    <div class="font-mono text-[10.5px] leading-[1.35]">
      <div class="text-gray-500">fragment@2&nbsp;{</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;target&nbsp;=&nbsp;&lt;&amp;display_timings_timing&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__overlay__&nbsp;{</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hactive&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;800&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vactive&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;480&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hback-porch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;46&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hfront-porch&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;210&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hsync-len&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;20&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vback-porch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;23&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vfront-porch&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;22&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vsync-len&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;10&gt;;</div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clock-frequency&nbsp;=&nbsp;&lt;33000000&gt;;</b></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hsync-active&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;0&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vsync-active&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;0&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;};</div>
      <div class="text-gray-500">};</div>
      <div class="h-2"></div>
      <div class="text-gray-500">fragment@6&nbsp;{</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;target&nbsp;=&nbsp;&lt;&amp;dpll_disp_ck&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__overlay__&nbsp;{</div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti,min-div&nbsp;=&nbsp;&lt;40&gt;;</b></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti,ssc-modfreq-hz&nbsp;=&nbsp;&lt;6000&gt;;</b></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti,ssc-deltam&nbsp;=&nbsp;&lt;114&gt;;</b></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;};</div>
      <div class="text-gray-500">};</div>
    </div>
</div>

<div class="relative rounded-lg border border-gray-300 px-4 pt-2 pb-1 [font-variant-ligatures:none]">
<div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
<span class="font-mono font-normal normal-case tracking-normal text-gray-500">LCD panel 800x600 @ 40 MHz &middot; SSC: &plusmn;2.9 %, 10 kHz</span>
</div>
    <div class="font-mono text-[10.5px] leading-[1.35]">
      <div class="text-gray-500">fragment@2&nbsp;{</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;target&nbsp;=&nbsp;&lt;&amp;display_timings_timing&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__overlay__&nbsp;{</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hactive&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;800&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vactive&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;600&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hback-porch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;46&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hfront-porch&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;210&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hsync-len&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;20&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vback-porch&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;15&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vfront-porch&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;13&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vsync-len&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;10&gt;;</div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clock-frequency&nbsp;=&nbsp;&lt;40000000&gt;;</b></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hsync-active&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;0&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;vsync-active&nbsp;&nbsp;&nbsp;&nbsp;=&nbsp;&lt;0&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;};</div>
      <div class="text-gray-500">};</div>
      <div class="h-2"></div>
      <div class="text-gray-500">fragment@6&nbsp;{</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;target&nbsp;=&nbsp;&lt;&amp;dpll_disp_ck&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;__overlay__&nbsp;{</div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti,min-div&nbsp;=&nbsp;&lt;12&gt;;</b></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti,ssc-modfreq-hz&nbsp;=&nbsp;&lt;10000&gt;;</b></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ti,ssc-deltam&nbsp;=&nbsp;&lt;29&gt;;</b></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;};</div>
      <div class="text-gray-500">};</div>
    </div>
</div>
</div>

</div>

---
title: AM33xx/AM43xx - Design Notes
---

::title::

AM33xx/AM43xx - Design Notes

::body::

<div class="flex flex-col justify-center h-full pl-[59px] pr-10">
  <div class="relative rounded-2xl border-2 border-[#fdcb0e] bg-[#fef7dc] px-10 py-8">
    <span class="absolute -top-4 left-4 text-4xl leading-none">&#128204;</span>
    <ul class="list-disc pl-6 text-2xl space-y-6 [&>li]:!my-0 [&>li]:!leading-snug">
      <li>
        <b>Clock-specific DT nodes</b> allow easy and precise SSC configuration
      </li>
      <li>
        <b>No profile DT property</b>
      </li>
      <li>
        <b>SoC-specific DT property</b> required
        (<span class="font-mono text-2xl whitespace-nowrap [font-variant-ligatures:none]">ti,min-div</span>)
      </li>
    </ul>
  </div>
</div>

---
title: STM32F4/STM32F7 - Hardware
---

::title::

STM32F4/STM32F7 - Hardware

::body::

<div class="flex flex-col gap-6">
  <div class="text-2xl text-center">
    SSC is only supported for the <b>main</b> PLL
  </div>

  <img src="./assets/stm32f4-pll-ssc.png" class="max-h-[320px] w-auto self-center" alt="Block diagram: an input clock f-in enters a PLL and the output clock f-out leaves it. The PLL box carries nothing but its name -- the multiply and divide ratio is not on this figure. Under the PLL an SSC block drives an arrow back up into it, through an open switch labelled RCC_SSCGR.SSCGEN. The SSC block lists the same four knobs as the earlier parameter slide, each against the field that carries it: depth in RCC_SSCGR.INCSTEP, rate in RCC_SSCGR.MODPER, type in RCC_SSCGR.SPREADSEL where 0 is center spread and 1 is down spread, and profile greyed out because it is not configurable: it is triangular, fixed in silicon. Beside the SSC block, a note reads: one dedicated register, four fields" />

</div>

---
title: STM32F4/STM32F7 - Linux Integration
---

::title::

STM32F4/STM32F7 - Linux Integration

::body::

<div class="flex flex-col gap-3 pl-[59px] pr-10 pt-[7px] h-[446px]">
  <div class="relative rounded-lg border border-gray-300 px-4 py-0.5 mb-2">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      <span class="inline-block rounded-full bg-[#3AA83A]" style="width: 0.8em; height: 0.8em; position: relative; top: 0.02em; margin-right: 0.15em"></span>
      Upstream status
      <span class="font-mono font-normal normal-case tracking-normal text-gray-500">Support spread spectrum clocking for stm32f{4,7} platforms</span>
    </div>
    <div class="flex items-baseline gap-4 text-lg">
      <span><b>5 Jan 2025</b></span>
      <span class="text-gray-400">&rarr;</span>
      <span><b>v4 14 Jan 2025</b></span>
      <span class="text-gray-400">&rarr;</span>
      <span><b>Merged</b></span>
      <span class="text-gray-400">&rarr;</span>
      <span><b>Linux 6.14</b></span>
      <span class="text-gray-400">&middot;</span>
      <span class="text-base"><span class="text-gray-500">author</span> <b>Dario Binacchi</b></span>
    </div>
  </div>

  <div class="relative rounded-lg border border-gray-300 px-4 py-1">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      <span class="font-mono font-normal normal-case tracking-normal text-gray-500 [font-variant-ligatures:none]">Documentation/devicetree/bindings/clock/st,stm32-rcc.yaml</span>
    </div>
    <div class="grid grid-cols-[auto_1fr] gap-x-6 gap-y-0 text-[13px] leading-[1.15] items-baseline">
      <div class="font-mono">st,ssc-moddepth-permyriad</div>
      <div>spreading depth, in hundredths of a percent</div>
      <div class="font-mono">st,ssc-modfreq-hz</div>
      <div>modulation rate</div>
      <div class="font-mono">st,ssc-modmethod</div>
      <div>spread type, string &mdash; <span class="font-mono">"center-spread"</span> or <span class="font-mono">"down-spread"</span></div>
    </div>
  </div>

  <div class="relative rounded-lg border border-gray-300 px-4 pt-2 pb-1 mt-2">
  <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
    <span class="font-mono font-normal normal-case tracking-normal text-gray-500">drivers/clk/clk-stm32f4.c</span>
  </div>
    <div class="grid grid-cols-[185px_1fr] gap-x-5 font-mono text-[11.5px] leading-[1.33] whitespace-nowrap [font-variant-ligatures:none]">
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; on init</div>
      <div class="text-gray-500">static&nbsp;void&nbsp;__init&nbsp;<b>stm32f4_rcc_init</b>(struct&nbsp;device_node&nbsp;*np)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(!<b style="color:#22863a">stm32f4_pll_ssc_parse_dt</b>(np,&nbsp;&amp;ssc_conf))</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#22863a">stm32f4_pll_init_ssc</b>(pll_vco_hw,&nbsp;&amp;ssc_conf);</div>
      <div></div>
      <div class="h-1.5"></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; on rate change</div>
      <div class="text-gray-500">static&nbsp;int&nbsp;<b>stm32f4_pll_set_rate</b>(struct&nbsp;clk_hw&nbsp;*hw,&nbsp;unsigned&nbsp;long&nbsp;rate,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unsigned&nbsp;long&nbsp;parent_rate)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(pll-&gt;ssc_enable)</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#22863a">stm32f4_pll_set_ssc</b>(hw,&nbsp;parent_rate,&nbsp;<b style="color:#22863a">n</b>);</div>
      <div></div>
      <div class="h-1.5"></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">3 &mdash; SSC setup</div>
      <div class="text-gray-500">static&nbsp;void&nbsp;<b style="color:#22863a">stm32f4_pll_set_ssc</b>(struct&nbsp;clk_hw&nbsp;*hw,&nbsp;unsigned&nbsp;long&nbsp;parent_rate,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unsigned&nbsp;int&nbsp;<b style="color:#22863a">ndiv</b>)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;modeper&nbsp;=&nbsp;DIV_ROUND_CLOSEST(parent_rate,&nbsp;4&nbsp;*&nbsp;ssc-&gt;<b style="color:#22863a">mod_freq</b>);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;incstep&nbsp;=&nbsp;DIV_ROUND_CLOSEST(((1&nbsp;&lt;&lt;&nbsp;15)&nbsp;-&nbsp;1)&nbsp;*&nbsp;ssc-&gt;<b style="color:#22863a">mod_depth</b>&nbsp;*&nbsp;<b style="color:#22863a">ndiv</b>,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5&nbsp;*&nbsp;10000&nbsp;*&nbsp;modeper);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(ssc-&gt;<b style="color:#22863a">mod_type</b>)</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sscgr&nbsp;|=&nbsp;STM32F4_RCC_SSCGR_SPREADSEL;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;writel(sscgr,&nbsp;base&nbsp;+&nbsp;STM32F4_RCC_SSCGR);</div>
    </div>
  </div>
</div>

---
title: STM32F4/STM32F7 - SSC In Action
---

::title::

STM32F4/STM32F7 - SSC In Action

::body::

<div class="flex flex-col gap-4">
  <div class="text-2xl text-center mb-10">
    Reset clock controller setup
  </div>

  <div class="flex justify-center">
<div class="relative rounded-lg border border-gray-300 px-8 py-5 [font-variant-ligatures:none]">
<div class="absolute -top-4 left-4 bg-white px-2 text-base font-semibold uppercase tracking-[0.15em] text-gray-700">
<span class="font-mono font-normal normal-case tracking-normal text-gray-500">SSC: 2 %, 10 kHz, center-spread</span>
</div>
    <div class="font-mono text-[17px] leading-[1.5]">
      <div class="text-gray-500">&amp;rcc {</div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;st,ssc-moddepth-permyriad&nbsp;=&nbsp;&lt;200&gt;;</b></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;st,ssc-modfreq-hz&nbsp;=&nbsp;&lt;10000&gt;;</b></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;st,ssc-modmethod&nbsp;=&nbsp;"center-spread";</b></div>
      <div class="text-gray-500">};</div>
    </div>
</div>
  </div>
</div>

---
title: STM32F4/STM32F7 - Design Notes
---

::title::

STM32F4/STM32F7 - Design Notes

::body::

<div class="flex flex-col justify-center h-full pl-[59px] pr-10">
  <div class="relative rounded-2xl border-2 border-[#fdcb0e] bg-[#fef7dc] px-10 py-8">
    <span class="absolute -top-4 left-4 text-4xl leading-none">&#128204;</span>
    <ul class="list-disc pl-6 text-2xl space-y-2 [&>li]:!my-0 [&>li]:!leading-snug">
      <li>
        SSC properties are <b>defined in the RCC node</b>
        <ul class="list-[circle] pl-6 mt-1 text-lg [&>li]:!my-0">
          <li>Main PLL is <b>implicitly referenced</b></li>
        </ul>
      </li>
      <li class="pt-7">
        <b>No profile DT property</b>
      </li>
      <li class="pt-7">
        <b>Different DT representations</b> across SoCs
        <div class="grid grid-cols-[auto_auto_auto_auto] gap-x-4 gap-y-1.5 mt-4 text-sm items-baseline [font-variant-ligatures:none]">
          <div class="text-xs uppercase tracking-wider text-gray-500">Parameter</div>
          <div class="text-xs uppercase tracking-wider text-gray-500">AM33xx/AM43xx</div>
          <div class="text-xs uppercase tracking-wider text-gray-500">STM32F4/STM32F7</div>
          <div></div>
          <div>Spreading depth</div>
          <div class="font-mono whitespace-nowrap">ti,ssc-deltam</div>
          <div class="font-mono whitespace-nowrap">st,ssc-moddepth-permyriad</div>
          <div class="whitespace-nowrap text-xs">&#9888;&#65039; Different name/unit</div>
          <div>Modulation rate</div>
          <div class="font-mono whitespace-nowrap">ti,ssc-modfreq-hz</div>
          <div class="font-mono whitespace-nowrap">st,ssc-modfreq-hz</div>
          <div class="whitespace-nowrap text-xs">&#9989; Same name</div>
          <div>Spread type</div>
          <div class="font-mono whitespace-nowrap">ti,ssc-downspread</div>
          <div class="font-mono whitespace-nowrap">st,ssc-modmethod</div>
          <div class="whitespace-nowrap text-xs">&#9888;&#65039; Different representation</div>
        </div>
      </li>
    </ul>
  </div>
</div>

---
title: i.MX8M Mini/Nano/Plus - Hardware
---

::title::

i.MX8M Mini/Nano/Plus - Hardware

::body::

<div class="flex flex-col gap-6">
  <div class="text-2xl text-center">
    SSC is supported for <b>audio</b>, <b>video</b> and <b>DRAM</b> PLLs
  </div>

  <img src="./assets/imx8m-pll-ssc.png" class="max-h-[330px] w-auto self-center" alt="Block diagram. An input clock f-in enters a PLL and the output clock f-out leaves it. The PLL box carries nothing but its name -- the multiply and divide ratio is not on this figure. Under the PLL an SSC block drives an arrow back up into it through an open switch labelled SSCG_CTRL.SSCG_ENABLE. The SSC block lists the same four knobs as the earlier parameter slide, each against the field that carries it: depth in SSCG_CTRL.MRAT_CTL, rate in SSCG_CTRL.MFREQ_CTL, type in SSCG_CTRL.SEL_PF where 0 is down spread, 1 is up spread and 2 is center spread, and profile greyed out because it is fixed in silicon. Beside the SSC block, a note reads: one dedicated register, four fields" />
</div>

---
title: i.MX8M Mini/Nano/Plus - Linux Integration
---

::title::

i.MX8M Mini/Nano/Plus - Linux Integration

::body::

<div class="flex flex-col h-[440px] pl-[59px] pr-10 pt-2">

  <div class="relative rounded-lg border border-gray-300 px-4 py-2">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      <span class="inline-block rounded-full bg-[#CC0000]" style="width: 0.8em; height: 0.8em; position: relative; top: 0.02em; margin-right: 0.15em"></span>
      Upstream status
      <span class="font-mono font-normal normal-case tracking-normal text-gray-500">Support spread spectrum clocking for i.MX8{M,N,P} PLLs</span>
    </div>
    <div class="grid grid-cols-[auto_auto] gap-x-4 items-baseline">
      <div class="flex items-baseline gap-4 text-lg whitespace-nowrap">
        <span><b>Sep 2024</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>v9 Jan 2025</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>Superseded</b></span>
        <span class="text-gray-400">&middot;</span>
      </div>
      <div class="text-base"><span class="text-gray-500">author</span> <b>Dario Binacchi</b></div>
      <div></div>
      <div class="text-sm whitespace-nowrap"><span class="text-gray-500">reviewers</span> <b>Krzysztof Kozlowski</b> <span class="text-gray-500">3 Reviewed-by, 2 Acked-by</span></div>
      <div></div>
      <div class="text-sm whitespace-nowrap"><span class="invisible">reviewers</span> <b>Peng Fan</b> <span class="text-gray-500">6 Reviewed-by</span></div>
    </div>
  </div>

  <div class="relative rounded-lg border border-gray-300 px-8 pt-3 pb-3 mt-6">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      DT Design
    </div>
    <div class="text-xs font-semibold uppercase tracking-[0.15em] text-gray-400 mb-1.5">1 &mdash; i.MX8M</div>
    <div class="text-xl">
      <ul class="list-disc pl-8 space-y-1 [&>li]:!my-0 [&>li]:!leading-snug">
        <li>DT clock controller node (CCM)</li>
        <li>four SSC PLLs</li>
      </ul>
    </div>
    <div class="border-t border-gray-200 mt-2 pt-1.5"></div>
    <div class="text-xs font-semibold uppercase tracking-[0.15em] text-gray-400 mb-1.5">2 &mdash; Existing designs</div>
    <div class="grid grid-cols-[auto_auto_1fr] gap-x-6 gap-y-1 text-xl items-baseline">
      <div class="font-semibold whitespace-nowrap pl-2">AM33xx/AM43xx</div>
      <div class="text-[#CC0000] font-bold">&#10007;</div>
      <div class="whitespace-nowrap">PLL is a DT node</div>
      <div class="font-semibold whitespace-nowrap pl-2 pt-1">STM32F4/STM32F7</div>
      <div class="text-[#3AA83A] font-bold pt-1">&#10003;</div>
      <div class="whitespace-nowrap pt-1">DT clock controller node (RCC)</div>
      <div></div>
      <div class="text-[#CC0000] font-bold">&#10007;</div>
      <div class="whitespace-nowrap">one PLL, implicitly referenced</div>
    </div>
    <div class="border-t border-gray-200 mt-2 pt-1.5"></div>
    <div class="text-xs font-semibold uppercase tracking-[0.15em] text-gray-400 mb-1.5">3 &mdash; Proposed solution</div>
    <div class="text-xl font-semibold pl-2">Extend the STM32F4/STM32F7 design to explicitly reference the SSC PLLs</div>
  </div>

</div>

---
title: i.MX8M Mini/Nano/Plus - Linux Integration
---

::title::

i.MX8M Mini/Nano/Plus - Linux Integration

::body::

<div class="flex flex-col gap-[22px] pl-[59px] pr-10 justify-center h-full">

  <div class="relative rounded-lg border border-gray-300 px-6 pt-4 pb-3">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
      v3
      <span class="font-mono font-normal tracking-normal text-gray-500">Documentation/devicetree/bindings/clock/imx8m-clock.yaml</span>
    </div>
    <div class="font-mono text-[14px] leading-[1.45] [font-variant-ligatures:none]">
      <div class="text-gray-500">clock-controller@30380000 {</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;compatible = "fsl,imx8mm-ccm";</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;reg = &lt;0x30380000 0x10000&gt;;</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;#clock-cells = &lt;1&gt;;</div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;clocks = &lt;&amp;osc_32k&gt;, &lt;&amp;osc_24m&gt;, &lt;&amp;clk_ext1&gt;, &lt;&amp;clk_ext2&gt;,</b></div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk_ext3&gt;, &lt;&amp;clk_ext4&gt;;</b></div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;clock-names = "osc_32k", "osc_24m", "clk_ext1", "clk_ext2",</b></div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"clk_ext3", "clk_ext4";</b></div>
      <div class="relative">
        <div class="text-[#22863a]"><b>&nbsp;&nbsp;&nbsp;&nbsp;fsl,ssc-clocks = &lt;&amp;clk IMX8MM_AUDIO_PLL1&gt;,</b></div>
        <div class="text-[#22863a]"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk IMX8MM_VIDEO_PLL1&gt;;</b></div>
        <div class="text-[#22863a]"><b>&nbsp;&nbsp;&nbsp;&nbsp;fsl,ssc-modfreq-hz = &lt;6818&gt;, &lt;2419&gt;;</b></div>
        <div class="text-[#22863a]"><b>&nbsp;&nbsp;&nbsp;&nbsp;fsl,ssc-modrate-percent = &lt;3&gt;, &lt;7&gt;;</b></div>
        <div class="text-[#22863a]"><b>&nbsp;&nbsp;&nbsp;&nbsp;fsl,ssc-modmethod = "down-spread", "center-spread";</b></div>
        <div v-click="1" class="absolute right-8 top-1/2 -translate-y-1/2 text-[#CC0000] text-[112px] leading-none font-bold">&#10007;</div>
      </div>
    </div>
  </div>

  <div v-click="1" class="relative rounded-lg border border-gray-300 px-6 py-5">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      Maintainer&rsquo;s response
    </div>
    <img v-click="1" src="./assets/tux-dtc-stop.png" class="absolute right-5 top-1/2 -translate-y-1/2 h-[96px] w-auto" alt="Cartoon Tux wearing a yellow hard hat marked with a device tree symbol, one flipper raised in a stop gesture, the other holding a red STOP sign" />
    <div class="pr-36 text-lg italic leading-snug">
      &ldquo;How is it possible that you change spread spectrum of some clocks from
      main Clock Controller, while <b>this device is not a consumer of them</b>?&rdquo;
    </div>
    <div class="text-sm text-gray-500 mt-1">Krzysztof Kozlowski</div>
  </div>

</div>

---
title: i.MX8M Mini/Nano/Plus - Linux Integration
---

::title::

i.MX8M Mini/Nano/Plus - Linux Integration

::body::

<div class="flex flex-col pl-[59px] pr-10 pt-2">

  <div class="relative rounded-lg border border-gray-300 px-8 pt-3 pb-3">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
      v4 <span class="font-normal">DESIGN</span>
    </div>
    <div class="text-xs font-semibold uppercase tracking-[0.15em] text-gray-400 mb-2">1 &mdash; The hardware</div>
    <div class="pl-2 pr-4">
      <svg viewBox="-26 8 980 140" class="w-full" role="img" aria-label="Block diagram. Two oscillators, osc_32k and osc_24m, each fork into two arrows: one enters the anatop block at address 0x30360000, the other runs underneath it and up into the CCM block at address 0x30380000. A third input, clk_ext1 to 4, runs straight into the CCM from below. Out of the anatop, four separate arrows cross to the CCM, labelled audio_pll1, audio_pll2, video_pll and dram_pll. Out of the CCM, one arrow leaves to peripheral clocks.">
        <defs>
          <marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#9ca3af" />
          </marker>
        </defs>
        <g fill="none" stroke="#9ca3af" stroke-width="1.6" marker-end="url(#ah)">
          <path d="M 46 40 H 108" />
          <path d="M 46 62 H 108" />
          <path d="M 46 40 H 84 V 118 H 645 V 110" />
          <path d="M 46 62 H 92 V 128 H 670 V 110" />
          <path d="M 68 138 H 695 V 110" />
          <path d="M 230 32 H 618" />
          <path d="M 230 54 H 618" />
          <path d="M 230 76 H 618" />
          <path d="M 230 98 H 618" />
          <path d="M 740 62 H 778" />
        </g>
        <g fill="#ffffff" stroke="#6b7280" stroke-width="1.6">
          <rect x="110" y="16" width="120" height="92" rx="6" />
          <rect x="620" y="16" width="120" height="92" rx="6" />
        </g>
        <g fill="#111827" text-anchor="middle" style="font-weight:600">
          <text x="170" y="52" style="font-size:20px">anatop</text>
          <text x="680" y="52" style="font-size:20px">CCM</text>
        </g>
        <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="#9ca3af" text-anchor="middle">
          <text x="170" y="74" style="font-size:11px">0x30360000</text>
          <text x="170" y="90" style="font-size:11px">size 0x10000</text>
          <text x="680" y="74" style="font-size:11px">0x30380000</text>
          <text x="680" y="90" style="font-size:11px">size 0x10000</text>
        </g>
        <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="#6b7280">
          <text x="-18" y="44" style="font-size:14px">osc_32k</text>
          <text x="-18" y="66" style="font-size:14px">osc_24m</text>
          <text x="-18" y="142" style="font-size:14px">clk_ext1&#8230;4</text>
          <text x="424" y="26" text-anchor="middle" style="font-size:14px">audio_pll1</text>
          <text x="424" y="48" text-anchor="middle" style="font-size:14px">audio_pll2</text>
          <text x="424" y="70" text-anchor="middle" style="font-size:14px">video_pll</text>
          <text x="424" y="92" text-anchor="middle" style="font-size:14px">dram_pll</text>
        </g>
        <text x="786" y="67" fill="#6b7280" style="font-size:16px">peripheral clocks</text>
      </svg>
    </div>
    <div class="border-t border-gray-200 mt-4 pt-2"></div>
    <div class="text-xs font-semibold uppercase tracking-[0.15em] text-gray-400 mb-2">2 &mdash; Current Linux integration</div>
    <div class="grid grid-cols-[auto_1fr] gap-x-4 gap-y-0.5 items-baseline pl-2 mb-1">
      <div class="text-[#3AA83A] font-bold text-base">&#10003;</div>
      <div class="text-base">DT bindings and DTS are <b>right</b></div>
      <div class="text-[#CC0000] font-bold text-base">&#10007;</div>
      <div class="text-base">no anatop driver &mdash; <b>all clocks are defined and registered by the CCM driver</b>, PLLs too</div>
    </div>
    <div class="pl-2 pr-4">
      <svg viewBox="-26 8 980 140" class="w-full" role="img" aria-label="The same frame as the hardware figure, with the real connections. The oscillators and the external clocks run past the anatop straight into the CCM. The four PLL wires between anatop and CCM are gone; in their place a single dashed arrow runs backwards from the CCM into the anatop, looking up the compatible fsl,imx8mp-anatop, mapping its registers with devm_of_iomap and registering the PLL into the CCM's own clock array. The anatop box is dashed and labelled no driver. Out of the CCM one arrow leaves to all clocks, PLLs included.">
        <defs>
          <marker id="ah2" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#9ca3af" />
          </marker>
        </defs>
        <g fill="none" stroke="#9ca3af" stroke-width="1.6" marker-end="url(#ah2)">
          <path d="M 46 40 H 84 V 118 H 645 V 110" />
          <path d="M 46 62 H 92 V 128 H 670 V 110" />
          <path d="M 68 138 H 695 V 110" />
          <path d="M 740 62 H 778" />
        </g>
        <path d="M 618 62 H 232" fill="none" stroke="#9ca3af" stroke-width="1.6" stroke-dasharray="5 4" marker-end="url(#ah2)" />
        <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="#9ca3af" text-anchor="middle">
          <text x="425" y="40" style="font-size:11px">np = of_find_compatible_node(&#8230;, <tspan style="font-weight:700;fill:#6b7280">"fsl,imx8mp-anatop"</tspan>);</text>
          <text x="425" y="56" style="font-size:11px">anatop_base = devm_of_iomap(dev, np, &#8230;);</text>
        </g>
        <rect x="110" y="16" width="120" height="92" rx="6" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.6" stroke-dasharray="5 4" />
        <rect x="620" y="16" width="120" height="92" rx="6" fill="#ffffff" stroke="#6b7280" stroke-width="1.6" />
        <text x="170" y="48" text-anchor="middle" fill="#9ca3af" style="font-size:20px;font-weight:600">anatop</text>
        <text x="170" y="74" text-anchor="middle" fill="#9ca3af" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" style="font-size:10px;font-weight:700">"fsl,imx8mp-anatop"</text>
        <text x="680" y="52" text-anchor="middle" fill="#111827" style="font-size:20px;font-weight:600">CCM</text>
        <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="#9ca3af" text-anchor="middle">
          <text x="680" y="72" style="font-size:11px">clk-imx8mm.c</text>
          <text x="680" y="86" style="font-size:11px">clk-imx8mn.c</text>
          <text x="680" y="100" fill="#6b7280" style="font-size:11px;font-weight:700">clk-imx8mp.c</text>
        </g>
        <g font-family="ui-monospace, SFMono-Regular, Menlo, monospace" fill="#6b7280">
          <text x="-18" y="44" style="font-size:14px">osc_32k</text>
          <text x="-18" y="66" style="font-size:14px">osc_24m</text>
          <text x="-18" y="142" style="font-size:14px">clk_ext1&#8230;4</text>
        </g>
        <text x="786" y="60" fill="#6b7280" style="font-size:16px">all clocks</text>
        <text x="786" y="80" fill="#6b7280" font-family="ui-monospace, SFMono-Regular, Menlo, monospace" style="font-size:11px;font-weight:700">PLLs included</text>
      </svg>
    </div>
    <div class="border-t border-gray-200 mt-4 pt-2"></div>
    <div class="text-xs font-semibold uppercase tracking-[0.15em] text-gray-400 mb-2">3 &mdash; Proposed solution</div>
    <div class="text-xl font-semibold pl-2">Give the PLLs <b>its</b> owner &mdash; the <b>anatop</b> &mdash; so the CCM can <b>consume</b> them</div>
  </div>

</div>

---
title: i.MX8M Mini/Nano/Plus - Linux Integration
---

::title::

i.MX8M Mini/Nano/Plus - Linux Integration

::body::

<div class="flex flex-col pl-[59px] pr-10 pt-3">

  <div class="relative rounded-lg border border-gray-300 px-8 pt-5 pb-5">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
      v9
      <span class="font-mono font-normal tracking-normal text-gray-500">23 patches &middot; 19 files &middot; <span style="color:#22863a">+1975</span> <span style="color:#CC0000">&minus;610</span></span>
    </div>
    <div class="grid grid-cols-[auto_1fr] gap-x-6 gap-y-1.5 items-center [font-variant-ligatures:none]">
      <div class="col-span-2 mt-0 mb-1 text-xs font-semibold uppercase tracking-[0.15em] text-gray-400">Drivers
        <span class="font-mono font-normal normal-case tracking-normal text-gray-400">drivers/clk/imx/</span>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">Makefile</div>
      <div class="flex items-center gap-3">
        <div class="flex h-[13px]"><div class="rounded-l-sm h-full" style="width:1px;background:#22863a"></div><div class="rounded-r-sm h-full" style="width:1px;background:#CC0000"></div></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+3</span>&nbsp;<span style="color:#CC0000">&minus;3</span></div>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">clk-imx8m{m,n,p}-anatop.c</div>
      <div class="flex items-center gap-3">
        <div class="h-[13px] rounded-sm" style="width:326px;background:#22863a"></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+875</span></div>
        <div class="text-[13px] text-gray-500 whitespace-nowrap"><b class="text-black">new driver</b> &mdash; one per SoC</div>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">clk-imx8m{m,n,p}.c</div>
      <div class="flex items-center gap-3">
        <div class="flex h-[13px]"><div class="rounded-l-sm h-full" style="width:212px;background:#22863a"></div><div class="rounded-r-sm h-full" style="width:218px;background:#CC0000"></div></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+569</span>&nbsp;<span style="color:#CC0000">&minus;586</span></div>
      </div>
      <div class="font-mono text-[13px] font-bold whitespace-nowrap">clk-pll14xx.c</div>
      <div class="flex items-center gap-3">
        <div class="h-[13px] rounded-sm" style="width:50px;background:#22863a"></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span class="font-bold" style="color:#22863a">+134</span></div>
        <div class="text-[13px] text-gray-500 whitespace-nowrap"><b class="text-black">SSC support</b></div>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">clk.c, clk.h</div>
      <div class="flex items-center gap-3">
        <div class="h-[13px] rounded-sm" style="width:12px;background:#22863a"></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+33</span></div>
      </div>
      <div class="col-span-2 mt-4 mb-1 text-xs font-semibold uppercase tracking-[0.15em] text-gray-400">Bindings
        <span class="font-mono font-normal normal-case tracking-normal text-gray-400">Documentation/devicetree/bindings/clock/ &middot; include/dt-bindings/clock/</span>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">fsl,imx8m-anatop.yaml</div>
      <div class="flex items-center gap-3">
        <div class="flex h-[13px]"><div class="rounded-l-sm h-full" style="width:19px;background:#22863a"></div><div class="rounded-r-sm h-full" style="width:1px;background:#CC0000"></div></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+52</span>&nbsp;<span style="color:#CC0000">&minus;1</span></div>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">imx8m-clock.yaml</div>
      <div class="flex items-center gap-3">
        <div class="flex h-[13px]"><div class="rounded-l-sm h-full" style="width:25px;background:#22863a"></div><div class="rounded-r-sm h-full" style="width:2px;background:#CC0000"></div></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+68</span>&nbsp;<span style="color:#CC0000">&minus;6</span></div>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">imx8m{m,n,p}-clock.h</div>
      <div class="flex items-center gap-3">
        <div class="flex h-[13px]"><div class="rounded-l-sm h-full" style="width:79px;background:#22863a"></div><div class="rounded-r-sm h-full" style="width:3px;background:#CC0000"></div></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+212</span>&nbsp;<span style="color:#CC0000">&minus;8</span></div>
      </div>
      <div class="col-span-2 mt-4 mb-1 text-xs font-semibold uppercase tracking-[0.15em] text-gray-400">Device trees
        <span class="font-mono font-normal normal-case tracking-normal text-gray-400">arch/arm64/boot/dts/freescale/</span>
      </div>
      <div class="font-mono text-[13px]  whitespace-nowrap">imx8m{m,n,p,q}.dtsi</div>
      <div class="flex items-center gap-3">
        <div class="flex h-[13px]"><div class="rounded-l-sm h-full" style="width:11px;background:#22863a"></div><div class="rounded-r-sm h-full" style="width:2px;background:#CC0000"></div></div>
        <div class="font-mono text-[12px] whitespace-nowrap"><span style="color:#22863a">+29</span>&nbsp;<span style="color:#CC0000">&minus;6</span></div>
      </div>
    </div>
  </div>

  <div class="text-2xl font-semibold mt-5 pl-2"><span class="text-gray-400">v3</span>&nbsp;8 patches&nbsp;<span class="text-gray-400">&rarr;</span>&nbsp;<span class="text-gray-400">v9</span>&nbsp;23 patches</div>

</div>

---
title: i.MX8M Mini/Nano/Plus - Linux Integration
---

::title::

i.MX8M Mini/Nano/Plus - Linux Integration

::body::

<div class="flex flex-col gap-2 pl-[59px] pr-10 pt-2">
  <div class="grid grid-cols-2 gap-x-6 items-stretch">
    <div class="relative h-full rounded-lg border border-gray-300 px-5 pt-4 pb-2">
      <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
        v9
        <span class="font-mono font-normal tracking-normal text-gray-500">arch/arm64/boot/dts/freescale/imx8mp.dtsi</span>
      </div>
      <div class="font-mono text-[10px] leading-[1.32] [font-variant-ligatures:none] text-gray-500">
        <div>clk: clock-controller@30380000 {</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;clocks = &lt;&amp;osc_32k&gt;, &lt;&amp;osc_24m&gt;,</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk_ext1&gt;, &lt;&amp;clk_ext2&gt;,</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk_ext3&gt;, &lt;&amp;clk_ext4&gt;,</div>
        <div style="color:#22863a;font-weight:700">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;anatop IMX8MP_ANATOP_AUDIO_PLL1&gt;,</div>
        <div style="color:#22863a;font-weight:700">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;anatop IMX8MP_ANATOP_AUDIO_PLL2&gt;,</div>
        <div style="color:#22863a;font-weight:700">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;anatop IMX8MP_ANATOP_DRAM_PLL&gt;,</div>
        <div style="color:#22863a;font-weight:700">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;anatop IMX8MP_ANATOP_VIDEO_PLL&gt;;</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;clock-names = "osc_32k", "osc_24m",</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"clk_ext1", "clk_ext2",</div>
        <div>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"clk_ext3", "clk_ext4",</div>
        <div style="color:#22863a;font-weight:700">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"audio_pll1", "audio_pll2",</div>
        <div style="color:#22863a;font-weight:700">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"dram_pll", "video_pll";</div>
        <div>};</div>
      </div>
      <div v-click="1" class="absolute right-4 bottom-3 text-[#CC0000] text-[72px] leading-none font-bold">&#10007;</div>
    </div>
    <div class="h-full">
    <div class="relative h-full rounded-lg border border-gray-300 px-5 pt-4 pb-12">
      <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
        v9 custom board
        <span class="font-mono font-normal tracking-normal text-gray-500 text-[10px]">SSC: 6818 Hz, 3 %, down-spread</span>
      </div>
      <div class="font-mono text-[10px] leading-[1.32] [font-variant-ligatures:none]">
        <div>&amp;clk {</div>
        <div class="pl-4 text-gray-400">/* audio_pll1, audio_pll2, dram_pll, video_pll */</div>
        <div class="pl-4">fsl,ssc-modfreq-hz = &lt;0&gt;, &lt;0&gt;, &lt;0&gt;, <b style="color:#22863a">&lt;6818&gt;</b>;</div>
        <div class="pl-4">fsl,ssc-modrate-percent = &lt;0&gt;, &lt;0&gt;, &lt;0&gt;, <b style="color:#22863a">&lt;3&gt;</b>;</div>
        <div class="pl-4">fsl,ssc-modmethod = "", "", "", <b style="color:#22863a">"down-spread"</b>;</div>
        <div>};</div>
      </div>
      <div v-click="1" class="absolute right-4 bottom-3 text-[#CC0000] text-[72px] leading-none font-bold">&#10007;</div>
    </div>
    </div>
  </div>
  <div v-click="1" class="relative rounded-lg border border-gray-300 px-6 pt-3 pb-2 mt-2">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      Maintainer&rsquo;s response
    </div>
    <img v-click="1" src="./assets/tux-dtc-stop.png" class="absolute right-5 top-1/2 -translate-y-1/2 h-[150px] w-auto" alt="Cartoon Tux wearing a yellow hard hat marked with a device tree symbol, one flipper raised in a stop gesture, the other holding a red STOP sign" />
    <div class="pr-40 text-base italic leading-snug space-y-1">
      <div>&ldquo;Ehh, so it looks that nine versions of this patches for iMX8 and NXP comes with generic bindings for iMX9.</div>
      <div>Please work with Peng and unify approach for entire iMX and <b>use common bindings</b>.&rdquo;</div>
    </div>
    <div class="text-sm text-gray-500 mt-1">Krzysztof Kozlowski</div>
    <div class="mr-40 mt-3 pt-2 border-t border-gray-200 [font-variant-ligatures:none]">
      <div class="text-[10px] font-semibold uppercase tracking-[0.15em] text-gray-400 mb-1">24 January 2025 &middot; UTC</div>
      <div class="grid grid-cols-[auto_1fr_auto] gap-x-4 gap-y-0.5 font-mono whitespace-nowrap">
        <div class="text-[10px] text-gray-400">12:31</div>
        <div class="text-[10px] text-gray-400">github.com/devicetree-org/dt-schema/pull/154</div>
        <div class="text-[10px] text-gray-400">Peng Fan</div>
        <div class="text-[11px] font-bold text-black">13:46</div>
        <div class="text-[10.5px] text-black">[PATCH v9 00/23] Support spread spectrum clocking for i.MX8M PLLs</div>
        <div class="text-[11px] text-black">Krzysztof Kozlowski</div>
        <div class="text-[10px] text-gray-400">14:25</div>
        <div class="text-[10px] text-gray-400">[PATCH 0/3] clk: Support spread spectrum and use it in clk-scmi</div>
        <div class="text-[10px] text-gray-400">Peng Fan</div>
      </div>
    </div>
  </div>

</div>

---
title: Towards Generic SSC Support
---

::title::

Towards Generic SSC Support

::body::

<Agenda :current="2" />

---
title: Generic SSC - DT Schema
---

::title::

Generic SSC - DT Schema

::body::

<div class="flex flex-col h-[440px] pl-[59px] pr-10 pt-[4px]">
  <div class="relative rounded-lg border border-gray-300 px-4 py-2">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      <span class="inline-block rounded-full bg-[#22863a]" style="width: 0.8em; height: 0.8em; position: relative; top: 0.02em; margin-right: 0.15em"></span>
      Upstream status
      <span class="font-mono font-normal normal-case tracking-normal text-gray-500">schemas: introduce assigned-clock-sscs</span>
    </div>
    <div class="grid grid-cols-[auto_auto] gap-x-4 items-baseline">
      <div class="flex items-baseline gap-4 text-lg whitespace-nowrap">
        <span><b>24 Jan 2025</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>Merged</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>v2025.08</b></span>
        <span class="text-gray-400">&middot;</span>
      </div>
      <div class="text-base"><span class="text-gray-500">author</span> <b>Peng Fan</b></div>
      <div class="font-mono text-xs whitespace-nowrap"><a href="https://github.com/devicetree-org/dt-schema/pull/154" class="text-blue-500 underline !border-b-0">github.com/devicetree-org/dt-schema/pull/154</a></div>
      <div class="text-sm whitespace-nowrap"><span class="text-gray-500">participants</span> <b>Krzysztof Kozlowski</b>, <b>Rob Herring</b>, <b>Dario Binacchi</b></div>
    </div>
  </div>
  <div class="relative rounded-lg border border-gray-300 px-6 pt-4 pb-2 mt-[20px]">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-mono text-gray-500">dtschema/schemas/clock/clock.yaml</div>
    <div class="grid grid-cols-[auto_1fr] gap-x-5 font-mono text-[10px] leading-[1.35] [font-variant-ligatures:none]">
      <div></div>
      <div class="text-gray-500">properties:</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;<b style="color:#22863a">assigned-clock-sscs</b>:</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;$ref:&nbsp;/schemas/types.yaml#/definitions/uint32-matrix</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; a list, one entry per clock</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;items:</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; three u32 values each</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;items:</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;description:&nbsp;<b style="color:#22863a">The&nbsp;modulation&nbsp;frequency</b></div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;description:&nbsp;<b style="color:#22863a">The&nbsp;modulation&nbsp;depth&nbsp;in&nbsp;permyriad</b></div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&nbsp;description:&nbsp;<b style="color:#22863a">The&nbsp;modulation&nbsp;method</b>,&nbsp;down-spread(3),</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;up-spread(2),&nbsp;center-spread(1),&nbsp;no-spread(0)</div>
      <div></div>
      <div>&nbsp;</div>
      <div></div>
      <div class="text-gray-500">dependentRequired:</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;assigned-clock-parents:&nbsp;&nbsp;&nbsp;[assigned-clocks]</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;assigned-clock-rates:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[assigned-clocks]</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;assigned-clock-rates-u64:&nbsp;[assigned-clocks]</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">3 &mdash; needs assigned-clocks</div>
      <div class="text-gray-500">&nbsp;&nbsp;<b style="color:#22863a">assigned-clock-sscs</b>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>[assigned-clocks]</b></div>
    </div>
  </div>
  <div class="mt-[13px] text-xl font-semibold">
    <span class="text-gray-400 line-through">consumer / producer</span>
    <svg viewBox="0 0 72 24" class="inline-block w-[72px] h-[24px] mx-3 align-middle" aria-hidden="true"><rect x="0" y="8.5" width="52" height="7" rx="2" fill="#fdcb0e"/><path d="M50 1 L71 12 L50 23 Z" fill="#fdcb0e"/></svg>
    <span>configuration</span>
  </div>
  <div class="mt-3 border-l-2 border-gray-300 pl-5">
    <div class="text-base italic leading-snug">&ldquo;<b>Configuration</b> of common clocks, which affect multiple consumer devices can be similarly specified in <b>the clock provider node</b>.&rdquo;</div>
    <div class="font-mono text-xs text-gray-800 mt-1">dtschema/schemas/clock/clock.yaml</div>
  </div>
</div>

---
title: Generic SSC - One More Callback
---

::title::

Generic SSC - One More Callback

::body::

<div class="flex flex-col h-[440px] pl-[59px] pr-10 pt-[8px]">
  <div class="relative rounded-lg border border-gray-300 px-4 py-2">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      <span class="inline-block rounded-full bg-[#22863a]" style="width: 0.8em; height: 0.8em; position: relative; top: 0.02em; margin-right: 0.15em"></span>
      Upstream status
      <span class="font-mono font-normal normal-case tracking-normal text-gray-500">clk: Support spread spectrum and use it in clk-scmi</span>
    </div>
    <div class="grid grid-cols-[auto_auto] gap-x-4 items-baseline">
      <div class="flex items-baseline gap-4 text-lg whitespace-nowrap">
        <span><b>Jan 2025</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>v10 Jun 2026</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>Merged 7.3</b></span>
        <span class="text-gray-400">&middot;</span>
      </div>
      <div class="text-base"><span class="text-gray-500">author</span> <b>Peng Fan</b></div>
      <div></div>
      <div class="text-sm whitespace-nowrap"><span class="text-gray-500">reviewers</span> <b>Brian Masney</b>, <b>Sebin Francis</b>, <b>Cristian Marussi</b></div>
    </div>
  </div>
  <div class="relative rounded-lg border border-gray-300 px-6 pt-2 pb-1 mt-[24px]">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-mono text-gray-500">include/linux/clk-provider.h</div>
    <div class="grid grid-cols-[185px_1fr] gap-x-5 font-mono text-[11px] leading-[1.42] whitespace-nowrap [font-variant-ligatures:none]">
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; SSC parameters</div>
      <div class="text-gray-500">struct&nbsp;<b style="color:#22863a">clk_spread_spectrum</b>&nbsp;{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;u32&nbsp;<b style="color:#22863a">modfreq_hz</b>;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;u32&nbsp;<b style="color:#22863a">spread_bp</b>;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enum&nbsp;clk_ssc_method&nbsp;<b style="color:#22863a">method</b>;</div>
      <div></div>
      <div class="text-gray-500">};</div>
      <div></div>
      <div class="h-4"></div>
      <div></div>
      <div class="text-gray-500">struct&nbsp;<b>clk_ops</b>&nbsp;{</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; driver callback</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;int&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(*<b style="color:#22863a">set_spread_spectrum</b>)(struct&nbsp;clk_hw&nbsp;*hw,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const&nbsp;struct&nbsp;clk_spread_spectrum&nbsp;*ss_conf);</div>
      <div></div>
      <div class="text-gray-500">};</div>
      <div></div>
      <div class="h-4"></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">3 &mdash; core API</div>
      <div class="text-gray-500">int&nbsp;<b style="color:#22863a">clk_hw_set_spread_spectrum</b>(struct&nbsp;clk_hw&nbsp;*hw,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const&nbsp;struct&nbsp;clk_spread_spectrum&nbsp;*ss_conf);</div>
    </div>
  </div>
  <div class="relative rounded-lg border border-gray-300 px-6 pt-2 pb-1 mt-[24px]">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-mono text-gray-500">drivers/clk/clk.c</div>
    <div class="grid grid-cols-[185px_1fr] gap-x-5 font-mono text-[11px] leading-[1.42] whitespace-nowrap [font-variant-ligatures:none]">
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; core</div>
      <div class="text-gray-500">int&nbsp;<b style="color:#22863a">clk_hw_set_spread_spectrum</b>(struct&nbsp;clk_hw&nbsp;*hw,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const&nbsp;struct&nbsp;clk_spread_spectrum&nbsp;*ss_conf)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div class="ml-[58px] text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">to</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(core-&gt;ops-&gt;<b style="color:#22863a">set_spread_spectrum</b>)</div>
      <div class="ml-[80px] text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">driver</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ret&nbsp;=&nbsp;core-&gt;ops-&gt;<b style="color:#22863a">set_spread_spectrum</b>(hw,&nbsp;ss_conf);</div>
    </div>
  </div>
</div>

---
title: Generic SSC - One More Call
---

::title::

Generic SSC - One More Call

::body::

<div class="flex flex-col pl-[59px] pr-10 pt-[5px] h-[446px]">
  <div class="relative rounded-lg border border-gray-300 px-4 pt-2 pb-2 mt-2">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-mono text-gray-500">drivers/clk/clk-conf.c</div>
    <div class="grid grid-cols-[185px_1fr] gap-x-5 font-mono text-[11px] leading-[1.3] whitespace-nowrap [font-variant-ligatures:none]">
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; early in clock setup</div>
      <div class="text-gray-500">int&nbsp;<b>of_clk_set_defaults</b>(struct&nbsp;device_node&nbsp;*node,&nbsp;bool&nbsp;clk_supplier)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; SSC through DT</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rc&nbsp;=&nbsp;<b style="color:#22863a">__set_clk_spread_spectrum</b>(node,&nbsp;clk_supplier);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rc&nbsp;=&nbsp;__set_clk_parents(node,&nbsp;clk_supplier);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;__set_clk_rates(node,&nbsp;clk_supplier);</div>
      <div></div>
      <div>&nbsp;</div>
      <div></div>
      <div class="text-gray-500">static&nbsp;int&nbsp;<b style="color:#22863a">__set_clk_spread_spectrum</b>(struct&nbsp;device_node&nbsp;*node,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;bool&nbsp;clk_supplier)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;u32&nbsp;elem_size&nbsp;=&nbsp;sizeof(struct&nbsp;clk_spread_spectrum);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;count&nbsp;=&nbsp;of_property_count_elems_of_size(node,&nbsp;"<b style="color:#22863a">assigned-clock-sscs</b>",</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;elem_size);</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">3 &mdash; load SSC parameters</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rc&nbsp;=&nbsp;of_property_read_u32_array(node,&nbsp;"<b style="color:#22863a">assigned-clock-sscs</b>",&nbsp;(u32&nbsp;*)<b style="color:#22863a">sscs</b>,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;count&nbsp;*&nbsp;3);</div>
      <div></div>
      <div>&nbsp;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;for&nbsp;(<b>index</b>&nbsp;=&nbsp;0;&nbsp;<b>index</b>&nbsp;&lt;&nbsp;count;&nbsp;<b>index</b>++)&nbsp;{</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">4 &mdash; SSC</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;struct&nbsp;clk_spread_spectrum&nbsp;*<b style="color:#22863a">conf</b>&nbsp;=&nbsp;&amp;<b style="color:#22863a">sscs</b>[<b>index</b>];</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(!conf-&gt;<b style="color:#22863a">modfreq_hz</b>&nbsp;&amp;&amp;&nbsp;!conf-&gt;<b style="color:#22863a">spread_bp</b>&nbsp;&amp;&amp;&nbsp;!conf-&gt;<b style="color:#22863a">method</b>)</div>
      <div class="ml-[50px] text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">to</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;continue;</div>
      <div class="ml-[72px] text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">clock</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rc&nbsp;=&nbsp;of_parse_phandle_with_args(node,&nbsp;"<b>assigned-clocks</b>",</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"#clock-cells",&nbsp;<b>index</b>,&nbsp;&amp;clkspec);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clk&nbsp;=&nbsp;of_clk_get_from_provider(&amp;clkspec);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;hw&nbsp;=&nbsp;__clk_get_hw(clk);</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">5 &mdash; the core call</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;rc&nbsp;=&nbsp;<b style="color:#22863a">clk_hw_set_spread_spectrum</b>(hw,&nbsp;<b style="color:#22863a">conf</b>);</div>
    </div>
  </div>
  <div class="mt-[22px] text-xl font-mono font-semibold">assigned-clock-sscs<span class="text-gray-400">[i]</span><svg viewBox="0 0 72 24" class="inline-block w-[72px] h-[24px] mx-3 align-middle" aria-hidden="true"><rect x="0" y="8.5" width="52" height="7" rx="2" fill="#fdcb0e"/><path d="M50 1 L71 12 L50 23 Z" fill="#fdcb0e"/></svg>assigned-clocks<span class="text-gray-400">[i]</span></div>
</div>

---
title: i.MX95 - Linux Integration
---

::title::

i.MX95 - Linux Integration

::body::
<div class="flex flex-col h-[446px] pl-[59px] pr-10 pt-[11px]">
  <div class="relative rounded-lg border border-gray-300 px-4 pt-2 pb-1">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
      v14
      <span class="font-mono font-normal tracking-normal text-gray-500">drivers/clk/clk-scmi-oem.c</span>
    </div>
    <div class="grid grid-cols-[150px_1fr] gap-x-5 font-mono text-[11.5px] leading-[1.55] whitespace-nowrap [font-variant-ligatures:none]">
      <div></div>
      <div class="text-gray-500">static&nbsp;const&nbsp;struct&nbsp;scmi_clk_oem&nbsp;scmi_clk_oem_imx&nbsp;=&nbsp;{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.query_ext_oem_feats&nbsp;=&nbsp;scmi_clk_imx_query_oem_feats,</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; registration</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.<b style="color:#22863a">set_spread_spectrum</b>&nbsp;=&nbsp;<b style="color:#22863a">scmi_clk_imx_set_spread_spectrum</b>,</div>
      <div></div>
      <div class="text-gray-500">};</div>
      <div></div>
      <div>&nbsp;</div>
      <div></div>
      <div class="text-gray-500">static&nbsp;int</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; driver callback</div>
      <div class="text-gray-500"><b style="color:#22863a">scmi_clk_imx_set_spread_spectrum</b>(struct&nbsp;clk_hw&nbsp;*hw,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const&nbsp;struct&nbsp;clk_spread_spectrum&nbsp;*ss_conf)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;struct&nbsp;scmi_clk&nbsp;*clk&nbsp;=&nbsp;to_scmi_clk(hw);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;u32&nbsp;<b style="color:#22863a">spread_pm</b>&nbsp;=&nbsp;ss_conf-&gt;<b style="color:#22863a">spread_bp</b>&nbsp;/&nbsp;10;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if&nbsp;(ss_conf-&gt;<b style="color:#22863a">method</b>&nbsp;==&nbsp;CLK_SPREAD_NO)&nbsp;{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;val&nbsp;=&nbsp;0;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;goto&nbsp;oem_set;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;val&nbsp;=&nbsp;FIELD_PREP(SCMI_CLOCK_IMX_SS_PERCENTAGE_MASK,&nbsp;<b style="color:#22863a">spread_pm</b>);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;val&nbsp;|=&nbsp;FIELD_PREP(SCMI_CLOCK_IMX_SS_MOD_FREQ_MASK,&nbsp;ss_conf-&gt;<b style="color:#22863a">modfreq_hz</b>);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;val&nbsp;|=&nbsp;SCMI_CLOCK_IMX_SS_ENABLE_MASK;</div>
      <div></div>
      <div class="text-gray-500">oem_set:</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ret&nbsp;=&nbsp;scmi_proto_clk_ops-&gt;<b>config_oem_set</b>(clk-&gt;ph,&nbsp;clk-&gt;id,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;SCMI_CLOCK_CFG_IMX_SSC,&nbsp;val,&nbsp;false);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return&nbsp;ret;</div>
      <div></div>
      <div class="text-gray-500">}</div>
    </div>
  </div>
</div>

---
title: Back to i.MX8M - Linux Integration
---

::title::

Back to i.MX8M - Linux Integration

::body::

<div class="flex flex-col pl-[59px] pr-10 pt-[1px] h-[446px]">
  <div class="relative rounded-lg border border-gray-300 px-4 py-1">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold uppercase tracking-[0.15em] text-gray-700">
      <span class="inline-block rounded-full bg-white border-[#B45309]" style="width: 0.8em; height: 0.8em; border-width: 2.5px; position: relative; top: 0.02em; margin-right: 0.15em"></span>
      Upstream status
      <span class="font-mono font-normal normal-case tracking-normal text-gray-500">Support spread spectrum clocking for i.MX8M PLLs</span>
    </div>
    <div class="grid grid-cols-[auto_auto] gap-x-4 items-baseline">
      <div class="flex items-baseline gap-4 text-lg">
        <span><b>v10 Aug 2026</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>v14 Sep 2026</b></span>
        <span class="text-gray-400">&rarr;</span>
        <span><b>Under review</b></span>
        <span class="text-gray-400">&middot;</span>
      </div>
      <div class="text-base"><span class="text-gray-500">author</span> <b>Dario Binacchi</b></div>
    </div>
  </div>
  <div class="relative rounded-lg border border-gray-300 px-6 pt-2 pb-1 mt-4">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-mono text-gray-500">drivers/clk/imx/clk-pll14xx.c</div>
    <div class="grid grid-cols-[150px_1fr] gap-x-5 font-mono text-[11px] leading-[1.1] whitespace-nowrap [font-variant-ligatures:none]">
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; registration</div>
      <div class="text-gray-500">static&nbsp;const&nbsp;struct&nbsp;clk_ops&nbsp;<b>clk_pll1443x_ops</b>&nbsp;=&nbsp;{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;.<b style="color:#22863a">set_spread_spectrum</b>&nbsp;=&nbsp;<b style="color:#22863a">clk_pll1443x_set_spread_spectrum</b>,</div>
      <div></div>
      <div>&nbsp;</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; driver callback</div>
      <div class="text-gray-500">static&nbsp;int&nbsp;<b style="color:#22863a">clk_pll1443x_set_spread_spectrum</b>(struct&nbsp;clk_hw&nbsp;*hw,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;const&nbsp;struct&nbsp;clk_spread_spectrum&nbsp;*<b style="color:#22863a">ss_conf</b>)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;div_ctl0&nbsp;=&nbsp;readl_relaxed(pll-&gt;base&nbsp;+&nbsp;DIV_CTL0);</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">3 &mdash; on init</div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#22863a">__clk_pll1443x_set_spread_spectrum</b>(hw,&nbsp;parent_rate,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FIELD_GET(PDIV_MASK,&nbsp;div_ctl0),</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FIELD_GET(MDIV_MASK,&nbsp;div_ctl0));</div>
      <div></div>
      <div class="h-1"></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">4 &mdash; on rate change</div>
      <div class="text-gray-500">static&nbsp;int&nbsp;<b>clk_pll1443x_set_rate</b>(struct&nbsp;clk_hw&nbsp;*hw,&nbsp;unsigned&nbsp;long&nbsp;drate,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unsigned&nbsp;long&nbsp;prate)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b style="color:#22863a">__clk_pll1443x_set_spread_spectrum</b>(hw,&nbsp;prate,&nbsp;rate.<b style="color:#22863a">pdiv</b>,&nbsp;rate.<b style="color:#22863a">mdiv</b>);</div>
      <div></div>
      <div class="h-1"></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">5 &mdash; SSC setup</div>
      <div class="text-gray-500">static&nbsp;void&nbsp;<b style="color:#22863a">__clk_pll1443x_set_spread_spectrum</b>(struct&nbsp;clk_hw&nbsp;*hw,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unsigned&nbsp;long&nbsp;parent_rate,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unsigned&nbsp;int&nbsp;<b style="color:#22863a">pdiv</b>,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;unsigned&nbsp;int&nbsp;<b style="color:#22863a">mdiv</b>)</div>
      <div></div>
      <div class="text-gray-500">{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mfr&nbsp;=&nbsp;div64_u64(parent_rate,&nbsp;(u64)conf-&gt;<b style="color:#22863a">modfreq_hz</b>&nbsp;*&nbsp;<b style="color:#22863a">pdiv</b>&nbsp;*&nbsp;BIT(5));</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mrr&nbsp;=&nbsp;(conf-&gt;<b style="color:#22863a">spread_bp</b>&nbsp;*&nbsp;<b style="color:#22863a">mdiv</b>&nbsp;*&nbsp;BIT(6))&nbsp;/&nbsp;(10000&nbsp;*&nbsp;mfr);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sscg_ctrl&nbsp;|=&nbsp;SSCG_ENABLE&nbsp;|&nbsp;FIELD_PREP(MFREQ_CTL_MASK,&nbsp;mfr)&nbsp;|</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FIELD_PREP(MRAT_CTL_MASK,&nbsp;mrr)&nbsp;|</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FIELD_PREP(SEL_PF_MASK,&nbsp;sel_pf);</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;writel_relaxed(sscg_ctrl,&nbsp;pll-&gt;base&nbsp;+&nbsp;SSCG_CTRL);</div>
    </div>
  </div>
  <div class="text-[18px] font-semibold mt-[24px] pl-2 whitespace-nowrap"><span class="text-gray-400">v9</span>&nbsp;23 patches&nbsp;19 files&nbsp;+1975<svg viewBox="0 0 72 24" class="inline-block w-[54px] h-[18px] mx-3 align-[-0.15em]" aria-hidden="true"><rect x="0" y="8.5" width="52" height="7" rx="2" fill="#fdcb0e"/><path d="M50 1 L71 12 L50 23 Z" fill="#fdcb0e"/></svg><span style="color:#22863a"><span class="text-gray-400">v14</span>&nbsp;1 patch&nbsp;1 file&nbsp;+103</span><span class="text-gray-400 ml-3">[ + 3 patches on merged SSC code ]</span></div>
</div>

---
title: Back to i.MX8M - SSC In Action
---

::title::

Back to i.MX8M - SSC In Action

::body::

<div class="flex flex-col h-[446px] pl-[59px] pr-10 pt-[17px] gap-[30px]">
  <div class="relative rounded-lg border border-gray-300 px-4 pt-3 pb-1">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
      <span class="font-mono font-normal tracking-normal text-gray-500">arch/arm64/boot/dts/freescale/imx8mp.dtsi</span>
    </div>
    <div class="grid grid-cols-[150px_1fr] gap-x-4 font-mono text-[12px] leading-[1.8] whitespace-nowrap [font-variant-ligatures:none]">
      <div></div>
      <div class="text-gray-500">clk:&nbsp;clock-controller@30380000&nbsp;{</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assigned-clocks&nbsp;=&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_A53_SRC&gt;,&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_A53_CORE&gt;,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_NOC&gt;,&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_NOC_IO&gt;,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_GIC&gt;;</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assigned-clock-rates&nbsp;=&nbsp;&lt;0&gt;,&nbsp;&lt;0&gt;,&nbsp;&lt;1000000000&gt;,</div>
      <div></div>
      <div class="text-gray-500">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;800000000&gt;,&nbsp;&lt;500000000&gt;;</div>
      <div></div>
      <div class="text-gray-500">};</div>
    </div>
  </div>
  <div class="relative rounded-lg border border-gray-300 px-4 pt-3 pb-1">
    <div class="absolute -top-3 left-4 bg-white px-2 text-xs font-semibold tracking-[0.15em] text-gray-700">
      custom board
      <span class="font-mono font-normal tracking-normal text-gray-500 text-[10px]">LVDS panel 1280x800 &middot; SSC: 6818 Hz, 3 %, down-spread</span>
    </div>
    <div class="grid grid-cols-[150px_1fr] gap-x-4 font-mono text-[12px] leading-[1.8] whitespace-nowrap [font-variant-ligatures:none]">
      <div></div>
      <div class="text-gray-500">&amp;clk&nbsp;{</div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">1 &mdash; the five, restated</div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assigned-clocks&nbsp;=&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_A53_SRC&gt;,&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_A53_CORE&gt;,</b></div>
      <div></div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_NOC&gt;,&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_NOC_IO&gt;,</b></div>
      <div></div>
      <div class="text-gray-500"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk&nbsp;IMX8MP_CLK_GIC&gt;,</b></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">2 &mdash; plus video PLL1</div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;&amp;clk&nbsp;IMX8MP_VIDEO_PLL1&gt;;</b></div>
      <div></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;assigned-clock-sscs&nbsp;=&nbsp;&lt;0&nbsp;0&nbsp;0&gt;,&nbsp;&lt;0&nbsp;0&nbsp;0&gt;,&nbsp;&lt;0&nbsp;0&nbsp;0&gt;,</b></div>
      <div></div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;0&nbsp;0&nbsp;0&gt;,&nbsp;&lt;0&nbsp;0&nbsp;0&gt;,</b></div>
      <div class="text-[10px] font-semibold uppercase tracking-[0.12em] text-gray-500 whitespace-nowrap">3 &mdash; video PLL1 setup</div>
      <div style="color:#22863a"><b>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;6818&nbsp;300&nbsp;CLK_SSC_DOWN_SPREAD&gt;;</b></div>
      <div></div>
      <div class="text-gray-500">};</div>
    </div>
  </div>
</div>

---
title: Conclusions - EMI Mitigation
---

::title::

Conclusions - EMI Mitigation

::body::

<div class="flex flex-col pl-[59px] pr-12 pt-0 h-[446px]">
  <div class="grid grid-cols-2 gap-12">
    <div class="flex flex-col items-center">
      <div class="text-3xl font-semibold mb-3">Rework the board</div>
      <img src="./assets/tux-hw-rework.png" class="h-[172px] w-auto" alt="Cartoon Tux in a yellow hard hat soldering a green circuit board at a workbench, magnifier lamp over the board" />
      <ul class="list-disc pl-5 text-lg text-gray-600 mt-2 space-y-1">
        <li>a new redesign cycle
          <ul class="list-[circle] pl-5 text-base space-y-0.5">
            <li>filtering, shielding, rerouting</li>
            <li>prototypes</li>
            <li>EMC scan again</li>
          </ul>
        </li>
        <li>an added cost on every unit shipped</li>
      </ul>
    </div>
    <div class="flex flex-col items-center">
      <div class="text-3xl font-semibold mb-3">Enable SSC</div>
      <img src="./assets/tux-beethoven-ssc.png" class="h-[172px] w-auto rounded-lg" alt="Cartoon Tux as Beethoven, wild grey hair and red scarf, conducting with a baton in front of a screen showing a square wave whose period visibly varies" />
      <ul class="list-disc pl-5 text-lg text-gray-600 mt-2 space-y-1">
        <li>embedded in many PLLs of modern SoCs</li>
        <li>a generic framework in Linux since 7.3</li>
        <li>requirements change? retune the configuration, not the board</li>
      </ul>
    </div>
  </div>
  <div class="flex items-center justify-center gap-4 mt-auto -mb-[8px] text-2xl font-semibold -ml-[59px] -mr-12">
    <mdi-hand-pointing-right class="w-11 h-11 text-[#fdcb0e] shrink-0" />
    If supported, try SSC first. Rework only if needed
  </div>
</div>

---
title: Conclusions - Timeline
---

::title::

Conclusions - Timeline

::body::

<div class="flex flex-col pl-8 pr-4 pt-1 h-[446px]">
  <div class="relative mt-0">
    <svg class="absolute left-0 -top-[12px] w-full h-[88px]" viewBox="0 0 1200 88" preserveAspectRatio="none" fill="none" aria-hidden="true">
      <line x1="48" y1="80" x2="1080" y2="80" stroke="#9ca3af" stroke-width="2.5" stroke-linecap="round" />
      <line x1="1092" y1="80" x2="1172" y2="80" stroke="#9ca3af" stroke-width="2.5" stroke-linecap="round" stroke-dasharray="2 9" />
      <polyline points="1170,73 1180,80 1170,87" stroke="#9ca3af" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" />
      <path d="M 360 34 C 540 4, 940 4, 1073 28" stroke="#c3c8d1" stroke-width="1.5" stroke-linecap="round" />
      <polyline points="1064,22 1074,30 1063,36" stroke="#c3c8d1" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
    </svg>
    <div class="relative grid grid-cols-5">
      <div class="flex flex-col items-center text-center">
        <div class="h-[60px] flex flex-col justify-end pb-2">
          <div class="text-base font-semibold">2021</div>
          <div class="text-xs">AM33xx/AM43xx</div>
        </div>
        <div class="w-4 h-4 rounded-full bg-[#22863a]"></div>
        <div class="pt-2 text-xs" style="color:#22863a">merged v5.14</div>
        <div class="pt-1 font-mono text-[9px] leading-[1.6] text-gray-500 whitespace-nowrap">
          <div>ti,ssc-modfreq-hz</div>
          <div>ti,ssc-deltam</div>
          <div>ti,ssc-downspread</div>
          <div>ti,min-div</div>
        </div>
      </div>
      <div class="flex flex-col items-center text-center">
        <div class="h-[60px] flex flex-col justify-end pb-2">
          <div class="text-base font-semibold">2024-25</div>
          <div class="text-xs">i.MX8M v1..v9</div>
        </div>
        <div class="w-4 h-4 rounded-full bg-gray-400"></div>
        <div class="pt-2 text-xs text-gray-500">superseded</div>
        <div class="pt-1 font-mono text-[9px] leading-[1.6] text-gray-500 whitespace-nowrap">
          <div>fsl,ssc-modfreq-hz</div>
          <div>fsl,ssc-modrate-percent</div>
          <div>fsl,ssc-modmethod</div>
        </div>
      </div>
      <div class="flex flex-col items-center text-center">
        <div class="h-[60px] flex flex-col justify-end pb-2">
          <div class="text-base font-semibold">2025</div>
          <div class="text-xs">STM32F4/STM32F7</div>
        </div>
        <div class="w-4 h-4 rounded-full bg-[#22863a]"></div>
        <div class="pt-2 text-xs" style="color:#22863a">merged v6.14</div>
        <div class="pt-1 font-mono text-[9px] leading-[1.6] text-gray-500 whitespace-nowrap">
          <div>st,ssc-modfreq-hz</div>
          <div>st,ssc-moddepth-permyriad</div>
          <div>st,ssc-modmethod</div>
        </div>
      </div>
      <div class="flex flex-col items-center text-center">
        <div class="h-[60px] flex flex-col justify-end pb-2">
          <div class="text-base font-bold">Aug 2026</div>
          <div class="text-xs font-semibold">Generic SSC &amp; i.MX95</div>
        </div>
        <div class="w-4 h-4 rounded-full bg-[#22863a] ring-4 ring-[#fdcb0e]"></div>
        <div class="pt-2 text-xs font-semibold" style="color:#22863a">merged 7.3</div>
        <div class="pt-1 font-mono text-[9px] leading-[1.6] text-gray-700 whitespace-nowrap">assigned-clock-sscs</div>
      </div>
      <div class="flex flex-col items-center text-center">
        <div class="h-[60px] flex flex-col justify-end pb-2">
          <div class="text-base font-semibold">Sep 2026</div>
          <div class="text-xs">i.MX8M v10..v14</div>
        </div>
        <div class="w-4 h-4 rounded-full bg-white border-[3px] border-[#B45309]"></div>
        <div class="pt-2 text-xs text-[#B45309]">under review</div>
        <div class="pt-1 font-mono text-[9px] leading-[1.6] text-gray-500 whitespace-nowrap">use assigned-clock-sscs</div>
      </div>
    </div>
  </div>
  <div class="pl-[27px] mt-1 text-[24px] font-semibold">Five years. Three vendor spellings. One generic framework.</div>
  <ul class="ml-[27px] pl-7 list-disc mt-1 space-y-1">
    <li class="text-lg">
      <b>One binding, vendor-agnostic</b>
      <div class="text-base text-gray-500">The property is now defined once and shared across platforms</div>
    </li>
    <li class="text-lg">
      <b>Four parameters &rarr; three are configurable</b>
      <div class="text-base text-gray-500">The profile is fixed in silicon</div>
    </li>
    <li class="text-lg">
      <b>Driver code &rarr; one callback</b>
      <div class="text-base text-gray-500">Parsing, validation and common handling move into the framework</div>
    </li>
  </ul>
  <div class="flex items-center justify-center gap-4 mt-auto -mb-[8px] text-2xl font-semibold -ml-8 -mr-4">
    <mdi-hand-pointing-right class="w-11 h-11 text-[#fdcb0e] shrink-0" />
    Register the callback and implement it
  </div>
</div>

---
title: Conclusions - What's Next
---

::title::

Conclusions - What's Next

::body::

<div class="flex flex-col pl-[27px] pr-4 h-[446px] pt-0">
  <ul class="pl-7 list-disc space-y-1.5">
    <li class="text-2xl">
      <b>Support your platform</b>
      <div class="text-lg text-gray-500">Minimal effort</div>
      <div class="text-lg text-gray-500">Implement the callback</div>
      <div class="text-lg text-gray-500">The framework handles the rest</div>
      <div class="text-lg text-gray-500">Validate the framework, extend or fix it when needed</div>
    </li>
    <li class="text-2xl">
      <b>Rework the legacy code</b>
      <div class="text-lg text-gray-500">Move existing vendor-specific implementations onto the common infrastructure</div>
    </li>
    <li class="text-2xl">
      <b>Need the profile parameter?</b>
      <div class="text-lg text-gray-500">Extend the binding where the silicon lets you choose</div>
    </li>
    <li class="text-2xl">
      <b>Need a platform-specific parameter?</b>
      <div class="text-lg text-gray-500">Remember AM33xx/AM43xx with its platform-specific <span class="font-mono text-base">ti,min-div</span> parameter?</div>
    </li>
  </ul>
  <div class="flex items-center justify-center gap-4 mt-auto -mb-[8px] text-2xl font-semibold -ml-[27px] -mr-4">
    <mdi-hand-pointing-right class="w-11 h-11 text-[#fdcb0e] shrink-0" />
    Every new platform makes the core stronger
  </div>
</div>

---
title: Acknowledgements
---

::title::

Acknowledgements

::body::

<div class="mt-0">
This talk was made possible thanks to the help and encouragement of many
people.
</div>

<div class="mt-6">
First of all, thanks to all guys who contributed to the review and acceptance
of the patches:<br>
Brian Masney, Cristian Marussi, Krzysztof Kozlowski, Peng Fan, Rob Herring,
Sebin Francis, Stephen Boyd and Tero Kristo.
</div>

<div class="mt-6">
Thanks to Alberto Bianchi, Alberto Panizzo, Andrea Ricchi, Michael Trimarchi
and Vera Binacchi (my daughter) for the slides review and refinement.
</div>

<div class="mt-6">
Thanks to Amarula and the ELCE organization for the assistance and support.
</div>

<div class="mt-18">
I'm sorry if I forgot someone :).
</div>

---
title: Resources
---

::title::

Resources

::body::

<div class="flex flex-col h-full pl-[59px] pr-12 pt-0 gap-[6px]">
  <div class="-mt-1">
    <div class="text-lg font-semibold">Technical Documentation</div>
    <div class="grid grid-cols-[68px_1fr] gap-x-2 font-mono text-[10.5px] leading-[1.2] mt-1">
      <div class="text-gray-500">AN4850</div>
      <div><a href="https://www.st.com/resource/en/application_note/dm00281138.pdf" class="text-blue-500 underline !border-b-0">st.com/resource/en/application_note/dm00281138.pdf</a></div>
      <div class="text-gray-500">Synopsys</div>
      <div><a href="https://www.synopsys.com/blogs/chip-design/understanding-pcie-spread-spectrum-clocking.html" class="text-blue-500 underline !border-b-0">synopsys.com/blogs/chip-design/understanding-pcie-spread-spectrum-clocking.html</a></div>
    </div>
  </div>
  <div>
    <div class="text-lg font-semibold">AM33xx/AM43xx SSC Linux series</div>
    <div class="grid grid-cols-[68px_1fr] gap-x-2 font-mono text-[10.5px] leading-[1.2] mt-1">
      <div class="text-gray-500">v3</div>
      <div><a href="https://lore.kernel.org/r/20210329164222.26794-1-dariobin@libero.it" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20210329164222.26794-1-dariobin@libero.it</a></div>
      <div class="text-gray-500">v4</div>
      <div><a href="https://lore.kernel.org/r/20210401193741.24639-1-dariobin@libero.it" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20210401193741.24639-1-dariobin@libero.it</a></div>
      <div class="text-gray-500">v5</div>
      <div><a href="https://lore.kernel.org/r/20210418145655.10415-1-dariobin@libero.it" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20210418145655.10415-1-dariobin@libero.it</a></div>
      <div class="text-gray-500">v6</div>
      <div><a href="https://lore.kernel.org/r/20210520191306.21711-1-dariobin@libero.it" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20210520191306.21711-1-dariobin@libero.it</a></div>
      <div class="text-gray-500">v7</div>
      <div><a href="https://lore.kernel.org/r/20210602150009.17531-1-dariobin@libero.it" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20210602150009.17531-1-dariobin@libero.it</a></div>
      <div class="text-gray-500">v7 RESEND</div>
      <div><a href="https://lore.kernel.org/r/20210606202253.31649-1-dariobin@libero.it" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20210606202253.31649-1-dariobin@libero.it</a></div>
      <div class="text-gray-500">U-Boot</div>
      <div><a href="https://lore.kernel.org/r/20210926095858.31278-1-dariobin@libero.it" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20210926095858.31278-1-dariobin@libero.it</a></div>
    </div>
  </div>
  <div>
    <div class="text-lg font-semibold">STM32F4/STM32F7 SSC Linux series</div>
    <div class="grid grid-cols-[68px_1fr] gap-x-2 font-mono text-[10.5px] leading-[1.2] mt-1">
      <div class="text-gray-500">v1</div>
      <div><a href="https://lore.kernel.org/r/20250105181525.1370822-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250105181525.1370822-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v2</div>
      <div><a href="https://lore.kernel.org/r/20250109211908.1553072-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250109211908.1553072-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v3</div>
      <div><a href="https://lore.kernel.org/r/20250114091128.528757-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250114091128.528757-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v4</div>
      <div><a href="https://lore.kernel.org/r/20250114182021.670435-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250114182021.670435-1-dario.binacchi@amarulasolutions.com</a></div>
    </div>
  </div>
  <div>
    <div class="text-lg font-semibold">i.MX8M Mini/Nano/Plus SSC Linux series</div>
    <div class="grid grid-cols-[68px_1fr] gap-x-2 font-mono text-[10.5px] leading-[1.2] mt-1">
      <div class="text-gray-500">v1</div>
      <div><a href="https://lore.kernel.org/r/20240928083804.1073942-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20240928083804.1073942-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v2</div>
      <div><a href="https://lore.kernel.org/r/20240929172743.1758292-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20240929172743.1758292-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v3</div>
      <div><a href="https://lore.kernel.org/r/20241106090549.3684963-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20241106090549.3684963-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v4</div>
      <div><a href="https://lore.kernel.org/r/20241201174639.742000-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20241201174639.742000-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v5</div>
      <div><a href="https://lore.kernel.org/r/20241205111939.1796244-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20241205111939.1796244-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v6</div>
      <div><a href="https://lore.kernel.org/r/20241222170534.3621453-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20241222170534.3621453-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v7</div>
      <div><a href="https://lore.kernel.org/r/20241227165719.3902388-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20241227165719.3902388-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v8</div>
      <div><a href="https://lore.kernel.org/r/20241229145027.3984542-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20241229145027.3984542-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v9</div>
      <div><a href="https://lore.kernel.org/r/CABGWkvoKV6dv1sHXJ1AZz7byp2ibh5uzLx9knF01HrcJLJyzCg@mail.gmail.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/CABGWkvoKV6dv1sHXJ1AZz7byp2ibh5uzLx9knF01HrcJLJyzCg@mail.gmail.com</a></div>
    </div>
  </div>
</div>

---
title: Resources
---

::title::

Resources

::body::

<div class="flex flex-col h-[430px] pl-[59px] pr-12 pt-[6px] gap-[10px]">
  <div class="-mt-1">
    <div class="text-lg font-semibold">i.MX8M Mini/Nano/Plus SSC Linux series</div>
    <div class="grid grid-cols-[68px_1fr] gap-x-2 font-mono text-[10.5px] leading-[1.4] mt-1">
      <div class="text-gray-500">v10</div>
      <div><a href="https://lore.kernel.org/r/20260831154752.15401-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260831154752.15401-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v11</div>
      <div><a href="https://lore.kernel.org/r/20260901090912.585681-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260901090912.585681-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v12</div>
      <div><a href="https://lore.kernel.org/r/20260902101515.167819-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260902101515.167819-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v13</div>
      <div><a href="https://lore.kernel.org/r/20260903153836.373267-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260903153836.373267-1-dario.binacchi@amarulasolutions.com</a></div>
      <div class="text-gray-500">v14</div>
      <div><a href="https://lore.kernel.org/r/20260904101243.412006-1-dario.binacchi@amarulasolutions.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260904101243.412006-1-dario.binacchi@amarulasolutions.com</a></div>
    </div>
  </div>
  <div>
    <div class="text-lg font-semibold">DT schema Pull Request</div>
    <div class="grid grid-cols-[68px_1fr] gap-x-2 font-mono text-[10.5px] leading-[1.4] mt-1">
      <div class="text-gray-500">PR 154</div>
      <div><a href="https://github.com/devicetree-org/dt-schema/pull/154" class="text-blue-500 underline !border-b-0">github.com/devicetree-org/dt-schema/pull/154</a></div>
    </div>
  </div>
  <div>
    <div class="text-lg font-semibold">Generic &amp; i.MX95 SSC Linux series</div>
    <div class="grid grid-cols-[68px_1fr] gap-x-2 font-mono text-[10.5px] leading-[1.4] mt-1">
      <div class="text-gray-500">v1</div>
      <div><a href="https://lore.kernel.org/r/20250812-clk-ssc-version1-v1-0-cef60f20d770@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250812-clk-ssc-version1-v1-0-cef60f20d770@nxp.com</a></div>
      <div class="text-gray-500">v2</div>
      <div><a href="https://lore.kernel.org/r/20250901-clk-ssc-version1-v2-0-1d0a486dffe6@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250901-clk-ssc-version1-v2-0-1d0a486dffe6@nxp.com</a></div>
      <div class="text-gray-500">v3</div>
      <div><a href="https://lore.kernel.org/r/20250912-clk-ssc-version1-v3-0-fd1e07476ba1@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250912-clk-ssc-version1-v3-0-fd1e07476ba1@nxp.com</a></div>
      <div class="text-gray-500">v4</div>
      <div><a href="https://lore.kernel.org/r/20250915-clk-ssc-version1-v4-0-5a2cee2f0351@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20250915-clk-ssc-version1-v4-0-5a2cee2f0351@nxp.com</a></div>
      <div class="text-gray-500">v5</div>
      <div><a href="https://lore.kernel.org/r/20251009-clk-ssc-v5-1-v5-0-d6447d76171e@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20251009-clk-ssc-v5-1-v5-0-d6447d76171e@nxp.com</a></div>
      <div class="text-gray-500">v6</div>
      <div><a href="https://lore.kernel.org/r/20251128-clk-ssc-v6-2-v6-0-cfafdb5d6811@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20251128-clk-ssc-v6-2-v6-0-cfafdb5d6811@nxp.com</a></div>
      <div class="text-gray-500">v7</div>
      <div><a href="https://lore.kernel.org/r/20251231-clk-ssc-v7-1-v7-0-380e8b58f9e3@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20251231-clk-ssc-v7-1-v7-0-380e8b58f9e3@nxp.com</a></div>
      <div class="text-gray-500">v8</div>
      <div><a href="https://lore.kernel.org/r/20260302-clk-ssc-v7-1-v8-0-2356443a7e4c@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260302-clk-ssc-v7-1-v8-0-2356443a7e4c@nxp.com</a></div>
      <div class="text-gray-500">v9</div>
      <div><a href="https://lore.kernel.org/r/20260312-clk-ssc-v7-1-v9-0-0a9d2e188d9e@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260312-clk-ssc-v7-1-v9-0-0a9d2e188d9e@nxp.com</a></div>
      <div class="text-gray-500">v10</div>
      <div><a href="https://lore.kernel.org/r/20260612-clk-v10-v10-0-eb92484eda38@nxp.com" class="text-blue-500 underline !border-b-0">lore.kernel.org/r/20260612-clk-v10-v10-0-eb92484eda38@nxp.com</a></div>
    </div>
  </div>
</div>

---
title: Q&A
---

::title::

Q&amp;A

::body::

<div class="flex flex-row justify-around items-center h-full pr-6">
  <div class="flex flex-col justify-center">
    <div class="text-3xl font-semibold">
      Thanks for your time
    </div>
    <div class="flex flex-col gap-4 mt-8">
      <div class="flex items-center gap-4 text-3xl">
        <mdi-help-circle class="w-9 h-9 text-[#fdcb0e] shrink-0" />
        Questions?
      </div>
      <div class="flex items-center gap-4 text-3xl pl-12 text-gray-700">
        <mdi-comment-text class="w-9 h-9 text-[#fdcb0e] shrink-0" />
        Comments?
      </div>
      <div class="flex items-center gap-4 text-3xl pl-24 text-gray-500">
        <mdi-lightbulb-on class="w-9 h-9 text-[#fdcb0e] shrink-0" />
        Suggestions?
      </div>
    </div>
    <div class="flex flex-col items-start gap-1 mt-12">
      <a href="mailto:dario.binacchi@amarulasolutions.com" class="inline-flex items-center gap-2 text-lg text-blue-500 underline !border-b-0">
        <mdi-email />
        dario.binacchi@amarulasolutions.com
      </a>
      <a href="https://www.amarulasolutions.com" class="inline-flex items-center gap-2 text-lg text-blue-500 underline !border-b-0">
        <mdi-web />
        www.amarulasolutions.com
      </a>
    </div>
  </div>
  <div class="flex flex-col justify-between space-y-2">
    <div>
      <img src="./assets/tux-beethoven-ssc.png" alt="Cartoon Tux as Beethoven, wild grey hair and red scarf, conducting with a baton in front of a screen showing a square wave whose period visibly varies" class="h-[300px] w-auto rounded-lg" />
    </div>
  </div>
</div>
