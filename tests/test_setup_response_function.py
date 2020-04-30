
import unittest

from clip.setup_response_function import *

class TestSetupResponeFunction(unittest.TestCase):
    
            #since results are floats, test that we are very close to the expected value
    
    def test_setup_respone_function(self):
        
        #Convert a linear function to a binned avearage.
        #the part from 0.1 to 0.2 is outside the 
        sampled_energies = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]
        sampled_response = [0, 1, 2, 3, 4, 5]
        bin_edges = [0.2, 0.4, 0.5, 0.7]
        
        binned_response = get_binned_response_function(sampled_energies, sampled_response, bin_edges)
        
        self.assertAlmostEqual(binned_response[0], 2, places = 10)      #larger bin
        self.assertAlmostEqual(binned_response[1], 3.5, places = 10)    #smaller bin
        self.assertAlmostEqual(binned_response[2], 4.5, places = 10)    #smaller bin, and not sampled to the highest edge.
    
if __name__ == '__main__':
    unittest.main()