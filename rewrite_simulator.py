import re

with open("simulator.html", "r") as f:
    html = f.read()

# Extract the script block
script_match = re.search(r'<script>(.*?)</script>\s*</body>', html, re.DOTALL)
script_content = script_match.group(1) if script_match else ""

# Prepare the new HTML layout
new_html = """<!DOCTYPE html>
<html class="dark" lang="en">
<head>
  <meta charset="utf-8"/>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>
  <title>SemiSim - Simulator</title>
  <style>
    @layer base {
      html, body { margin: 0; padding: 0; height: 100%; overflow: hidden; }
      body { overscroll-behavior: none; }
    }
    ::-webkit-scrollbar { display: none; }
    #drawer { transform: translateX(0); transition: transform 0.3s ease-in-out; }
    #drawer.closed { transform: translateX(-100%); }
    #main-stage { transition: margin-left 0.3s ease-in-out; }
    .drawer-open #main-stage { margin-left: 24rem; }
    .dossier-content { max-height: 0; overflow: hidden; transition: max-height 0.4s ease-out; }
    .dossier-open .dossier-content { max-height: 2000px; }
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
            "primary-container": "#38bdf8", "error": "#ffb4ab", "on-primary": "#00354a", "on-secondary": "#402d00",
            "on-tertiary": "#490081"
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
  <script src="api-config.js"></script>
</head>
<body class="bg-surface-container-lowest font-body-md text-on-surface antialiased drawer-open flex flex-col h-screen">

  <!-- Restrained Header -->
  <header class="h-16 shrink-0 w-full px-6 flex items-center justify-between border-b border-outline/10 bg-surface-container-lowest z-40 relative">
    <div class="flex items-center gap-4">
      <button onclick="toggleDrawer()" class="p-2 hover:bg-surface-container rounded-full text-on-surface-variant transition-colors">
        <span class="material-symbols-outlined">menu</span>
      </button>
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
        <span class="font-label-md text-sm text-primary tracking-widest uppercase">Simulator</span>
      </div>
    </div>
    
    <nav class="hidden md:flex items-center gap-8">
      <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="index.html">Overview</a>
      <a class="text-on-surface font-label-md text-sm transition-colors" href="simulator.html">Simulator</a>
      <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="evaluation.html">Decisions</a>
      <a class="text-on-surface-variant hover:text-on-surface font-label-md text-sm transition-colors" href="export.html">Report</a>
    </nav>
    <div class="flex items-center gap-2">
      <span class="px-2 py-0.5 rounded font-label-sm text-xs bg-secondary text-on-secondary font-medium" id="headerCouplingBadge">EMISSION ACTIVE [OLED]</span>
    </div>
  </header>

  <div class="flex flex-1 relative overflow-hidden">
    
    <!-- Left Drawer (Controls) -->
    <aside id="drawer" class="absolute top-0 left-0 h-full w-96 bg-surface-container-low border-r border-outline/10 z-30 overflow-y-auto flex flex-col">
      <div class="p-6 flex flex-col gap-8">
        
        <!-- Mode & Architecture -->
        <div class="flex flex-col gap-4">
          <span class="font-label-sm text-xs text-on-surface-variant tracking-wider uppercase">Operating Regime</span>
          <div class="grid grid-cols-2 p-1 bg-surface-container-lowest rounded-lg gap-1">
            <button class="py-2 px-2 rounded font-label-md text-sm text-on-primary-container bg-primary-container font-semibold transition-all text-center" id="modeOledBtn" onclick="setAppMode('oled')">OLED Display</button>
            <button class="py-2 px-2 rounded font-label-md text-sm text-on-surface-variant hover:text-on-surface transition-all text-center" id="modeSolarBtn" onclick="setAppMode('solar')">Solar Cell</button>
          </div>
          
          <span class="font-label-sm text-xs text-on-surface-variant tracking-wider uppercase mt-2">Material Class</span>
          <div class="grid grid-cols-2 p-1 bg-surface-container-lowest rounded-lg gap-1">
            <button class="py-2 px-2 rounded font-label-md text-sm text-on-primary-container bg-primary-container font-semibold transition-all text-center" id="matOrganicBtn" onclick="setMatClass('organic')">Organic</button>
            <button class="py-2 px-2 rounded font-label-md text-sm text-on-surface-variant hover:text-on-surface transition-all text-center" id="matInorganicBtn" onclick="setMatClass('inorganic')">Inorganic</button>
          </div>

          <span class="font-label-sm text-xs text-on-surface-variant tracking-wider uppercase mt-2">Preset Material</span>
          <select class="w-full bg-surface-container-lowest text-on-surface font-label-md text-sm py-3 px-4 rounded-lg outline-none focus:bg-surface-bright transition-colors cursor-pointer border border-outline/10" id="presetSelect" onchange="applyPreset(this.value)"></select>
        </div>

        <hr class="border-outline/10"/>

        <!-- Primary Control (Band Gap) -->
        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <span class="font-label-sm text-xs text-secondary tracking-wider uppercase">Band Gap Tuning</span>
            <span class="px-2 py-0.5 rounded font-label-sm text-[10px] bg-secondary text-on-secondary font-semibold" id="spectralBadge">590 nm • Amber</span>
          </div>
          <div class="flex items-baseline justify-between mb-2">
            <label class="font-label-sm text-xs text-on-surface-variant" for="egSlider">Energy ($E_g$)</label>
            <div class="flex items-center gap-1 bg-surface-container-lowest px-2 py-1 rounded">
              <span class="font-readout-md text-base text-secondary font-semibold" id="egValueDisplay">2.10</span>
              <span class="font-label-sm text-xs text-on-surface-variant">eV</span>
            </div>
          </div>
          <input class="w-full accent-secondary bg-surface-container-lowest h-2 rounded cursor-pointer" id="egSlider" max="3.8" min="0.5" oninput="onEgInput(parseFloat(this.value))" step="0.02" type="range" value="2.10"/>
        </div>

        <hr class="border-outline/10"/>

        <!-- Contextual Secondary Parameters -->
        <div class="flex flex-col gap-4">
          <span class="font-label-sm text-xs text-primary tracking-wider uppercase" id="contextParamsHeading">Organic Parameters</span>
          
          <div class="flex flex-col gap-3" id="organicParamsGroup">
            <div class="flex flex-col gap-1">
              <div class="flex justify-between font-label-sm text-xs text-on-surface-variant">
                <span>Disorder (σ)</span>
                <span class="text-on-surface" id="disorderDisplay">0.08 eV</span>
              </div>
              <input class="w-full accent-primary bg-surface-container-lowest h-1.5 rounded cursor-pointer" id="disorderSlider" max="0.18" min="0.02" oninput="onDisorderInput(parseFloat(this.value))" step="0.01" type="range" value="0.08"/>
            </div>
            <div class="flex flex-col gap-1">
              <div class="flex justify-between font-label-sm text-xs text-on-surface-variant">
                <span>Thickness</span>
                <span class="text-on-surface" id="thickDisplay">100 nm</span>
              </div>
              <input class="w-full accent-primary bg-surface-container-lowest h-1.5 rounded cursor-pointer" id="thickSlider" max="250" min="40" oninput="document.getElementById('thickDisplay').innerText = this.value + ' nm'" type="range" value="100"/>
            </div>
          </div>

          <div class="hidden flex flex-col gap-3" id="inorganicParamsGroup">
            <div class="flex justify-between font-label-sm text-xs text-on-surface-variant">
                <span>Doping (N<sub>d</sub>)</span>
                <span class="text-on-surface">5.0×10¹⁶</span>
            </div>
          </div>

          <div class="flex flex-col gap-1 mt-2" id="biasControlWrapper">
            <div class="flex justify-between font-label-sm text-xs text-on-surface-variant">
              <span>Applied Bias (V)</span>
              <span class="text-primary font-readout-md text-sm" id="biasDisplay">3.80 V</span>
            </div>
            <input class="w-full accent-primary bg-surface-container-lowest h-1.5 rounded cursor-pointer" id="biasSlider" max="8.0" min="0.0" oninput="document.getElementById('biasDisplay').innerText=parseFloat(this.value).toFixed(2)+' V'" step="0.1" type="range" value="3.8"/>
          </div>
          
          <div class="hidden flex flex-col gap-1 mt-2" id="solarFluxControlWrapper">
            <div class="flex justify-between font-label-sm text-xs text-on-surface-variant">
              <span>Incident Flux</span>
              <span class="text-secondary font-readout-md text-sm" id="fluxDisplay">1.0 Sun</span>
            </div>
            <input class="w-full accent-secondary bg-surface-container-lowest h-1.5 rounded cursor-pointer" id="fluxSlider" max="5.0" min="1.0" oninput="onConcentrationInput(parseFloat(this.value))" step="0.5" type="range" value="1.0"/>
          </div>
        </div>

      </div>
    </aside>

    <!-- Main Center Stage -->
    <main id="main-stage" class="flex-1 overflow-y-auto p-8 flex flex-col items-center bg-surface-container-lowest relative">
      <div class="w-full max-w-5xl flex flex-col gap-12 pt-8 pb-32">
        
        <!-- Hero Metric -->
        <div class="flex flex-col items-center justify-center text-center">
          <span class="font-label-md tracking-[0.3em] text-on-surface-variant uppercase mb-4" id="efficiencyLabel">INTERNAL QUANTUM EFF. (IQE)</span>
          <div class="flex items-center gap-6">
            <div class="w-16 h-16 rounded-2xl shadow-2xl flex items-center justify-center font-label-sm text-xs font-bold text-on-secondary transition-colors duration-500" id="colorSwatchBox" style="background-color: #f59e0b;">
              590nm
            </div>
            <h2 class="font-display-lg text-[100px] leading-none text-on-surface tracking-tighter" id="efficiencyValue">7.2%</h2>
          </div>
          <span class="font-label-sm text-sm text-on-surface-variant mt-4" id="efficiencySub">η_S=25% (fluorescent singlet limit)</span>
        </div>

        <!-- Huge Visualization Stage -->
        <div class="w-full flex flex-col gap-8">
          
          <!-- Band Diagram -->
          <div class="relative w-full aspect-[3/1] bg-surface-container-low rounded-3xl p-6 overflow-hidden shadow-2xl border border-outline/5">
            <div class="absolute top-6 left-6 font-label-sm text-xs text-on-surface-variant tracking-wider uppercase">Energy Landscape</div>
            <div class="absolute top-6 right-6 px-3 py-1 rounded-full bg-surface-container-highest text-primary font-label-sm text-[10px]" id="transportModelBadge">Miller-Abrahams Hopping</div>
            
            <svg class="w-full h-full pt-8 select-none" id="bandDiagramSvg" preserveAspectRatio="none" viewBox="0 0 600 220">
              <defs>
                <pattern height="20" id="reticleGrid" patternUnits="userSpaceOnUse" width="40">
                  <path class="text-surface-variant" d="M 40 0 L 0 0 0 20" fill="none" opacity="0.3" stroke="currentColor" stroke-width="0.5"></path>
                </pattern>
                <linearGradient id="lumoGradient" x1="0%" x2="100%" y1="0%" y2="0%">
                  <stop offset="0%" stop-color="#ffc640" stop-opacity="0.9"></stop>
                  <stop offset="100%" stop-color="#e3aa00" stop-opacity="0.8"></stop>
                </linearGradient>
                <linearGradient id="homoGradient" x1="0%" x2="100%" y1="0%" y2="0%">
                  <stop offset="0%" stop-color="#e1c0ff" stop-opacity="0.9"></stop>
                  <stop offset="100%" stop-color="#ce9cff" stop-opacity="0.8"></stop>
                </linearGradient>
                <marker id="arrow" markerHeight="6" markerWidth="6" orient="auto-start-reverse" refX="5" refY="5" viewBox="0 0 10 10">
                  <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#8ed5ff"></path>
                </marker>
              </defs>
              <rect fill="url(#reticleGrid)" height="100%" width="100%"></rect>
              <line stroke="#87929a" stroke-dasharray="4 4" stroke-width="1.5" x1="40" x2="560" y1="20" y2="20"></line>
              <g id="lumoGroup">
                <rect fill="url(#lumoGradient)" height="12" id="lumoBar" rx="6" width="440" x="80" y="75"></rect>
                <text class="font-readout-md text-[14px]" fill="#ffc640" id="lumoLabel" x="525" y="85">LUMO</text>
              </g>
              <g id="homoGroup">
                <rect fill="url(#homoGradient)" height="12" id="homoBar" rx="6" width="440" x="80" y="165"></rect>
                <text class="font-readout-md text-[14px]" fill="#e1c0ff" id="homoLabel" x="525" y="175">HOMO</text>
              </g>
              <line id="transitionArrow" marker-end="url(#arrow)" marker-start="url(#arrow)" stroke="#8ed5ff" stroke-width="2" x1="280" x2="280" y1="163" y2="87"></line>
              <g id="egBadgeGroup">
                <rect class="fill-surface-container-highest" height="28" id="egBadgeBg" rx="14" width="120" x="220" y="105"></rect>
                <text class="font-readout-md text-[14px] font-bold" fill="#8ed5ff" id="svgEgText" text-anchor="middle" x="280" y="124">Eg = 2.10 eV</text>
              </g>
              <g id="photonParticle">
                <path d="M 285,119 Q 295,109 305,119 T 325,119 T 345,119" fill="none" id="photonWave" stroke="#ffc640" stroke-linecap="round" stroke-width="3"></path>
                <polygon fill="#ffc640" points="348,119 340,114 340,124"></polygon>
                <text class="font-label-sm text-[12px]" fill="#ffc640" id="photonLabelText" x="355" y="123">hν (590 nm)</text>
              </g>
            </svg>
          </div>

          <!-- Transport Canvas -->
          <div class="relative w-full aspect-[4/1] bg-surface-container-low rounded-3xl overflow-hidden shadow-2xl border border-outline/5">
            <canvas id="transportCanvas" class="w-full h-full block"></canvas>
            <div class="absolute inset-y-0 left-0 w-12 bg-gradient-to-r from-surface-container-highest to-transparent flex items-center justify-center pointer-events-none">
              <span class="font-label-sm text-[10px] text-primary [writing-mode:vertical-rl] rotate-180 font-bold opacity-50">CATHODE</span>
            </div>
            <div class="absolute inset-y-0 right-0 w-12 bg-gradient-to-l from-surface-container-highest to-transparent flex items-center justify-center pointer-events-none">
              <span class="font-label-sm text-[10px] text-tertiary [writing-mode:vertical-rl] rotate-180 font-bold opacity-50">ANODE</span>
            </div>
          </div>
          
        </div>

        <!-- Progressive Disclosure: The Dossier -->
        <div class="w-full max-w-4xl mx-auto mt-16" id="dossier-container">
          <button onclick="toggleDossier()" class="w-full flex items-center justify-between p-6 bg-surface-container rounded-2xl hover:bg-surface-container-high transition-colors outline-none focus:ring-2 ring-primary/50 group">
            <div class="flex items-center gap-4">
              <span class="material-symbols-outlined text-primary">data_object</span>
              <span class="font-headline-md text-xl text-on-surface">Open Full Physics Dossier</span>
            </div>
            <span class="material-symbols-outlined text-on-surface-variant group-hover:text-on-surface transition-colors" id="dossier-icon">expand_more</span>
          </button>
          
          <div class="dossier-content px-2 mt-4" id="dossier-content">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pb-8">
              
              <!-- Metrics grid -->
              <div class="bg-surface-container-low p-6 rounded-2xl border border-outline/5 flex flex-col gap-6">
                <span class="font-label-sm text-xs text-on-surface-variant tracking-wider uppercase">Extracted Metrics</span>
                
                <div class="flex flex-col gap-4">
                  <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                    <span class="font-body-sm text-on-surface-variant">Charge Mobility (μ)</span>
                    <span class="font-readout-lg text-lg text-primary" id="mobilityValue">1.4 × 10⁻⁴ cm²/(V·s)</span>
                  </div>
                  <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                    <span class="font-body-sm text-on-surface-variant">Transport Model</span>
                    <span class="font-readout-md text-sm text-on-surface" id="mobilityType">GDM (Bässler)</span>
                  </div>
                  <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                    <span class="font-body-sm text-on-surface-variant">Exciton Binding (E<sub>b</sub>)</span>
                    <span class="font-readout-lg text-lg text-tertiary" id="excitonBindingVal">529 meV</span>
                  </div>
                  <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                    <span class="font-body-sm text-on-surface-variant">Exciton Character</span>
                    <span class="font-readout-md text-sm text-on-surface" id="excitonType">Frenkel</span>
                  </div>
                  <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                    <span class="font-body-sm text-on-surface-variant">Photon Wavelength</span>
                    <span class="font-readout-lg text-lg text-secondary" id="quantumWavelength">590.4 nm</span>
                  </div>
                  
                  <div id="pvDetailedCard" class="hidden flex-col gap-4 mt-2">
                    <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                      <span class="font-body-sm text-on-surface-variant">Short-Circuit Current (J<sub>sc</sub>)</span>
                      <span class="font-readout-lg text-lg text-primary" id="jscVal">35.0 mA/cm²</span>
                    </div>
                    <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                      <span class="font-body-sm text-on-surface-variant">Open-Circuit Voltage (V<sub>oc</sub>)</span>
                      <span class="font-readout-lg text-lg text-secondary" id="vocVal">1.08 V</span>
                    </div>
                    <div class="flex justify-between items-end border-b border-outline/10 pb-2">
                      <span class="font-body-sm text-on-surface-variant">Fill Factor (FF)</span>
                      <span class="font-readout-lg text-lg text-on-surface" id="ffVal">88.9%</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Supplementary info -->
              <div class="flex flex-col gap-6">
                <!-- Color Box -->
                <div class="bg-surface-container-low p-6 rounded-2xl border border-outline/5" id="oledSubPanel">
                  <span class="font-label-sm text-xs text-on-surface-variant tracking-wider uppercase block mb-4">Photometric Output</span>
                  <div class="flex items-center gap-4">
                    <div class="flex flex-col">
                      <span class="font-readout-lg text-xl text-on-surface" id="colorHexDisplay">#F59E0B</span>
                      <span class="font-label-sm text-sm text-on-surface-variant mt-1" id="colorCieDisplay">CIE 1931: (0.58, 0.41)</span>
                    </div>
                  </div>
                  <div class="mt-6 flex flex-col gap-2">
                    <span class="font-label-sm text-[10px] text-on-surface-variant uppercase">Device Stack</span>
                    <div class="h-6 w-full flex rounded overflow-hidden">
                      <div class="w-1/5 bg-surface-bright border-r border-background/20"></div>
                      <div class="w-1/5 bg-primary-container/50 border-r border-background/20"></div>
                      <div class="w-1/5 bg-secondary" id="emlStackLayer"></div>
                      <div class="w-1/5 bg-tertiary/40 border-l border-background/20"></div>
                      <div class="w-1/5 bg-surface-bright"></div>
                    </div>
                  </div>
                </div>
                
                <div class="hidden bg-surface-container-low p-6 rounded-2xl border border-outline/5" id="solarSubPanel">
                  <span class="font-label-sm text-xs text-on-surface-variant tracking-wider uppercase block mb-4">Absorption Spectrum</span>
                  <div class="font-label-sm text-sm text-on-surface" id="solarCutoffLabel">Cutoff: λ<sub>c</sub> = 590 nm</div>
                  <svg class="w-full h-24 mt-4" preserveAspectRatio="none" viewBox="0 0 500 100">
                    <path d="M 30,90 Q 60,15 120,25 T 220,60 L 220,90 Z" fill="#8ed5ff" fill-opacity="0.35"></path>
                    <path d="M 220,60 Q 280,70 340,78 T 470,88 L 470,90 L 220,90 Z" fill="#31353e" fill-opacity="0.6"></path>
                    <line stroke="#ffb4ab" stroke-dasharray="3 3" stroke-width="1.5" x1="220" x2="220" y1="10" y2="90" id="solarCutoffLine"></line>
                    <text class="font-label-sm text-[10px]" fill="#ffb4ab" id="solarCutoffSvgText" x="225" y="25">Cutoff</text>
                  </svg>
                </div>
                
                <!-- Raw Values for DOM logic preservation -->
                <div class="hidden">
                  <span id="homoVal"></span><span id="lumoVal"></span><span id="ecVal"></span><span id="evVal"></span>
                  <span id="tradeoffEgBadge"></span><span id="canvasMobilitySub"></span>
                </div>
              </div>
              
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>

  <script>
""" + script_content + """
    
    // UI Drawer Logic
    function toggleDrawer() {
      const drawer = document.getElementById('drawer');
      const body = document.body;
      if (drawer.classList.contains('closed')) {
        drawer.classList.remove('closed');
        body.classList.add('drawer-open');
      } else {
        drawer.classList.add('closed');
        body.classList.remove('drawer-open');
      }
    }

    // Dossier Accordion Logic
    function toggleDossier() {
      const container = document.getElementById('dossier-container');
      const icon = document.getElementById('dossier-icon');
      if (container.classList.contains('dossier-open')) {
        container.classList.remove('dossier-open');
        icon.style.transform = 'rotate(0deg)';
      } else {
        container.classList.add('dossier-open');
        icon.style.transform = 'rotate(180deg)';
      }
    }
  </script>
</body>
</html>
"""

with open("simulator.html", "w") as f:
    f.write(new_html)
