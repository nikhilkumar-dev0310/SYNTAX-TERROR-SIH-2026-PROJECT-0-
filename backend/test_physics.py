"""
Unit tests for SemiSim Physics Engine.
Uses standard library unittest so no external test dependencies are required.
"""

import unittest
from backend.physics import (
    calculate_shockley_queisser,
    calculate_oled_iqe,
    calculate_transport_properties
)

class TestSemiSimPhysics(unittest.TestCase):

    def test_shockley_queisser_peak_and_materials(self):
        # 1. Theoretical Shockley-Queisser optimum at 1.34 eV at 300K is ~33.7%
        sq_134 = calculate_shockley_queisser(1.34, temp_K=300.0)
        self.assertAlmostEqual(sq_134["pce_pct"], 33.7, delta=0.5,
                               msg=f"Expected ~33.7%, got {sq_134['pce_pct']}")
        self.assertGreater(sq_134["voc_V"], 1.0,
                           msg=f"Expected Voc > 1.0V, got {sq_134['voc_V']}")
        self.assertTrue(30.0 <= sq_134["jsc_mA_cm2"] <= 40.0,
                        msg=f"Expected Jsc between 30 and 40 mA/cm2, got {sq_134['jsc_mA_cm2']}")
        self.assertGreater(sq_134["ff_pct"], 85.0,
                           msg=f"Expected FF > 85%, got {sq_134['ff_pct']}")

        # 2. Silicon (1.12 eV, theoretical limit ~33%)
        sq_si = calculate_shockley_queisser(1.12, temp_K=300.0)
        self.assertTrue(32.5 <= sq_si["pce_pct"] <= 34.0,
                        msg=f"Si PCE expected ~33%, got {sq_si['pce_pct']}")
        self.assertTrue(40.0 <= sq_si["jsc_mA_cm2"] <= 46.0,
                        msg=f"Si Jsc expected 40-46 mA/cm2, got {sq_si['jsc_mA_cm2']}")

        # 3. Gallium Arsenide (1.42 eV, theoretical limit ~33%)
        sq_gaas = calculate_shockley_queisser(1.42, temp_K=300.0)
        self.assertTrue(32.0 <= sq_gaas["pce_pct"] <= 34.0,
                        msg=f"GaAs PCE expected ~33%, got {sq_gaas['pce_pct']}")

    def test_oled_iqe_spin_statistics(self):
        # Alq3: fluorescent (eta_S = 0.25, PLQY = 0.32, charge_balance = 0.9)
        # IQE = 0.9 * 0.25 * 0.32 = 0.072 = 7.2%
        alq3 = calculate_oled_iqe("Alq3 (Tris(8-hydroxyquinolinato)aluminium)")
        self.assertEqual(alq3["iqe_pct"], 7.2)
        self.assertEqual(alq3["spin_statistics_limit_pct"], 25.0)
        self.assertIn("25%", alq3["spin_limit_label"])
        self.assertEqual(alq3["eqe_pct"], 1.44)

        # Phosphorescent emitter Ir(ppy)3: (eta_S = 1.0, PLQY = 0.88, charge_balance = 0.9)
        # IQE = 0.9 * 1.0 * 0.88 = 0.792 = 79.2%
        phosphor = calculate_oled_iqe("Ir(ppy)3 (Green Phosphor Benchmark)")
        self.assertEqual(phosphor["iqe_pct"], 79.2)
        self.assertEqual(phosphor["spin_statistics_limit_pct"], 100.0)
        self.assertIn("100%", phosphor["spin_limit_label"])

    def test_transport_properties_inorganic_silicon(self):
        # Si Wannier-Mott exciton binding energy ~ 3.8 meV (< 10 meV)
        si_props = calculate_transport_properties(1.12, mat_class="inorganic", preset="Crystalline Silicon (c-Si)")
        self.assertTrue(3.0 <= si_props["exciton_binding_meV"] <= 4.5,
                        f"Expected ~3.8 meV, got {si_props['exciton_binding_meV']}")
        self.assertTrue(si_props["exciton_type"].startswith("Wannier-Mott"))
        self.assertEqual(si_props["mobility_cm2_Vs"], 1400.0)

    def test_transport_properties_organic_gdm(self):
        # GDM mobility decreases with energetic disorder sigma
        low_disorder = calculate_transport_properties(2.1, mat_class="organic", disorder_eV=0.04)
        high_disorder = calculate_transport_properties(2.1, mat_class="organic", disorder_eV=0.10)
        self.assertGreater(low_disorder["mobility_cm2_Vs"], high_disorder["mobility_cm2_Vs"])
        # Frenkel binding energy ~ 0.3 to 0.8 eV
        self.assertTrue(0.3 <= low_disorder["exciton_binding_eV"] <= 0.8)
        self.assertTrue(low_disorder["exciton_type"].startswith("Frenkel"))

if __name__ == "__main__":
    unittest.main()
