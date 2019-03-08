import unittest
from tracker.Mask.config import Config

# get
# when
# then

class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.Config=Config()

    def test_config_property(self):
        self.assertIsNotNone(self.Config.DISTANCE)
        self.assertIsNotNone(self.Config.HISTOGRAM)
        self.assertIsNotNone(self.Config.SIZE)

    def test_set_config(self):
        self.Config.set_config([600,6000,600])
        self.assertEqual(self.Config.DISTANCE,600)
        self.assertEqual(self.Config.HISTOGRAM,6000)
        self.assertEqual(self.Config.SIZE,600)
    
        
if __name__=="__main__":
    unittest.main()