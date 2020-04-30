
import unittest

from clip.rescale import *

class TestSerpentResultsRescale(unittest.TestCase):

    def test_rescale(self):
        
        scale = scale_serpent_to_origen(1)
        self.assertAlmostEqual(scale, 109160.771985, places = 4)
          
    
if __name__ == '__main__':
    unittest.main()