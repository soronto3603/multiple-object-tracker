import unittest
from tracker.tracker import Tracker
from tracker.Mask.mask import Mask

class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.DEFAULT_PATH="./optima/optima2"
        self.JSON_NAME="infos.json"
        self.tracker=Tracker(default_path=self.DEFAULT_PATH,json_name=self.JSON_NAME)

    def test_set_path(self):
        tracker=Tracker(default_path=self.DEFAULT_PATH,json_name=self.JSON_NAME)

    def test_add_mask(self):
        """
            새로 들어온 멤버가 제일 앞으로 
            Stack
        """
        # get
        mask=Mask(x=10,y=10,width=10,height=10,src_image="./optima/optima2/optima_frame60.jpg")
        mask2=Mask(x=20,y=20,width=10,height=10,src_image="./optima/optima2/optima_frame60.jpg")
        # when
        mask_index=self.tracker.create_mask(mask)
        self.tracker.add_mask_at(mask2,mask_index)
        # then
        self.assertEqual(self.tracker.masks[mask_index][0],mask2)
    def test_create_mask(self):
        # get
        mask=Mask(x=10,y=10,width=10,height=10,src_image="./optima/optima2/optima_frame60.jpg")
        # when
        mask_index=self.tracker.create_mask(mask)
        # then
        self.assertEqual(self.tracker.masks[mask_index][0],mask)

        # get
        mask1=Mask(x=10,y=10,width=10,height=10,src_image="./optima/optima2/optima_frame60.jpg")
        # when
        mask_index=self.tracker.create_mask(mask1)
        # then
        self.assertEqual(self.tracker.masks[mask_index][0],mask1)
    
    def test_load_json(self):
        # get
        self.tracker=Tracker(default_path=self.DEFAULT_PATH,json_name=self.JSON_NAME)
        # when
        json=self.tracker.json
        # then
        self.assertIsNotNone(json)
    
    def pick_mask(self):
        # get
        mask=Mask(x=10,y=10,width=10,height=10,src_image="./optima/optima2/optima_frame60.jpg")
        # when
        mask_index=self.tracker.create_mask(mask)
        picked_mask=self.tracker.masks[0]
        # then
        self.assertNotEqual(type(picked_mask),type(list))

    def test_make_mask_from_json(self):
        # get
        tracker=Tracker(default_path=self.DEFAULT_PATH,json_name=self.JSON_NAME)
        
        sample=[{"box": [352, 863, 391, 920], "label": "car", "polygons": [[[914.0, 389.5], [913.0, 389.5], [912.0, 389.5], [911.0, 389.5], [910.5, 389.0], [910.0, 388.5], [909.0, 388.5], [908.0, 388.5], [907.0, 388.5], [906.0, 388.5], [905.0, 388.5], [904.0, 388.5], [903.0, 388.5], [902.0, 388.5], [901.0, 388.5], [900.0, 388.5], [899.0, 388.5], [898.0, 388.5], [897.0, 388.5], [896.0, 388.5], [895.0, 388.5], [894.0, 388.5], [893.0, 388.5], [892.0, 388.5], [891.0, 388.5], [890.0, 388.5], [889.0, 388.5], [888.0, 388.5], [887.0, 388.5], [886.0, 388.5], [885.0, 388.5], [884.5, 388.0], [884.0, 387.5], [883.0, 387.5], [882.0, 387.5], [881.0, 387.5], [880.0, 387.5], [879.0, 387.5], [878.0, 387.5], [877.0, 387.5], [876.0, 387.5], [875.0, 387.5], [874.0, 387.5], [873.0, 387.5], [872.0, 387.5], [871.0, 387.5], [870.0, 387.5], [869.0, 387.5], [868.0, 387.5], [867.5, 387.0], [867.0, 386.5], [866.5, 386.0], [866.0, 385.5], [865.5, 385.0], [865.5, 384.0], [865.5, 383.0], [865.5, 382.0], [865.5, 381.0], [865.5, 380.0], [865.5, 379.0], [865.5, 378.0], [865.5, 377.0], [865.5, 376.0], [865.5, 375.0], [865.5, 374.0], [865.5, 373.0], [866.0, 372.5], [866.5, 372.0], [866.5, 371.0], [866.5, 370.0], [866.5, 369.0], [866.5, 368.0], [866.5, 367.0], [866.5, 366.0], [866.5, 365.0], [866.5, 364.0], [866.5, 363.0], [867.0, 362.5], [867.5, 362.0], [868.0, 361.5], [868.5, 361.0], [868.5, 360.0], [869.0, 359.5], [869.5, 359.0], [870.0, 358.5], [870.5, 358.0], [871.0, 357.5], [871.5, 357.0], [872.0, 356.5], [872.5, 356.0], [873.0, 355.5], [873.5, 355.0], [874.0, 354.5], [874.5, 354.0], [875.0, 353.5], [875.5, 353.0], [876.0, 352.5], [877.0, 352.5], [878.0, 352.5], [879.0, 352.5], [880.0, 352.5], [881.0, 352.5], [882.0, 352.5], [883.0, 352.5], [884.0, 352.5], [885.0, 352.5], [886.0, 352.5], [887.0, 352.5], [888.0, 352.5], [889.0, 352.5], [890.0, 352.5], [891.0, 352.5], [892.0, 352.5], [893.0, 352.5], [894.0, 352.5], [895.0, 352.5], [896.0, 352.5], [897.0, 352.5], [898.0, 352.5], [898.5, 353.0], [899.0, 353.5], [900.0, 353.5], [901.0, 353.5], [902.0, 353.5], [903.0, 353.5], [904.0, 353.5], [904.5, 354.0], [905.0, 354.5], [905.5, 355.0], [906.0, 355.5], [907.0, 355.5], [908.0, 355.5], [908.5, 356.0], [909.0, 356.5], [909.5, 357.0], [910.0, 357.5], [910.5, 358.0], [911.0, 358.5], [912.0, 358.5], [912.5, 359.0], [913.0, 359.5], [913.5, 360.0], [913.5, 361.0], [914.0, 361.5], [914.5, 362.0], [915.0, 362.5], [915.5, 363.0], [916.0, 363.5], [916.5, 364.0], [916.5, 365.0], [917.0, 365.5], [917.5, 366.0], [917.5, 367.0], [917.5, 368.0], [918.0, 368.5], [918.5, 369.0], [918.5, 370.0], [918.5, 371.0], [918.5, 372.0], [918.5, 373.0], [918.5, 374.0], [918.5, 375.0], [918.5, 376.0], [918.5, 377.0], [918.5, 378.0], [918.5, 379.0], [918.5, 380.0], [918.5, 381.0], [918.5, 382.0], [918.5, 383.0], [918.5, 384.0], [918.5, 385.0], [918.0, 385.5], [917.5, 386.0], [917.5, 387.0], [917.0, 387.5], [916.5, 388.0], [916.0, 388.5], [915.0, 388.5], [914.5, 389.0], [914.0, 389.5]]]}]
        # when
        tracker.make_mask_from_json(sample)

        # then 
        self.assertEqual(len(tracker.masks),10)
    


if __name__=="__main__":
    unittest.main()