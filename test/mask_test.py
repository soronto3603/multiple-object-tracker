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
        dist=mask_a.get_distance_with(mask_b)
        # then
        self.assertEqual(dist,4)
        self.assertNotEqual(Mask(x=12,y=25).get_distance_with(mask_b),4)

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
        self.assertEqual(Mask(width=10,height=20).get_difference_size_with(Mask(width=30,height=50)),1300)
        self.assertEqual(Mask(width=10,height=20).get_difference_size_with(Mask(width=10,height=20)),0)
        self.assertEqual(Mask(width=10,height=20).get_difference_size_with(Mask(width=22.2,height=5.5)),77.9)

    def test_load_image(self):
        # get
        mask1=Mask(x=10,y=10,width=100,height=100,src_image="./nascar_Extract/frame_0.jpg")
        # when
        # then
        self.assertIsNotNone(mask1.croped_img)

    def test_get_similarity_with(self):
        # get
        mask1=Mask(x=10,y=10,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        mask2=Mask(x=20,y=20,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        # when
        result=mask1.get_similarity_with(mask2)
        # then
        self.assertIsNotNone(result)
        self.assertIn(type(result),[type(1.),type(1)])

    def test_get_histogram_with(self):
        #get
        mask1=Mask(x=10,y=10,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        mask2=Mask(x=20,y=20,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        #when
        result=mask1.get_histogram_with(mask2)
        #then
        self.assertIsNotNone(result)

        #get
        mask3=Mask(x=100,y=100,width=100,height=100,src_image="./nascar_Extract/frame_0.jpg")
        mask4=Mask(x=100,y=100,width=100,height=100,src_image="./nascar_Extract/frame_0.jpg")
        #when
        result2=mask3.get_histogram_with(mask4)
        print(result2)
        #then
        self.assertIsNotNone(result2)
    
    def test_exist_label(self):
        # get
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        # when
        # then
        self.assertEqual(mask1.label,"car")
    
    def test_get_there_not_equal(self):
        # 라벨이 다른 경우 == True
        # get
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        mask2=Mask(x=10,y=10,width=10,height=10,label="umbrella",src_image="./nascar_Extract/frame_0.jpg")
        # when
        n_e=mask1.there_not_equal(mask2)
        # then
        self.assertEqual(n_e,True)

        # 라벨이 같은 경우 == False
        # get
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        mask2=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        # when
        n_e=mask1.there_not_equal(mask2)
        # then
        self.assertEqual(n_e,False)

        # 거리가 먼 경우 == True
        # get
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        mask2=Mask(x=200,y=200,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        # when
        n_e=mask1.there_not_equal(mask2)
        # then
        self.assertEqual(n_e,True)
    
    def test_random_color(self):
        # get
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")

        # when

        # then
        self.assertIsNotNone(mask1.color)
    
    def test_get_image_size(self):
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        
        self.assertIsNotNone(mask1.src_image_width)
        self.assertIsNotNone(mask1.src_image_height)
        print(mask1.src_image_width,mask1.src_image_height, "test_get_image_size .. OK")
    
    def test_get_angle(self):
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")

        self.assertIsNotNone(mask1.angle)
        print(mask1.angle, "test_get_angle .. OK")
    
    def test_get_distance_from_camera_with(self):
        mask1=Mask(x=10,y=10,width=10,height=10,label="car",src_image="./nascar_Extract/frame_0.jpg")
        # mask1.get_distance_from_camera_with()

if __name__=="__main__":
    unittest.main()