
import unittest

from clip.isotope_data import *

class TestIsotopeData(unittest.TestCase):
    
    def test_name_conversion(self):
        
        ORIGEN_name = "Cs137"
        Serpent_name = "55137"
        
        #Two correct conversions
        self.assertEqual(convert_isotope_name(Serpent_name, "ORIGEN"), ORIGEN_name)
        self.assertEqual(convert_isotope_name(ORIGEN_name, "Serpent"), Serpent_name)
        
        #Will not convert to itself
        self.assertEqual(convert_isotope_name(ORIGEN_name, "ORIGEN"), "")
        
    def test_isotope_mass(self):
        
        ORIGEN_name = "Cs137"
        Serpent_name = "55137"
        Cs_mass = 136.907090
        
        #Masses that are available
        self.assertEqual(get_isotope_mass(ORIGEN_name, "ORIGEN"), Cs_mass)
        self.assertEqual(get_isotope_mass(Serpent_name, "Serpent"), Cs_mass)
        
        #Mass for isotope that does not exist.
        self.assertEqual(get_isotope_mass("Pu186", "Serpent"), 0)
    
if __name__ == '__main__':
    unittest.main()