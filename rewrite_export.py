import re

with open("export.html", "r") as f:
    html = f.read()

# Replace the header block
header_pattern = r'<header.*?</header>'
new_header = """<header class="fixed top-0 w-full z-50 bg-surface-container-lowest border-b border-outline/10">
    <div class="h-16 w-full px-8 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 160 40" fill="none" class="h-6 w-auto">
          <g transform="translate(4, 4)">
            <rect x="0" y="2" width="32" height="28" rx="6" fill="#111827" stroke="#38bdf8" stroke-width="1.5"/>
            <line x1="6" y1="9" x2="26" y2="9" stroke="#fbbf24" stroke-width="2.5" stroke-linecap="round"/>
            <line x1="6" y1="23" x2="26" y2="23" stroke="#a855f7" stroke-width="2.5" stroke-linecap="round"/>
            <path d="M16 21V11" stroke="#38bdf8" stroke-width="1.5" stroke-dasharray="2 2"/>
            <polygon points="16,8 13.5,12 18.5,12" fill="#38bdf8"/>
            <circle cx="21" cy="9" r="2" fill="#fbbf24"/>
            <circle cx="11" cy="23" r="2" fill="#c084fc"/>
          </g>
          <text x="44" y="22" font-family="'IBM Plex Sans', sans-serif" font-weight="700" font-size="16" fill="#f8fafc" letter-spacing="0.5">SemiSim</text>
        </svg>
        <span class="text-outline mx-2">|</span>
        <span class="font-label-md text-sm text-primary tracking-widest uppercase">Report</span>
      </div>
      <nav class="hidden md:flex items-center gap-8">
        <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="index.html">Overview</a>
        <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="simulator.html">Simulator</a>
        <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="evaluation.html">Decisions</a>
        <a class="text-on-surface font-label-md text-sm transition-colors" href="export.html">Report</a>
      </nav>
    </div>
  </header>"""

html = re.sub(header_pattern, new_header, html, flags=re.DOTALL)

# Adjust pt-28 to pt-24
html = html.replace('pt-28', 'pt-24')

# Add a Math section before Section 1
math_section = """
        <!-- SECTION 0: Mathematical Derivations -->
        <details class="group bg-surface-container-low rounded-xl overflow-hidden border border-outline/5 mb-4">
          <summary class="flex justify-between items-center p-4 cursor-pointer select-none outline-none hover:bg-surface-container transition-colors">
            <div class="flex items-center gap-2">
              <span class="material-symbols-outlined text-primary">functions</span>
              <span class="font-headline-md text-lg text-on-surface">Show Mathematical Derivations</span>
            </div>
            <span class="material-symbols-outlined text-outline group-open:-scale-y-100 transition-transform">expand_more</span>
          </summary>
          <div class="p-6 pt-0 border-t border-outline/10 text-on-surface-variant font-body-sm leading-relaxed overflow-x-auto">
            <h4 class="font-label-md text-primary mt-4 mb-2">Detailed Balance Shockley-Queisser Limit</h4>
            <div class="bg-surface-container-highest p-4 rounded text-center mb-4">
              <code class="font-mono text-readout-md">J<sub>sc</sub> = q ∫ [Φ<sub>AM1.5G</sub>(E) dE] from E<sub>g</sub> to ∞</code>
            </div>
            <h4 class="font-label-md text-tertiary mt-4 mb-2">Gaussian Disorder Model (Bässler)</h4>
            <div class="bg-surface-container-highest p-4 rounded text-center">
              <code class="font-mono text-readout-md">μ = μ<sub>0</sub> exp[-(2σ / 3k<sub>B</sub>T)<sup>2</sup>] exp[C ( (σ/k<sub>B</sub>T)<sup>2</sup> - Σ<sup>2</sup> ) √E]</code>
            </div>
          </div>
        </details>
"""
html = html.replace('<!-- SECTION 1: Executive Summary -->', math_section + '\n        <!-- SECTION 1: Executive Summary -->')

with open("export.html", "w") as f:
    f.write(html)

