"""
SemiSim Precision Physics & Chemistry Modeling Engine
Solid State & Optoelectronic Device Simulation:
1. Shockley-Queisser detailed-balance theoretical limit (ASTM G173-03 AM1.5G integration)
2. OLED Internal Quantum Efficiency (IQE) via PLQY and Spin-Statistics Exciton Harvest
3. Charge Transport (Gaussian Disorder Model for Organics, Hydrogenic Wannier-Mott for Inorganics)
"""

import os
import csv
import math
from typing import Dict, Any, Optional

# Physical Constants (CODATA 2018 standard)
Q = 1.602176634e-19          # Elementary charge (C)
H = 6.62607015e-34           # Planck constant (J*s)
C = 299792458.0              # Speed of light (m/s)
KB = 1.380649e-23            # Boltzmann constant (J/K)
KB_EV = 8.617333262e-5       # Boltzmann constant (eV/K)
EPSILON_0 = 8.8541878128e-12 # Vacuum permittivity (F/m)
RYDBERG_EV = 13.605693       # Hydrogen ground state energy (eV)

# Path to bundled reference spectrum
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
AM15_PATH = os.path.join(DATA_DIR, "am1.5g.csv")

# In-memory cached reference spectrum: list of (wavelength_m, spectral_irradiance_W_m2_m)
_SPECTRUM_CACHE = None

