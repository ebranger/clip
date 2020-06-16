
import unittest

from clip.Clip import *

class TestClipOrigenPrediction(unittest.TestCase):
    
            #since results are floats, test that we are very close to the expected value
    
    def test_Clip_ORIGEN_binned(self):
    
        predictor = Clip("Data")
        predictor.set_prediction_parameters("PWR17x17", "binned", "isotope", "ORIGEN", "10.0 y")
        prediction, uncertainty = predictor.predict("Example_ORIGEN_outputs/PWR_50MWd_test.out") 
        self.assertAlmostEqual(prediction, 1116070414300.2612, places=6)
        self.assertAlmostEqual(uncertainty, 21553290971.92218, places=6)
          
    def test_Clip_ORIGEN_isotope(self):
        
        predictor = Clip("Data")
        predictor.set_prediction_parameters("PWR17x17", "isotope", "isotope", "ORIGEN", "10.0 y")
        prediction, uncertainty = predictor.predict("Example_ORIGEN_outputs/PWR_50MWd_test.out") 
        self.assertAlmostEqual(prediction, 1111343285500.0, places=6)
        self.assertAlmostEqual(uncertainty, 20019873852.011665, places=6)
       
    def test_Clip_ORIGEN_sampled(self):
        
        predictor = Clip("Data")
        predictor.set_prediction_parameters("PWR17x17", "sampled", "isotope", "ORIGEN", "10.0 y")
        prediction, uncertainty = predictor.predict("Example_ORIGEN_outputs/PWR_50MWd_test.out") 
        self.assertAlmostEqual(prediction, 1115463249369.859, places=6)
        self.assertAlmostEqual(uncertainty, 4275563455.5758524, places=6)
        
        
class TestClipSerpentPrediction(unittest.TestCase):
        
    def test_Clip_serpent_binned(self):
        
        predictor = Clip("Data")
        predictor.set_prediction_parameters("PWR17x17", "binned", "none", "Serpent_gamma")
        prediction, uncertainty = predictor.predict("Example_Serpent_outputs/PWR_50MWd_10years_gamma.m") 
        self.assertAlmostEqual(prediction, 4954358.667392312, places=10)
        self.assertAlmostEqual(uncertainty, 101281.53687396941, places=10)
           
    def test_Clip_serpent_isotope(self):
        
        predictor = Clip("Data")
        predictor.set_prediction_parameters("PWR17x17", "isotope", "isotope", "Serpent_bumat")
        prediction, uncertainty = predictor.predict("Example_Serpent_outputs/PWR_50MWd_10years.bumat") 
        self.assertAlmostEqual(prediction, 10442390.687943177, places=10)
        self.assertAlmostEqual(uncertainty, 183302.48865090107, places=10)
        
    def test_Clip_serpent_sampled(self):
        
        predictor = Clip("Data")
        predictor.set_prediction_parameters("PWR17x17", "sampled", "none", "Serpent_gamma")
        prediction, uncertainty = predictor.predict("Example_Serpent_outputs/PWR_50MWd_10years_gamma.m") 
        self.assertAlmostEqual(prediction, 5207255.815381419, places=10)
        self.assertAlmostEqual(uncertainty, 19038.932373043383, places=10)
    
    
if __name__ == '__main__':
    unittest.main()