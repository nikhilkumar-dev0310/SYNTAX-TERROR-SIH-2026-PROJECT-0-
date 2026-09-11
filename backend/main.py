"""
SemiSim Precision Physics API Service
Solid-State Device Physics & Optoelectronic Engineering Workbench
Provides endpoints for:
1. Shockley-Queisser Detailed-Balance Solar Cell Efficiency (ASTM G173-03 AM1.5G)
2. OLED Internal Quantum Efficiency & Spin-Statistics Exciton Harvesting
3. Charge Transport Properties (Gaussian Disorder Model & Hydrogenic Wannier-Mott)
"""

import logging
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.physics import (
    calculate_shockley_queisser,
    calculate_oled_iqe,
    calculate_transport_properties,
    ORGANIC_PRESETS,
    INORGANIC_PRESETS
)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("semisim-api")

app = FastAPI(
    title="SemiSim Physics API",
    description="Precision optoelectronic and solid-state device physics simulation engine.",
    version="2.4.0"
)

# Enable CORS for Render/Vercel and localhost cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class SolarEfficiencyRequest(BaseModel):
    eg_eV: float = Field(..., ge=0.2, le=5.0, description="Band gap in electronvolts")
    temp_K: float = Field(300.0, ge=10.0, le=600.0, description="Operating temperature in Kelvin")
    concentration: float = Field(1.0, ge=1.0, le=1000.0, description="Solar concentration factor (suns)")

class OledIqeRequest(BaseModel):
    material_preset: str = Field("Alq3", description="Material preset or emitter system name")
    charge_balance: float = Field(0.9, ge=0.0, le=1.0, description="Charge balance factor gamma")

class TransportPropertiesRequest(BaseModel):
    eg_eV: float = Field(2.1, ge=0.2, le=5.0, description="Band gap in electronvolts")
    mat_class: str = Field("organic", description="'organic' or 'inorganic'")
    disorder_eV: float = Field(0.08, ge=0.01, le=0.3, description="Energetic disorder sigma in eV (organic only)")
    temp_K: float = Field(300.0, ge=10.0, le=600.0, description="Temperature in Kelvin")
    preset: Optional[str] = Field(None, description="Selected material preset name")


@app.get("/health")
@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "service": "SemiSim Precision Computational Engine",
        "version": "v2.4.0",
        "solver": "Poisson-Coupled Detailed Balance",
        "reference_spectrum": "ASTM G173-03 AM1.5G (Global Tilt 1000 W/m²)"
    }


@app.post("/api/solar/efficiency")
async def api_solar_efficiency(req: SolarEfficiencyRequest):
    """
    Computes theoretical Shockley-Queisser detailed balance efficiency limit,
    short-circuit current Jsc, dark saturation current J0, open-circuit voltage Voc,
    and empirical fill factor FF under AM1.5G irradiation.
    """
    try:
        results = calculate_shockley_queisser(
            eg_eV=req.eg_eV,
            temp_K=req.temp_K,
            concentration=req.concentration
        )
        return results
    except Exception as e:
        logger.exception("Error in solar efficiency calculation")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/oled/iqe")
async def api_oled_iqe(req: OledIqeRequest):
    """
    Computes OLED Internal Quantum Efficiency (IQE) and planar outcoupled EQE
    based on emitter photoluminescence quantum yield (PLQY), spin-statistics
    exciton harvesting (25% singlet ceiling vs 100% phosphor/TADF), and charge balance.
    """
    try:
        results = calculate_oled_iqe(
            material_preset=req.material_preset,
            charge_balance=req.charge_balance
        )
        return results
    except Exception as e:
        logger.exception("Error in OLED IQE calculation")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/transport/properties")
async def api_transport_properties(req: TransportPropertiesRequest):
    """
    Recomputes charge carrier mobility and exciton binding energy:
    - Organics: Gaussian Disorder Model (GDM, Bässler) mu(sigma, T) + Frenkel Coulombic binding.
    - Inorganics: Hydrogenic Wannier-Mott exciton binding Eb = 13.6 eV * (mu*/m0) / eps_r^2.
    """
    try:
        results = calculate_transport_properties(
            eg_eV=req.eg_eV,
            mat_class=req.mat_class,
            disorder_eV=req.disorder_eV,
            temp_K=req.temp_K,
            preset=req.preset
        )
        return results
    except Exception as e:
        logger.exception("Error in transport properties calculation")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/presets")
async def get_presets():
    """
    Returns available verified material presets for organic and inorganic classes.
    """
    return {
        "organic": list(ORGANIC_PRESETS.keys()),
        "inorganic": list(INORGANIC_PRESETS.keys())
    }
