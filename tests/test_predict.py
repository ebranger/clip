
import unittest

from clip.Predict import Predict_ORIGEN
from clip.Predict import Predict_serpent

class TestOrigenPrediction(unittest.TestCase):
    
            #since results are floats, test that we are very close to the expected value
    
    def test_ORIGEN_binned(self):
        
        prediction, uncertainty = Predict_ORIGEN("Example_ORIGEN_outputs/PWR_50MWd_test.out", "10.0 y", "PWR17x17", "binned", "isotope") 
        self.assertAlmostEqual(prediction, 1116070414300.2612, places=6)
        self.assertAlmostEqual(uncertainty, 21553290971.92218, places=6)
          
    def test_ORIGEN_isotope(self):
        
        prediction, uncertainty = Predict_ORIGEN("Example_ORIGEN_outputs/PWR_50MWd_test.out", "10.0 y", "PWR17x17", "isotope", "isotope")
        self.assertAlmostEqual(prediction, 1111343285500.0, places=6)
        self.assertAlmostEqual(uncertainty, 20019873852.011665, places=6)
       
    def test_ORIGEN_sampled(self):
        
        prediction, uncertainty = Predict_ORIGEN("Example_ORIGEN_outputs/PWR_50MWd_test.out", "10.0 y", "PWR17x17", "sampled", "isotope")
        self.assertAlmostEqual(prediction, 1115463249369.859, places=6)
        self.assertAlmostEqual(uncertainty, 4275563455.5758524, places=6)
        
        
class TestSerpentPrediction(unittest.TestCase):
        
    def test_serpent_binned(self):
    
        prediction, uncertainty = Predict_serpent("Example_Serpent_outputs/PWR_50MWd_10years_gamma.m", "PWR17x17", "spectrum", "binned", "none")
        self.assertAlmostEqual(prediction, 4954358.667392312, places=10)
        self.assertAlmostEqual(uncertainty, 101281.53687396941, places=10)
           
    def test_serpent_isotope(self):
        
        prediction, uncertainty = Predict_serpent("Example_Serpent_outputs/PWR_50MWd_10years.bumat", "PWR17x17", "isotope", "isotope", "isotope")
        self.assertAlmostEqual(prediction, 10442390.687943177, places=10)
        self.assertAlmostEqual(uncertainty, 183302.48865090107, places=10)
        
    def test_serpent_sampled(self):
        
        prediction, uncertainty = Predict_serpent("Example_Serpent_outputs/PWR_50MWd_10years_gamma.m", "PWR17x17", "spectrum", "sampled", "none")
        self.assertAlmostEqual(prediction, 5207255.815381419, places=10)
        self.assertAlmostEqual(uncertainty, 19038.932373043383, places=10)
    
    
if __name__ == '__main__':
    unittest.main()