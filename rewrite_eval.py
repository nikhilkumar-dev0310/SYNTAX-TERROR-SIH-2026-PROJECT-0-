import re

with open("evaluation.html", "r") as f:
    html = f.read()

# Extract script at the bottom
script_match = re.search(r'<script>(.*?)</script>\s*</body>', html, re.DOTALL)
script_content = script_match.group(1) if script_match else ""

new_html = """<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>SemiSim - Engineering Decisions</title>
  <style>
    @layer base {
      html, body { margin: 0; padding: 0; }
      body { overscroll-behavior: none; }
    }
    ::-webkit-scrollbar { display: none; }
    details > summary { list-style: none; }
    details > summary::-webkit-details-marker { display: none; }
  </style>
  <script src="https://cdn.tailwindcss.com"></script>
  <script id="tailwind-config">
    tailwind.config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "secondary": "#ffc640", "primary": "#8ed5ff", "tertiary": "#e1c0ff",
            "surface-container-lowest": "#0a0e16", "surface-variant": "#31353e",
            "surface-container-highest": "#31353e", "surface-container-low": "#181c24",
            "surface-container": "#1c2028", "surface": "#0f131c", "on-surface": "#dfe2ee",
            "on-surface-variant": "#bdc8d1", "outline": "#87929a", "on-primary-container": "#004965",
            "primary-container": "#38bdf8", "error": "#ffb4ab"
          },
          fontFamily: {
            "body-sm": ["Inter"], "display-lg": ["IBM Plex Sans"], "body-lg": ["Inter"],
            "label-md": ["JetBrains Mono"], "body-md": ["Inter"],
            "headline-lg": ["IBM Plex Sans"], "headline-md": ["IBM Plex Sans"], "readout-md": ["JetBrains Mono"],
            "label-sm": ["JetBrains Mono"], "readout-lg": ["JetBrains Mono"]
          }
        }
      }
    };
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet"/>
  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@100..900&family=Inter:wght@100..900&family=JetBrains+Mono:wght@100..900&display=swap" rel="stylesheet"/>
</head>
<body class="bg-surface-container-lowest font-body-md text-on-surface antialiased">

  <header class="h-16 shrink-0 w-full px-8 flex items-center justify-between border-b border-outline/10 bg-surface-container-lowest z-40 fixed top-0">
    <div class="flex items-center gap-4">
      <div class="flex items-center gap-2">
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
        <span class="font-label-md text-sm text-primary tracking-widest uppercase">Decisions</span>
      </div>
    </div>
    
    <nav class="hidden md:flex items-center gap-8">
      <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="index.html">Overview</a>
      <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="simulator.html">Simulator</a>
      <a class="text-on-surface font-label-md text-sm transition-colors" href="evaluation.html">Decisions</a>
      <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="export.html">Report</a>
    </nav>
  </header>

  <main class="w-full pt-24 pb-16 px-4">
    <div class="max-w-4xl mx-auto flex flex-col items-center">
      
      <div class="text-center mb-16 mt-8">
        <span class="font-label-md text-xs tracking-[0.2em] text-primary uppercase mb-4 block">Decision Gateway</span>
        <h1 class="font-display-lg text-5xl md:text-6xl text-on-surface tracking-tight font-medium mb-6">Evaluation & Synthesis</h1>
        <p class="font-body-lg text-xl text-on-surface-variant font-light max-w-2xl mx-auto">
          Bridge molecular-scale photophysics to utility manufacturing and operational endurance. Complete the dossiers below.
        </p>
      </div>

      <div class="w-full flex flex-col gap-4">
        
        <!-- Task 1 Dossier -->
        <details class="group bg-surface-container-low rounded-2xl overflow-hidden shadow-lg border border-outline/5" open>
          <summary class="flex justify-between items-center p-8 cursor-pointer select-none outline-none group-hover:bg-surface-container transition-colors">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-3">
                <span class="w-2 h-2 rounded-full bg-primary group-open:animate-ping"></span>
                <span class="font-label-md text-xs tracking-[0.2em] text-on-surface-variant uppercase">Task 01</span>
              </div>
              <h2 class="font-headline-md text-2xl text-on-surface">Smart Materials & Functional Coatings</h2>
            </div>
            <span class="material-symbols-outlined text-outline group-open:-scale-y-100 transition-transform">expand_more</span>
          </summary>
          <div class="p-8 pt-0 border-t border-outline/10">
            <p class="font-body-md text-on-surface-variant mt-6 mb-8 font-light text-lg">
              Functional exterior layers control interfacial photon injection, dielectric passivation, and environmental water vapor barrier dynamics. Inspect the performance trade-offs below to select an optimized thin-film coating architecture.
            </p>

            <!-- Coating Selector Cards -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-8">
              <div class="cursor-pointer bg-surface-container rounded-xl p-6 transition-all border border-transparent hover:border-primary/30" id="card-coating-A" onclick="selectCoating('A')">
                <div class="flex items-center justify-between mb-4">
                  <span class="font-label-sm text-[10px] uppercase tracking-wider text-secondary">Option A • AR</span>
                  <div class="w-2.5 h-2.5 rounded-full bg-surface-variant transition-colors" id="indicator-coating-A"></div>
                </div>
                <h3 class="font-headline-md text-lg text-on-surface mb-2">TiO₂ / SiO₂ Graded</h3>
                <span class="font-label-sm text-xs text-on-surface-variant">Cost: $14.50 /m²</span>
              </div>

              <div class="cursor-pointer bg-surface-container rounded-xl p-6 transition-all border border-transparent hover:border-primary/30" id="card-coating-B" onclick="selectCoating('B')">
                <div class="flex items-center justify-between mb-4">
                  <span class="font-label-sm text-[10px] uppercase tracking-wider text-tertiary">Option B • Barrier</span>
                  <div class="w-2.5 h-2.5 rounded-full bg-surface-variant transition-colors" id="indicator-coating-B"></div>
                </div>
                <h3 class="font-headline-md text-lg text-on-surface mb-2">Al₂O₃ / Vitrimer</h3>
                <span class="font-label-sm text-xs text-on-surface-variant">Cost: $62.00 /m²</span>
              </div>

              <div class="cursor-pointer bg-surface-container rounded-xl p-6 transition-all border border-transparent hover:border-primary/30" id="card-coating-C" onclick="selectCoating('C')">
                <div class="flex items-center justify-between mb-4">
                  <span class="font-label-sm text-[10px] uppercase tracking-wider text-primary">Option C • Smart</span>
                  <div class="w-2.5 h-2.5 rounded-full bg-surface-variant transition-colors" id="indicator-coating-C"></div>
                </div>
                <h3 class="font-headline-md text-lg text-on-surface mb-2">VO₂ Monoclinic</h3>
                <span class="font-label-sm text-xs text-on-surface-variant">Cost: $38.00 /m²</span>
              </div>
            </div>

            <!-- Response Box -->
            <div class="bg-surface-container-lowest p-6 rounded-xl flex flex-col md:flex-row gap-8 mb-8 border border-outline/5">
              <div class="flex-1 flex flex-col gap-6">
                <div>
                  <h4 class="font-headline-md text-xl text-on-surface" id="sim-coating-name">TiO₂/SiO₂ Graded Sol-Gel</h4>
                  <span class="font-label-sm text-sm text-primary mt-1 block" id="sim-coating-role">Solar Front Surface AR</span>
                </div>
                <div class="grid grid-cols-2 gap-4 font-readout-md text-lg">
                  <div class="flex flex-col"><span class="font-label-sm text-[10px] text-on-surface-variant uppercase tracking-widest mb-1">PCE Impact</span><span class="text-primary" id="sim-val-pce">+1.42%</span></div>
                  <div class="flex flex-col"><span class="font-label-sm text-[10px] text-on-surface-variant uppercase tracking-widest mb-1">Durability</span><span class="text-secondary" id="sim-val-life">+4.8 yrs</span></div>
                </div>
              </div>
              <div class="flex-1 flex flex-col gap-4 justify-center">
                <div class="flex flex-col gap-1"><span class="font-label-sm text-xs text-on-surface-variant">Optical Transmittance</span><div class="w-full h-1.5 bg-surface-bright rounded overflow-hidden"><div class="h-full bg-primary" id="meter-bar-opt" style="width:94.8%"></div></div></div>
                <div class="flex flex-col gap-1"><span class="font-label-sm text-xs text-on-surface-variant">Mechanical Flexibility</span><div class="w-full h-1.5 bg-surface-bright rounded overflow-hidden"><div class="h-full bg-secondary" id="meter-bar-flex" style="width:48%"></div></div></div>
                <div class="flex flex-col gap-1"><span class="font-label-sm text-xs text-on-surface-variant">Moisture Barrier (MVTR)</span><div class="w-full h-1.5 bg-surface-bright rounded overflow-hidden"><div class="h-full bg-tertiary" id="meter-bar-mvtr" style="width:85%"></div></div></div>
              </div>
              <div class="hidden">
                <span id="sim-coating-status"></span><span id="meter-val-opt"></span><span id="meter-val-flex"></span><span id="meter-val-mvtr"></span><span id="meter-val-temp"></span><span id="meter-bar-temp"></span><span id="sim-val-lum"></span><span id="sim-val-cost"></span>
              </div>
            </div>

            <!-- Justification -->
            <div class="flex flex-col gap-4 bg-surface-container p-6 rounded-xl border border-outline/5">
              <label class="font-label-md text-sm text-on-surface" for="justification-task1">Engineering Justification</label>
              <textarea class="w-full bg-surface-container-lowest p-4 rounded-lg font-body-md text-on-surface focus:outline-none focus:ring-1 focus:ring-primary border border-outline/10 resize-none h-32" id="justification-task1" placeholder="Synthesize your coating choice for high-humidity outdoor solar deployment..."></textarea>
              <div class="flex justify-end">
                <button class="px-6 py-2 rounded-full bg-primary text-on-primary font-label-md text-sm font-semibold hover:scale-105 transition-transform shadow-lg shadow-primary/20" onclick="commitJustification(1)">Commit Rationale</button>
              </div>
            </div>
          </div>
        </details>

        <!-- Task 2 Dossier -->
        <details class="group bg-surface-container-low rounded-2xl overflow-hidden shadow-lg border border-outline/5">
          <summary class="flex justify-between items-center p-8 cursor-pointer select-none outline-none group-hover:bg-surface-container transition-colors">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-3">
                <span class="w-2 h-2 rounded-full bg-primary group-open:animate-ping"></span>
                <span class="font-label-md text-xs tracking-[0.2em] text-on-surface-variant uppercase">Task 02</span>
              </div>
              <h2 class="font-headline-md text-2xl text-on-surface">Organic vs Inorganic Matrix</h2>
            </div>
            <span class="material-symbols-outlined text-outline group-open:-scale-y-100 transition-transform">expand_more</span>
          </summary>
          <div class="p-8 pt-0 border-t border-outline/10">
            <p class="font-body-md text-on-surface-variant mt-6 mb-8 font-light text-lg">
              Examine how crystal symmetry, electronic delocalization, and Coulombic dielectric screening dictate carrier propagation.
            </p>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
              <div class="bg-surface-container p-6 rounded-xl border border-outline/5">
                <h4 class="font-label-md text-sm text-primary uppercase tracking-wider mb-4">Inorganic (Si / GaAs)</h4>
                <ul class="font-body-md text-on-surface-variant font-light space-y-3">
                  <li>• High Dielectric Constant (ε ≈ 12)</li>
                  <li>• Bloch Wave Delocalization (μ > 1000 cm²/Vs)</li>
                  <li>• Thermal Stability > 150°C</li>
                </ul>
              </div>
              <div class="bg-surface-container p-6 rounded-xl border border-outline/5">
                <h4 class="font-label-md text-sm text-tertiary uppercase tracking-wider mb-4">Organic (Alq3 / PPV)</h4>
                <ul class="font-body-md text-on-surface-variant font-light space-y-3">
                  <li>• Low Dielectric Constant (ε ≈ 3)</li>
                  <li>• Gaussian Disorder Hopping (μ < 1 cm²/Vs)</li>
                  <li>• Mechanical Flexibility (Roll-to-roll)</li>
                </ul>
              </div>
            </div>
            <!-- Justification -->
            <div class="flex flex-col gap-4 bg-surface-container p-6 rounded-xl border border-outline/5">
              <label class="font-label-md text-sm text-on-surface" for="justification-task2">Tradeoff Analysis</label>
              <textarea class="w-full bg-surface-container-lowest p-4 rounded-lg font-body-md text-on-surface focus:outline-none focus:ring-1 focus:ring-primary border border-outline/10 resize-none h-32" id="justification-task2" placeholder="Analyze why low carrier mobility in organics is acceptable for thin emissive OLED displays..."></textarea>
              <div class="flex justify-end">
                <button class="px-6 py-2 rounded-full bg-primary text-on-primary font-label-md text-sm font-semibold hover:scale-105 transition-transform shadow-lg shadow-primary/20" onclick="commitJustification(2)">Commit Rationale</button>
              </div>
            </div>
          </div>
        </details>

        <!-- Task 3 Dossier -->
        <details class="group bg-surface-container-low rounded-2xl overflow-hidden shadow-lg border border-outline/5">
          <summary class="flex justify-between items-center p-8 cursor-pointer select-none outline-none group-hover:bg-surface-container transition-colors">
            <div class="flex flex-col gap-2">
              <div class="flex items-center gap-3">
                <span class="w-2 h-2 rounded-full bg-primary group-open:animate-ping"></span>
                <span class="font-label-md text-xs tracking-[0.2em] text-on-surface-variant uppercase">Task 03</span>
              </div>
              <h2 class="font-headline-md text-2xl text-on-surface">Application Scenario Synthesis</h2>
            </div>
            <span class="material-symbols-outlined text-outline group-open:-scale-y-100 transition-transform">expand_more</span>
          </summary>
          <div class="p-8 pt-0 border-t border-outline/10">
            
            <div class="grid grid-cols-2 gap-4 mb-8 mt-6">
              <button class="py-4 px-4 rounded-xl bg-primary-container text-on-primary-container font-headline-md text-lg transition-all text-center border border-transparent" id="btn-scenario-1" onclick="selectScenario('1')">Utility PV</button>
              <button class="py-4 px-4 rounded-xl bg-surface-container text-on-surface-variant hover:text-on-surface font-headline-md text-lg transition-all text-center border border-outline/5" id="btn-scenario-2" onclick="selectScenario('2')">Wearable Textile</button>
              <button class="py-4 px-4 rounded-xl bg-surface-container text-on-surface-variant hover:text-on-surface font-headline-md text-lg transition-all text-center border border-outline/5" id="btn-scenario-3" onclick="selectScenario('3')">Foldable OLED</button>
              <button class="py-4 px-4 rounded-xl bg-surface-container text-on-surface-variant hover:text-on-surface font-headline-md text-lg transition-all text-center border border-outline/5" id="btn-scenario-4" onclick="selectScenario('4')">Solid-State Light</button>
            </div>

            <div class="bg-surface-container-lowest p-8 rounded-xl flex flex-col gap-6 mb-8 border border-outline/5">
              <h3 class="font-headline-md text-2xl text-on-surface" id="scene-title">Utility Scale Rooftop PV</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6 font-readout-md text-lg">
                <div class="flex flex-col"><span class="font-label-sm text-[10px] text-on-surface-variant uppercase tracking-widest mb-1">Target Band Gap</span><span class="text-secondary" id="scene-eg">1.1 - 1.4 eV</span></div>
                <div class="flex flex-col"><span class="font-label-sm text-[10px] text-on-surface-variant uppercase tracking-widest mb-1">Target Mobility</span><span class="text-primary" id="scene-mob">μe > 800 cm²/V·s</span></div>
                <div class="flex flex-col"><span class="font-label-sm text-[10px] text-on-surface-variant uppercase tracking-widest mb-1">Optimal Stack</span><span class="text-on-surface" id="scene-mat">c-Si / InGaP-GaAs Tandem</span></div>
                <div class="hidden"><span id="scene-status-tag"></span><span id="scene-mvtr"></span></div>
              </div>
            </div>

            <!-- Justification -->
            <div class="flex flex-col gap-4 bg-surface-container p-6 rounded-xl border border-outline/5">
              <label class="font-label-md text-sm text-on-surface" for="justification-task3">Scenario Rationale</label>
              <textarea class="w-full bg-surface-container-lowest p-4 rounded-lg font-body-md text-on-surface focus:outline-none focus:ring-1 focus:ring-primary border border-outline/10 resize-none h-32" id="justification-task3" placeholder="Explain your design choice for the selected scenario..."></textarea>
              <div class="flex justify-end">
                <button class="px-6 py-2 rounded-full bg-primary text-on-primary font-label-md text-sm font-semibold hover:scale-105 transition-transform shadow-lg shadow-primary/20" onclick="commitJustification(3)">Commit Rationale</button>
              </div>
            </div>
          </div>
        </details>

      </div>
    </div>
  </main>

  <script>
""" + script_content + """
  </script>
</body>
</html>
"""

with open("evaluation.html", "w") as f:
    f.write(new_html)