def load_am15g_spectrum():
    """
    Loads ASTM G173-03 AM1.5G spectrum from CSV.
    The file columns are:
    wavelength (nm), extraterrestrial (W/m2/nm), global (W/m2/nm), direct (W/m2/nm)
    We convert wavelength to meters and global irradiance to W/(m^2 * m).
    """
    global _SPECTRUM_CACHE
    if _SPECTRUM_CACHE is not None:
        return _SPECTRUM_CACHE

    if not os.path.exists(AM15_PATH):
        raise FileNotFoundError(f"AM1.5G data file not found at {AM15_PATH}")

    data = []
    with open(AM15_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or len(row) < 3:
                continue
            try:
                wl_nm = float(row[0].strip())
                global_irrad_nm = float(row[2].strip())
            except ValueError:
                continue
            
            wl_m = wl_nm * 1e-9
            # Convert W/(m^2 * nm) to W/(m^2 * m) -> multiply by 1e9
            irrad_m = global_irrad_nm * 1e9
            data.append((wl_m, irrad_m))

    data.sort(key=lambda x: x[0])
    _SPECTRUM_CACHE = data
    return _SPECTRUM_CACHE


def calculate_shockley_queisser(eg_eV: float, temp_K: float = 300.0, concentration: float = 1.0) -> Dict[str, float]:
    """
    Performs full Shockley-Queisser detailed-balance calculation.
    
    1. J_sc = q * integral_{0}^{lambda_g} (I(lambda) * lambda / (h * c)) d_lambda
       where lambda_g = h * c / (eg_eV * q)
    2. J_0 = q * (2 * pi / (h^3 * c^2)) * integral_{E_g}^{inf} E^2 / (exp(E / (k*T)) - 1) dE
       (Blackbody emission at cell temperature into 2*pi solid angle)
    3. Voc = (k*T / q) * ln( (concentration * J_sc) / J_0 + 1 )
    4. Fill Factor FF via empirical SQ relation:
       v_oc = q * Voc / (k * T)
       FF = (v_oc - ln(v_oc + 0.72)) / (v_oc + 1)
    5. PCE = (concentration * J_sc * Voc * FF) / (P_in * concentration)
       where P_in = 1000 W/m^2 (nominal AM1.5G 1 sun)
    """
    if eg_eV <= 0.2:
        eg_eV = 0.2
    
    # 1. Short-circuit current density J_sc
    spectrum = load_am15g_spectrum()
    eg_J = eg_eV * Q
    cutoff_wl_m = (H * C) / eg_J

    jsc_A_m2 = 0.0
    for i in range(len(spectrum) - 1):
        wl1, irr1 = spectrum[i]
        wl2, irr2 = spectrum[i+1]

        if wl1 >= cutoff_wl_m:
            break

        # If interval crosses cutoff wavelength, clip it
        if wl2 > cutoff_wl_m:
            fraction = (cutoff_wl_m - wl1) / (wl2 - wl1)
            wl2 = cutoff_wl_m
            irr2 = irr1 + fraction * (irr2 - irr1)

        # Photon flux: Phi(lambda) = I(lambda) * lambda / (h * c)
        phi1 = irr1 * wl1 / (H * C)
        phi2 = irr2 * wl2 / (H * C)

        # Trapezoidal integration of photon flux * q
        d_wl = wl2 - wl1
        jsc_A_m2 += Q * 0.5 * (phi1 + phi2) * d_wl

        if wl2 >= cutoff_wl_m:
            break

    jsc_A_m2 *= concentration

    # 2. Dark saturation current density J_0 via blackbody emission
    # J_0 = q * (2 * pi / (h^3 * c^2)) * int_{E_g}^{inf} E^2 / (exp(E / kT) - 1) dE
    kT_J = KB * temp_K
    E_max_J = eg_J + 4.0 * Q
    num_steps = 2000
    dE = (E_max_J - eg_J) / num_steps

    integral_bb = 0.0
    for step in range(num_steps):
        E1 = eg_J + step * dE
        E2 = E1 + dE

        # To avoid overflow, cap exponent
        x1 = min(E1 / kT_J, 700.0)
        x2 = min(E2 / kT_J, 700.0)

        f1 = (E1 ** 2) / (math.exp(x1) - 1.0)
        f2 = (E2 ** 2) / (math.exp(x2) - 1.0)

        integral_bb += 0.5 * (f1 + f2) * dE

    prefactor = Q * (2.0 * math.pi) / ((H ** 3) * (C ** 2))
    j0_A_m2 = prefactor * integral_bb

    # 3. Open-circuit voltage Voc
    vt = (KB * temp_K) / Q  # Thermal voltage ~ 0.02585 V at 300K
    if jsc_A_m2 > 0 and j0_A_m2 > 0:
        voc_V = vt * math.log((jsc_A_m2 / j0_A_m2) + 1.0)
    else:
        voc_V = 0.0

    # 4. Fill factor FF (standard Green / Shockley-Queisser empirical relation)
    if voc_V > 0 and vt > 0:
        v_oc = voc_V / vt
        ff = (v_oc - math.log(v_oc + 0.72)) / (v_oc + 1.0)
        ff = max(0.0, min(ff, 0.95))
    else:
        ff = 0.0

    # 5. Power conversion efficiency (PCE)
    p_in_W_m2 = 1000.0 * concentration
    p_max_W_m2 = jsc_A_m2 * voc_V * ff
    pce = (p_max_W_m2 / p_in_W_m2) * 100.0

    jsc_mA_cm2 = jsc_A_m2 / 10.0  # 1 A/m^2 = 0.1 mA/cm^2

    return {
        "jsc_mA_cm2": round(jsc_mA_cm2, 2),
        "voc_V": round(voc_V, 3),
        "ff_pct": round(ff * 100.0, 1),
        "pce_pct": round(max(0.0, pce), 2),
        "j0_A_m2": j0_A_m2,
        "eg_eV": eg_eV,
        "temp_K": temp_K
    }


# Materials database for OLED and Transport models
ORGANIC_PRESETS = {
    "Alq3 (Tris(8-hydroxyquinolinato)aluminium)": {
        "type": "fluorescent",
        "plqy": 0.32,
        "eta_s": 0.25,
        "epsilon_r": 3.4,
        "r_exciton_nm": 0.8,
        "homo": -5.70,
        "lumo": -3.00,
        "eg": 2.70,
        "mu0": 1.0e-2
    },
    "Poly(p-phenylene vinylene) PPV": {
        "type": "fluorescent",
        "plqy": 0.27,
        "eta_s": 0.25,
        "epsilon_r": 3.2,
        "r_exciton_nm": 0.9,
        "homo": -5.10,
        "lumo": -2.85,
        "eg": 2.25,
        "mu0": 1.0e-2
    },
    "P3HT:PCBM Blend (OPV Benchmark)": {
        "type": "blend",
        "plqy": 0.15,
        "eta_s": 0.25,
        "epsilon_r": 3.8,
        "r_exciton_nm": 1.0,
        "homo": -5.20,
        "lumo": -3.30,
        "eg": 1.90,
        "mu0": 1.0e-2
    },
    "Spiro-OMeTAD (HTL Emissive)": {
        "type": "fluorescent",
        "plqy": 0.38,
        "eta_s": 0.25,
        "epsilon_r": 3.0,
        "r_exciton_nm": 0.75,
        "homo": -5.22,
        "lumo": -2.22,
        "eg": 3.00,
        "mu0": 1.0e-2
    },
    "Ir(ppy)3 (Green Phosphor Benchmark)": {
        "type": "phosphorescent",
        "plqy": 0.88,
        "eta_s": 1.00,
        "epsilon_r": 3.5,
        "r_exciton_nm": 0.85,
        "homo": -5.30,
        "lumo": -2.80,
        "eg": 2.50,
        "mu0": 1.0e-2
    }
}

INORGANIC_PRESETS = {
    "Crystalline Silicon (c-Si)": {
        "eg": 1.12,
        "mu_reduced": 0.038,  # exciton reduced mass mu* / m0
        "epsilon_r": 11.7,
        "mobility": 1400.0,   # cm^2 / V*s
        "homo": -5.17,
        "lumo": -4.05
    },
    "Gallium Arsenide (GaAs Direct)": {
        "eg": 1.42,
        "mu_reduced": 0.050,
        "epsilon_r": 12.9,
        "mobility": 8500.0,
        "homo": -5.49,
        "lumo": -4.07
    },
    "Cadmium Telluride (CdTe)": {
        "eg": 1.50,
        "mu_reduced": 0.075,
        "epsilon_r": 10.2,
        "mobility": 1050.0,
        "homo": -5.80,
        "lumo": -4.30
    },
    "Halide Perovskite (CH3NH3PbI3)": {
        "eg": 1.55,
        "mu_reduced": 0.104,
        "epsilon_r": 25.0,     # Low frequency screening
        "mobility": 40.0,
        "homo": -5.45,
        "lumo": -3.90
    }
}


def calculate_oled_iqe(material_preset: str, charge_balance: float = 0.9) -> Dict[str, Any]:
    """
    Computes OLED Internal Quantum Efficiency (IQE) and estimated External Quantum Efficiency (EQE).
    IQE = gamma (charge balance factor) * eta_ST (spin-statistics harvest factor) * Phi_PL (emitter PLQY)
    EQE = IQE * eta_outcoupling
    where planar ITO/glass outcoupling factor eta_outcoupling approx 1 / (2 * n^2) approx 0.20-0.22.
    """
    preset_data = None
    for name, data in ORGANIC_PRESETS.items():
        if material_preset.lower() in name.lower() or name.lower() in material_preset.lower():
            preset_data = data
            break

    if not preset_data:
        preset_data = ORGANIC_PRESETS["Alq3 (Tris(8-hydroxyquinolinato)aluminium)"]

    plqy = preset_data["plqy"]
    eta_s = preset_data["eta_s"]
    iqe = charge_balance * eta_s * plqy

    # Planar glass/ITO refractive index n ~ 1.7 -> outcoupling ~ 1 / (2 * n^2) ~ 0.20
    outcoupling_efficiency = 0.20
    eqe = iqe * outcoupling_efficiency

    spin_limit_label = "η_S=25% (fluorescent singlet limit)" if eta_s <= 0.25 else "η_S=100% (phosphorescent / triplet harvest)"

    return {
        "iqe_pct": round(iqe * 100.0, 1),
        "eqe_pct": round(eqe * 100.0, 2),
        "spin_statistics_limit_pct": round(eta_s * 100.0, 1),
        "plqy_used": plqy,
        "charge_balance": charge_balance,
        "emitter_type": preset_data["type"],
        "spin_limit_label": spin_limit_label,
        "outcoupling_factor": outcoupling_efficiency
    }


def calculate_transport_properties(
    eg_eV: float,
    mat_class: str = "organic",
    disorder_eV: float = 0.08,
    temp_K: float = 300.0,
    preset: Optional[str] = None
) -> Dict[str, Any]:
    """
    Computes charge carrier mobility and exciton binding energy based on physical models:
    
    Organics (Gaussian Disorder Model, Bässler/Pasveer approximation):
      mu(sigma, T) = mu_0 * exp(-(2 * sigma / (3 * k_B * T))^2)
      Exciton binding energy (Frenkel):
      E_b = e^2 / (4 * pi * epsilon_0 * epsilon_r * r_exciton)
      
    Inorganics:
      Mobility based on crystalline band structure.
      Exciton binding energy (Wannier-Mott hydrogenic approximation):
      E_b = 13.6 eV * (mu* / m_0) / epsilon_r^2
    """
    is_inorganic = (mat_class.lower().startswith("inorg") or "cryst" in mat_class.lower())

    if not is_inorganic:
        # Match organic preset or default
        matched_preset = None
        if preset:
            for name, data in ORGANIC_PRESETS.items():
                if preset.lower() in name.lower() or name.lower() in preset.lower():
                    matched_preset = data
                    break
        if not matched_preset:
            matched_preset = ORGANIC_PRESETS["Alq3 (Tris(8-hydroxyquinolinato)aluminium)"]

        # Gaussian Disorder Model (GDM):
        # mu(sigma, T) = mu0 * exp(-(2 * sigma / (3 * kT))^2)
        # reference disorder-free mobility mu0 ~ 1.0e-2 cm^2 / V*s
        mu0 = matched_preset.get("mu0", 1.0e-2)
        kT = KB_EV * temp_K  # ~ 0.02585 eV at 300K
        
        if kT > 0 and disorder_eV >= 0:
            arg = (2.0 * disorder_eV) / (3.0 * kT)
            mobility = mu0 * math.exp(-(arg ** 2))
        else:
            mobility = mu0

        # Frenkel Exciton Binding Energy:
        # E_b = e / (4 * pi * epsilon_0 * epsilon_r * r) in eV
        eps_r = matched_preset.get("epsilon_r", 3.4)
        r_m = matched_preset.get("r_exciton_nm", 0.8) * 1e-9
        eb_J = (Q ** 2) / (4.0 * math.pi * EPSILON_0 * eps_r * r_m)
        eb_eV = eb_J / Q

        return {
            "mobility_cm2_Vs": mobility,
            "mobility_formatted": f"{mobility:.1e} cm²/(V·s)" if mobility < 0.01 else f"{mobility:.3f} cm²/(V·s)",
            "exciton_binding_eV": round(eb_eV, 3),
            "exciton_binding_meV": round(eb_eV * 1000.0, 1),
            "exciton_type": "Frenkel (Localized)",
            "model_used": "Gaussian Disorder Model (Bässler)"
        }

    else:
        # Inorganic Semiconductor
        matched_preset = None
        if preset:
            for name, data in INORGANIC_PRESETS.items():
                if preset.lower() in name.lower() or name.lower() in preset.lower():
                    matched_preset = data
                    break
        if not matched_preset:
            matched_preset = INORGANIC_PRESETS["Crystalline Silicon (c-Si)"]

        mobility = matched_preset["mobility"]
        mu_reduced = matched_preset["mu_reduced"]
        eps_r = matched_preset["epsilon_r"]

        # Hydrogenic Wannier-Mott binding energy:
        # E_b = 13.6 eV * (mu* / m0) / (eps_r^2)
        eb_eV = RYDBERG_EV * mu_reduced / (eps_r ** 2)

        return {
            "mobility_cm2_Vs": mobility,
            "mobility_formatted": f"{mobility:,.0f} cm²/(V·s)",
            "exciton_binding_eV": round(eb_eV, 4),
            "exciton_binding_meV": round(eb_eV * 1000.0, 2),
            "exciton_type": "Wannier-Mott (Delocalized)",
            "model_used": "Boltzmann Band Transport (Bloch Waves)"
        }
