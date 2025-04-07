import cv2
import numpy as np
from Vision_Agorithm import Vision_Picture
from Comparision_Agorithm import Shelf


Shelf1_1=Shelf(['Heineken','TH true Milk'],1,"shelf1_1")

Test_pic=Vision_Picture("C:/Users/GIGABYTE/Desktop/DATN_Vision/DATN/images1/phai/Im_R_4.png",'stockv18.pt','oosv11.pt',0.7,0.6,"Test1","Test2")

Test_pic.Capture_frame()
Test_pic.Vision_Model()
Shelf1_1.shelf_object_comparision(1,Test_pic.object_label_dict)
Shelf1_1.semi_out_of_stock_checking(1,Test_pic.object_label_dict,Test_pic.stock_stage_label_dict,0.7)
Shelf1_1.out_of_stock_checking(1,Test_pic.object_label_dict,Test_pic.stock_stage_label_dict)

while True:
    Test_pic.show_result()
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()
cv2.imwrite(Test_pic.detection_window,Test_pic.outframe)
cv2.imwrite(Test_pic.oos_window,Test_pic.outframe2)

Shelf1_1.write_data_to_json()