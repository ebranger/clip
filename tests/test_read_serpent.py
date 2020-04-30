
import unittest

from clip.read_serpent_output import *

class TestReadSerpent(unittest.TestCase):
    
    def test_binning(self):
        
        bins = [0.3, 0.4, 0.5]
        
        #gamma energy in the middle of bin, will be added with weight 1.
        binned_spectrum = convert_to_ORIGEN_binning([0.35], [1], bins)
        self.assertAlmostEqual(binned_spectrum[0], 1, places=6)
        self.assertAlmostEqual(binned_spectrum[1], 0, places=6)
        self.assertEqual(len(binned_spectrum), 2)
        
        #gamma energy in the low range of a bin, will be added with weight 0.31/0.35.
        binned_spectrum = convert_to_ORIGEN_binning([0.31], [1], bins)
        self.assertAlmostEqual(binned_spectrum[0], 0.31/0.35, places=6)
        self.assertAlmostEqual(binned_spectrum[1], 0, places=6)
        
        #gamma energy below the lowest bin, will be ignored.
        binned_spectrum = convert_to_ORIGEN_binning([0.29], [1], bins)
        self.assertAlmostEqual(binned_spectrum[0], 0, places=6)
        self.assertAlmostEqual(binned_spectrum[1], 0, places=6)
        
        #splitting a gamma line that was close to but below a boundary.
        binned_spectrum = convert_to_ORIGEN_binning([0.399], [1], bins)
        self.assertAlmostEqual(binned_spectrum[0], 0.399/(0.35*2), places=6)
        self.assertAlmostEqual(binned_spectrum[1], 0.399/(0.45*2), places=6)
        
        #splitting a gamma line that was close to but above a boundary.
        binned_spectrum = convert_to_ORIGEN_binning([0.401], [1], bins)
        self.assertAlmostEqual(binned_spectrum[0], 0.401/(0.35*2), places=6)
        self.assertAlmostEqual(binned_spectrum[1], 0.401/(0.45*2), places=6)
        
        #gamma energy above the highest bin, will be ignored.
        binned_spectrum = convert_to_ORIGEN_binning([0.251], [1], bins)
        self.assertAlmostEqual(binned_spectrum[0], 0, places=6)
        self.assertAlmostEqual(binned_spectrum[1], 0, places=6)
    
    def test_read_serpent_gamma_spectrum(self):
        #Test reading in the Cs137 662 keV gamma line from a gamma spectrum file (Which actaully comes from Ba137m)
        
        spectrum_energies, spectrum_counts = read_serpent_gamma_spectrum("Example_Serpent_outputs/PWR_50MWd_10years_gamma.m")

        #Ba-137m emission, which is often considered to be part of the Cs137 decay chain.
        self.assertTrue(6.61660E-01 in spectrum_energies)
        position = spectrum_energies.index(6.61660E-01)
        self.assertAlmostEqual(spectrum_counts[position], 17967366148.532, places=2)
    
    def test_read_serpent_isotope_contents(self):
        
        isotope_contents = read_serpent_isotope_contents("Example_Serpent_outputs/PWR_50MWd_10years.bumat", ["Cs137"])
        
        self.assertAlmostEqual(isotope_contents[0], 0.0128834663837, places=10)
    
if __name__ == '__main__':
    unittest.main()