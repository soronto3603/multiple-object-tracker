import unittest
from tracker.tracker import Tracker
from tracker.Mask.mask import Mask

class TrackerTests(unittest.TestCase):
    def setUp(self):
        
        self.tracker=Tracker(json_src="./nascar_Extract/segment.json")

    def test_add_mask(self):
        """
            새로 들어온 멤버가 제일 앞으로 
            Stack
        """
        # get
        mask=Mask(x=10,y=10,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        mask2=Mask(x=20,y=20,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        # when
        mask_index=self.tracker.create_mask(mask)
        self.tracker.add_mask_at(mask2,mask_index)
        # then
        self.assertEqual(self.tracker.masks[mask_index][0],mask2)
    def test_create_mask(self):
        # get
        mask=Mask(x=10,y=10,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        # when
        mask_index=self.tracker.create_mask(mask)
        # then
        self.assertEqual(self.tracker.masks[mask_index][0],mask)

        # get
        mask1=Mask(x=10,y=10,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        # when
        mask_index=self.tracker.create_mask(mask1)
        # then
        self.assertEqual(self.tracker.masks[mask_index][0],mask1)
    
    def test_load_json(self):
        # get
        self.tracker=Tracker(json_src="./nascar_Extract/segment.json")
        # when
        json=self.tracker.json
        # then
        self.assertIsNotNone(json)
    
    def pick_mask(self):
        # get
        mask=Mask(x=10,y=10,width=10,height=10,src_image="./nascar_Extract/frame_0.jpg")
        # when
        mask_index=self.tracker.create_mask(mask)
        picked_mask=self.tracker.masks[0]
        # then
        self.assertNotEqual(type(picked_mask),type(list))

    def test_make_mask_from_json(self):
        # get
        tracker=Tracker(json_src="./optima/optima/infos.json")
        
        
        # when
        tracker.make_mask_from_json(sample)
        tracker.sort_masks()
        # then
        print("=======================두번째 세대 삽입")
        self.assertEqual(len(tracker.masks),len(sample['info']))

        
        tracker.make_mask_from_json(sample2)
        tracker.sort_masks()
        # then 
        self.assertEqual(len(tracker.masks),10)
    


if __name__=="__main__":
    unittest.main()