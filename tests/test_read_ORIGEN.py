
import unittest

from clip.read_ORIGEN_output import *

class TestReadORIGENOutput(unittest.TestCase):
    
    def test_read_gamma_spectrum(self):
        
        #Read two gamma spectra, from two cooling time runs. I.e. the data comes from two different places.
        bin_edges, bin_count = read_ORIGEN_gamma_spectrum("Example_ORIGEN_outputs/PWR_50MWd_test.out", "1.0 y")
        
        #Check the bin containing Cs-137
        self.assertEqual(bin_edges[16], 6.00E-1)
        self.assertEqual(bin_edges[17], 7.00E-1)
        self.assertEqual(bin_count[16], 1.187E+16)
        
        bin_edges, bin_count = read_ORIGEN_gamma_spectrum("Example_ORIGEN_outputs/PWR_50MWd_test.out", "10.0 y")
        
        #Check the bin containing Cs-137
        self.assertEqual(bin_edges[16], 6.00E-1)
        self.assertEqual(bin_edges[17], 7.00E-1)
        self.assertEqual(bin_count[16], 4.221E+15)
        
        #Test for a cooling time that does not exists
        
        print("A cooling time of 100 years is not provided in the input data, so the input reader should now fail to find it.")
        bin_edges, bin_count = read_ORIGEN_gamma_spectrum("Example_ORIGEN_outputs/PWR_50MWd_test.out", "100.0 y")
        
        #Check the bin containing Cs-137
        self.assertEqual(bin_edges, [0])
        self.assertEqual(bin_count, [0])
        
    def test_read_isotopes(self):
        
        isotope_contents = read_ORIGEN_isotope_contents("Example_ORIGEN_outputs/PWR_50MWd_test.out", "10.0 y", ["Cs137"])
        
        self.assertEqual(isotope_contents[0], 1.412E+03)
          
    
if __name__ == '__main__':
    unittest.main()