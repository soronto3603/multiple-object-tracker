import unittest
from tracker.tracker import Tracker

class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tracker=Tracker()
    def test_set_up(self):
        Tracker()
    
    
if __name__=="__main__":
    unittest.main()