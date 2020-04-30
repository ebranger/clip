
import unittest

from clip.read_responses import *

class TestReadResponses(unittest.TestCase):
    
    def test_binned_response(self):
        
        bin_edges, bin_count, bin_uncertainty = read_binned_response("Data/Binned_gamma_response/PWR17x17.txt")
        
        #Check the Cs137 662 keV bin
        self.assertEqual(bin_edges[16], 6.00E-1)
        self.assertEqual(bin_edges[17], 7.00E-1)
        self.assertEqual(bin_count[16], 0.000139939)
        self.assertEqual(bin_uncertainty[16], 5.04E-06)
          
    def test_sampled_response(self):
        
        sampled_energies, response, uncertainty = read_sampled_response("Data/Sampled_gamma_response/PWR17x17.txt")
        
        #Check the Cs137 662 keV closest sample
        self.assertEqual(sampled_energies[21], 0.66)
        self.assertEqual(response[21], 0.000150779)
        self.assertEqual(uncertainty[21], 1.03E-06)
        
    def test_isotope_response_activity(self):
        
        isotope_list, isotope_response_activity, isotope_uncertainty_activity = read_isotope_response("Data/Isotope_gamma_response/PWR17x17.txt", "decay")
        
        #Check the Cs137 isotope response
        self.assertEqual(isotope_list[2], "Cs137")
        self.assertEqual(isotope_response_activity[2], 1.192E-04)
        self.assertEqual(isotope_uncertainty_activity[2], 4.294E-06)
        
    def test_isotope_response_mass(self):
        
        isotope_list, isotope_response_mass, isotope_uncertainty_mass = read_isotope_response("Data/Isotope_gamma_response/PWR17x17.txt", "mass")
        
        #Check the Cs137 isotope response
        self.assertEqual(isotope_list[2], "Cs137")
        self.assertEqual(isotope_response_mass[2], 3.882E+08)
        self.assertEqual(isotope_uncertainty_mass[2], 1.398E+07)
        
if __name__ == '__main__':
    unittest.main()