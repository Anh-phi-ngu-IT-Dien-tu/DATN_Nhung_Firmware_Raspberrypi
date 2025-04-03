import cv2
import numpy as np
from Vision_Agorithm import Vision_Picture
from Comparision_Agorithm import Shelf_ver2




Shelf1_1=Shelf_ver2(['Pepsi-den', 'Pepsi-xanh', 'Redbull', 'Simply', 'Tea Plus'],1,"shelf1_1")

Test_pic=Vision_Picture('path.jpg','stockv17.pt','oosv8_20.3pt',0.6,0.5,"Test detection","Test out of stock")

Test_pic.Capture_frame()
Test_pic.Vision_Model()
Shelf1_1.shelf_object_comparision(1,Test_pic.object_label_dict)
Shelf1_1.semi_out_of_stock_checking(1,Test_pic.object_label_dict,Test_pic.stock_stage_label_dict,0.7)

while True:
    Test_pic.show_result()
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()
cv2.imwrite(Test_pic.detection_window,Test_pic.outframe)
cv2.imwrite(Test_pic.oos_window,Test_pic.outframe2)

Shelf1_1.write_data_to_json