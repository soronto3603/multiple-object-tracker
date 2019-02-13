import unittest
from tracker.Mask.mask import Mask

# get
# when
# then

class MaskTests(unittest.TestCase):
    def setUp(self):
        self.mask=Mask()

    def test_set_up(self):
        Mask()

    def test_disactivation(self):
        # get
        mask=Mask()
        # when
        mask.disactivation()
        # then
        self.assertEqual(mask.activation,-1)
    
    def test_increase_activation(self):
        # get
        mask=Mask()
        mask_activation=mask.activation
        # when
        mask.increase_activation()
        # then
        self.assertEqual(mask.activation,mask_activation+1)  
    
    def test_get_distance_both_two_mask(self):
        # get
        mask_a=Mask(x=10,y=20)
        mask_b=Mask(x=10,y=24)
        # when
        dist=mask_a.get_distance_to(mask_b)
        # then
        self.assertEqual(dist,4)
        self.assertNotEqual(Mask(x=12,y=25).get_distance_to(mask_b),4)

    def test_compare_float(self):
        # get
        # when
        # then
        self.assertEqual(self.mask.isclose(0.008,0.007),False)
        self.assertEqual(self.mask.isclose(0.00008,0.00007),False)
        self.assertEqual(self.mask.isclose(0.0000008,0.0000007),False)
        self.assertEqual(self.mask.isclose(0.000000008,0.000000008),True)

    def test_get_size_both_two_mask(self):
        # get
        # when
        # then
        self.assertEqual(Mask(width=10,height=20).get_difference_size_to(Mask(width=30,height=50)),1300)
        self.assertEqual(Mask(width=10,height=20).get_difference_size_to(Mask(width=22.2,height=5.5)),77.9)

    def test_load_image(self):
        self.assertIsNotNone(Mask().load_image("./nascar_Extract/frame_0.jpg"))
        self.assertIsNone(Mask().load_image("./nascar_Extract/frame_0.jp123g"))
        self.assertIsNone(Mask().load_image("/frame_0.jp123g"))
        self.assertIsNone(Mask().load_image("/nascar_Extract/frame_0.jp123g"))
        self.assertIsNone(Mask().load_image("abcd"))

    def test_load_polygon_data(self):
        

if __name__=="__main__":
    unittest.main()