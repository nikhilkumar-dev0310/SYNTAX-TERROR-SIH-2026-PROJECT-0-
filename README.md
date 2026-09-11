# SemiSim: Band Gap & Charge Transport Explorer

SemiSim is an interactive physics and materials chemistry laboratory simulation platform designed for optoelectronic device modeling (OLEDs and Photovoltaics). It replaces heuristic approximations with rigorous physical solvers for the Shockley-Queisser detailed-balance limit, OLED internal quantum efficiency decomposition, and charge carrier transport models.

---

## 🔬 Core Physics Models & Assumptions

### 1. Shockley-Queisser Detailed-Balance Limit (`POST /api/solar/efficiency`)
- **Reference Solar Spectrum**: ASTM G173-03 AM1.5G terrestrial global tilt reference spectrum ($1000\text{ W/m}^2$, $280\text{ nm} - 4000\text{ nm}$, 2002 tabulated wavelengths).
- **Short-Circuit Current Density ($J_{sc}$)**:
  $$J_{sc} = q \int_0^{\lambda_g} \Phi(\lambda) d\lambda = q \int_0^{\lambda_g} \frac{I(\lambda) \lambda}{hc} d\lambda$$
  where $\lambda_g = \frac{hc}{E_g}$ is the optical absorption threshold cutoff.
- **Dark Saturation Current ($J_0$)**: Radiative blackbody recombination into the hemisphere at cell temperature $T$ ($300\text{ K}$):
  $$J_0 = q \frac{2\pi}{h^3 c^2} \int_{E_g}^\infty \frac{E^2}{\exp\left(\frac{E}{k_B T}\right) - 1} dE$$
- **Open-Circuit Voltage ($V_{oc}$)**: Ideal diode equation under open-circuit condition:
  $$V_{oc} = \frac{k_B T}{q} \ln\left(\frac{C \cdot J_{sc}}{J_0} + 1\right)$$
- **Fill Factor ($FF$)**: Standard empirical relation for ideal solar cells:
  $$v_{oc} = \frac{q V_{oc}}{k_B T}, \quad FF = \frac{v_{oc} - \ln(v_{oc} + 0.72)}{v_{oc} + 1}$$
- **Power Conversion Efficiency ($PCE$)**:
  $$PCE = \frac{J_{sc} \cdot V_{oc} \cdot FF}{P_{in}} \times 100\%$$
- **Validation**:
  - $E_g = 1.34\text{ eV} \implies PCE \approx 33.7\%$ (maximum theoretical limit).
  - Silicon ($E_g = 1.12\text{ eV}$) $\implies PCE \approx 33.4\%$, $J_{sc} \approx 43.8\text{ mA/cm}^2$.
  - GaAs ($E_g = 1.42\text{ eV}$) $\implies PCE \approx 33.2\%$, $J_{sc} \approx 32.1\text{ mA/cm}^2$.

---

### 2. OLED Internal Quantum Efficiency (IQE) & Spin Statistics (`POST /api/oled/iqe`)
- **Decomposition**:
  $$IQE = \gamma \times \eta_{S/T} \times \Phi_{PL}$$
  - $\gamma$: Charge carrier balance factor ($\approx 0.90$).
  - $\eta_{S/T}$: Spin-statistics exciton harvest factor:
    - **Fluorescent emitters** (e.g. Alq3, PPV): $\eta_S = 0.25$ ($25\%$ singlet harvest ceiling).
    - **Phosphorescent / TADF emitters** (e.g. $\text{Ir(ppy)}_3$): $\eta_T \approx 1.00$ ($100\%$ singlet + triplet harvest via strong spin-orbit coupling or reverse intersystem crossing).
  - $\Phi_{PL}$: Photoluminescence Quantum Yield (PLQY) from literature (Alq3 $\approx 0.32$, $\text{Ir(ppy)}_3 \approx 0.88$).
- **External Quantum Efficiency (EQE) Estimate**:
  $$EQE = IQE \times \eta_{out}$$
  using the planar glass/ITO dipole outcoupling approximation $\eta_{out} \approx \frac{1}{2n^2} \approx 0.20$ ($n \approx 1.7-1.8$).

---

### 3. Charge Carrier Transport & Exciton Binding (`POST /api/transport/properties`)
- **Organics (Gaussian Disorder Model, Bässler / Pasveer)**:
  $$\mu(\sigma, T) = \mu_0 \exp\left(-\left(\frac{2\sigma}{3 k_B T}\right)^2\right)$$
  where $\mu_0 = 10^{-2}\text{ cm}^2/\text{V}\cdot\text{s}$ is the disorder-free polaron hopping mobility and $\sigma$ is the energetic disorder parameter ($0.02 - 0.18\text{ eV}$).
- **Frenkel Exciton Binding (Organics)**:
  $$E_b \approx \frac{e^2}{4\pi \varepsilon_0 \varepsilon_r r_{exc}} \approx 0.3 - 0.8\text{ eV}$$
  due to low dielectric screening ($\varepsilon_r \approx 3.0 - 3.8$, $r_{exc} \approx 0.8\text{ nm}$).
- **Inorganics (Hydrogenic Wannier-Mott Model)**:
  $$E_b = 13.606\text{ eV} \times \frac{\mu^* / m_0}{\varepsilon_r^2}$$
  where $\mu^* = (m_e^{*-1} + m_h^{*-1})^{-1}$ is the exciton reduced effective mass.
  - Silicon ($c\text{-Si}$): $\mu^* \approx 0.038 m_0, \varepsilon_r = 11.7 \implies E_b \approx 3.78\text{ meV}$ ($< k_B T \approx 25.85\text{ meV}$ $\implies$ spontaneous thermal ionization into free carriers at room temperature).
  - Gallium Arsenide (GaAs): $\mu^* \approx 0.050 m_0, \varepsilon_r = 12.9 \implies E_b \approx 4.09\text{ meV}$.

---

## 🚀 Running Locally

### 1. Backend (FastAPI + Uvicorn)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
API endpoints will be live at `http://localhost:8000` (docs at `http://localhost:8000/docs`).

### 2. Frontend (Static HTML/JS)
```bash
# From project root
python3 -m http.server 3000
```
Open `http://localhost:3000` in your web browser:
- `index.html`: Overview & Orientation
- `simulator.html`: Live Simulator Workspace with debounced physics calls & particle dynamics canvas
- `evaluation.html`: Engineering Decisions (Coatings, Org vs Inorg, Application Scenarios)
- `export.html`: Publication Lab Report with editable justifications & LaTeX/JSON export

---

## 🌐 Deployment Architecture
- **Backend**: Render Web Service (`uvicorn main:app --host 0.0.0.0 --port $PORT`).
- **Frontend**: Vercel Static deployment.
- **Cross-Origin Configuration**: In `api-config.js`, update `API_CONFIG.BASE_URL` with your Render service URL when running in production. CORS is enabled for all origins on the backend.

---

## 🧪 Running Unit Tests
```bash
python3 -m unittest backend/test_physics.py
```
Validates:
1. Shockley-Queisser $1.34\text{ eV}$ peak reaches $33.7\% \pm 0.5\%$.
2. Alq3 fluorescent IQE calculates to $7.2\%$, contrasting with phosphorescent $\approx 79.2\%$.
3. Crystalline Silicon Wannier-Mott $E_b$ evaluates to $\approx 3.8\text{ meV}$.
4. Organic GDM mobility decreases monotonically with energetic disorder $\sigma$.
