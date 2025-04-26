import json
import numpy as np
import os
import math

class Shelf:
    def __init__(self,shelf=["object1","object2","object3"],shelf_id=1,shelf_sub_id=1,shelf_name="shelf1_1",shelf_path="./shelf_info_report"):
        self.shelf_set={""}
        self.shelf_set.update(shelf)
        self.shelf_set.remove("")
        self.shelf={"":0}
        i=0
        for object in shelf:
           i+=1
           temp={
               object:i
           }
           self.shelf.update(temp)
        self.shelf.pop("")
        self.max_order =i
        self.shelf_name=shelf_name
        self.shelf_id=shelf_id
        self.shelf_sub_id=shelf_sub_id
        self.shelf_path=shelf_path
        self.addproductcheck=0
        self.wrong_object_file_name=f"{self.shelf_path}/Wrong_object_in_{self.shelf_name}.json"
        self.soos_file_name=f"{self.shelf_path}/Semi_out_of_stock_report_in_{self.shelf_name}.json"
        self.oos_file_name=f"{self.shelf_path}/Out_of_stock_report_in_{self.shelf_name}.json"
        self.wrong_object_data=[]#contains wrong object in shelf
        self.soos_data=dict.fromkeys(shelf,0)#contain object that semi out of stock
        self.soos_data.update({"":0})
        self.oos_data=dict.fromkeys(shelf,0)
        self.oos_data.update({"":0})
        self.seen_data=dict.fromkeys(shelf,0)
        self.pre_state=False# to obtain the state if the robot is in range of shelf 1 or not
        self.state=False
        self.wrong_object_non_repeated_condition=False#condition for avoiding repeated data self.wrong_object_data
        self.write_data_to_json()
        pass


    def Load_shelf_information(self,id=1,sub_id=1,shelf=["object1","object2","object3"]):
        if id==self.shelf_id and sub_id==self.shelf_sub_id:
            self.shelf_set={""}
            self.shelf_set.update(shelf)
            self.shelf_set.remove("")
            self.shelf={"":0}
            i=0
            for object in shelf:
                i+=1
                temp={
                    object:i
                }
                self.shelf.update(temp)
            self.shelf.pop("")
            self.max_order =i
            self.soos_data=dict.fromkeys(shelf,0)#contain object that semi out of stock
            self.soos_data.update({"":0})
            self.oos_data=dict.fromkeys(shelf,0)
            self.oos_data.update({"":0})
            self.seen_data=dict.fromkeys(shelf,0)
            self.write_data_to_json()

    def ResetData(self,id=1,sub_id=1):
        if id==self.shelf_id and sub_id==self.shelf_sub_id:
            for object in self.shelf_set:
                self.soos_data[object]=0
            self.soos_data[""]=0
            for object in self.shelf_set:
                self.oos_data[object]=0
            self.oos_data[""]=0
            self.wrong_object_data=[]
            
    def shelf_object_comparision(self,id=1,object_dictionary_list=[{"object":'247',"coordinate":np.array([0,0,0,0])}]):
        if id==self.shelf_id:
            for dictionary in object_dictionary_list:
                if dictionary['object'] in self.shelf_set:

                    pass
                else:
                    if len(self.wrong_object_data)==0:

                        temp={'object':dictionary['object']}

                        self.wrong_object_data.append(temp)
                        print(f"label {temp['object']} not in {self.shelf_name}")
                        
                    
                    for dictionary2 in self.wrong_object_data:
                        if dictionary2['object']==dictionary['object']:
                            self.wrong_object_non_repeated_condition=False
                            break 
                        else:
                            self.wrong_object_non_repeated_condition=True

                    
                    if self.wrong_object_non_repeated_condition==True:
                        temp={'object':dictionary['object']}
                        self.wrong_object_data.append(temp)
                        print(f"label {temp['object']} not in {self.shelf_name}")

                    pass

            pass
        else:
            pass

    def semi_out_of_stock_checking(self,id=1,object_dictionary_list=[{"object":'247',"coordinate":np.array([0,0,0,0])}],stock_stage_dictionary_list=[{"stock stage":'semi-oos',"coordinate":np.array([0,0,0,0])}],threshold=0.5):
        if id==self.shelf_id:
            semi_out=[]
            if len(stock_stage_dictionary_list)==0:
                return
            else:
                for stock_stage in stock_stage_dictionary_list:
                    if stock_stage['stock stage']=='semi-oos':
                        semi_out.append(stock_stage)

            for semi in semi_out:
                self.soos_data[""]=1
                
                for object in object_dictionary_list:
                    if object['object'] not in self.shelf_set:
                        continue
                    else:
                        x1_1, y1_1, x2_1, y2_1 = object['coordinate']
                        x1_2, y1_2, x2_2, y2_2 = semi['coordinate']
                        

                        overlap_x1 = max(x1_1, x1_2)
                        overlap_y1 = max(y1_1, y1_2)
                        overlap_x2 = min(x2_1, x2_2)
                        overlap_y2 = min(y2_1, y2_2)

                        if overlap_x1 < overlap_x2 and overlap_y1 < overlap_y2:
                            overlap_area = (overlap_x2 - overlap_x1) * (overlap_y2 - overlap_y1)
                        else:
                            overlap_area=0.0
                        
                        object_area=(x2_1-x1_1)*(y2_1-y1_1)

                        overlap_object=overlap_area/object_area

                        if overlap_object>=threshold:
                            self.soos_data[object['object']]=1
                        
        else:
            pass


    def out_of_stock_checking(self,id=1,object_dictionary_list=[{"object":'247',"coordinate":np.array([0,0,0,0])}],stock_stage_dictionary_list=[{"stock stage":'semi-oos',"coordinate":np.array([0,0,0,0])}]):
        if id==self.shelf_id:
            out_stock=[]
            if len(stock_stage_dictionary_list)==0:
                return
            else:
                for stock_stage in stock_stage_dictionary_list:
                    if stock_stage['stock stage']=='oos':
                        out_stock.append(stock_stage)
            
            for out in out_stock:
                self.oos_data[""]=1
              
                x1,y1,x2,y2=out["coordinate"]
                x_center_oos=(x1+x2)/2
                y_center_oos=(y1+y2)/2



                left_product=[]
                right_product=[]

                for object in object_dictionary_list:
                    if object['object'] not in self.shelf_set:
                        continue
                    else:
                        pass
                    x1o,y1o,x2o,y2o=object['coordinate']
                    x_center_ob=(x1o+x2o)/2
                    y_center_ob=(y1o+y2o)/2


                    distance=np.sqrt((x_center_ob-x_center_oos)**2+(y_center_ob-y_center_oos)**2)

                    if x_center_ob<x_center_oos:
                        left_product.append([object['object'],x_center_ob,y_center_ob,distance])
                    if x_center_ob>x_center_oos:
                        right_product.append([object['object'],y_center_ob,y_center_oos,distance])

                closest_left_product=[]
                closest_right_product=[]

                if len(left_product)>0:
                    temp=[]
                    for product in left_product:
                        temp.append(product[3])
                    min_temp=min(temp)
                    min_index=temp.index(min_temp)    
                    closest_left_product.append(left_product[min_index])

                if len(right_product)>0:
                    temp=[]
                    for product in right_product:
                        temp.append(product[3])
                    min_temp=min(temp)
                    min_index=temp.index(min_temp)    
                    closest_right_product.append(right_product[min_index])

                if len(closest_left_product) == 0 and len(closest_right_product) == 0:
                    self.oos_data[""]=1
                
                elif len(closest_left_product) > 0 and len(closest_right_product) > 0:
                    if closest_left_product[0][0]==closest_right_product[0][0]:
                        self.oos_data[closest_left_product[0][0]]=1

                    else:
                        self.oos_data[closest_left_product[0][0]]=max(0.5,self.oos_data[closest_left_product[0][0]])
                        self.oos_data[closest_right_product[0][0]]=max(0.5,self.oos_data[closest_right_product[0][0]])

                    if self.shelf[closest_left_product[0][0]]== (self.shelf[closest_right_product[0][0]]-1):
                        continue
                    else:
                        
                        for i in range(1,self.max_order+1):
                            if i>self.shelf[closest_left_product[0][0]] and i<self.shelf[closest_right_product[0][0]] :
                                for label_set in self.shelf_set:
                                    if self.shelf[label_set]==i:
                                        self.oos_data[label_set]=1
                    
                elif len(closest_left_product) > 0:
                    if self.shelf[closest_left_product[0][0]]==self.max_order:
                        self.oos_data[closest_left_product[0][0]]=1
                    else:
                        self.oos_data[closest_left_product[0][0]]=max(0.5,self.oos_data[closest_left_product[0][0]])
                elif len(closest_right_product) >0:
                    if self.shelf[closest_right_product[0][0]]==1:
                        self.oos_data[closest_right_product[0][0]]=1
                    else:
                        self.oos_data[closest_right_product[0][0]]=max(0.5,self.oos_data[closest_right_product[0][0]])

            
        else:
            pass
    
    def seen_product_checking(self,id,object_dictionary_list=[{"object":'247',"coordinate":np.array([0,0,0,0])}]):
        if id==self.shelf_id:
            self.state=True
            for object in object_dictionary_list:
                if object['object'] in self.shelf_set:
                    self.seen_data[object['object']]=1

        else:
            self.state=False
        
        if self.state==False and self.pre_state==True:
            for object in self.shelf_set:
                if self.seen_data[object]==0:
                    self.soos_data[object]=1
        
        self.pre_state=self.state


    def write_data_to_json(self):
        with open(self.wrong_object_file_name,"w") as outfile:
            json.dump(self.wrong_object_data,outfile,indent=4)
        with open(self.soos_file_name,"w") as outfile:
            json.dump(self.soos_data,outfile,indent=4)
        with open(self.oos_file_name,"w") as outfile:
            json.dump(self.oos_data,outfile,indent=4)
        


class Shelf_Position:
    def __init__(self,shelf_id=1,x_below=0.0,x_above=0.0,y_below=0.0,y_above=0.0,theta_below=0.0,theta_above=0.0,shelf_path="./shelf_info_report",using_theta=True):
        self.shelf_id=shelf_id
        self.already_written=False
        self.x_below=x_below
        self.x_above=x_above
        self.y_below=y_below
        self.y_above=y_above
        self.theta_below=theta_below
        self.theta_above=theta_above
        self.theta_condition=False
        self.comparision_result=False
        self.using_theta=using_theta
        self.file_name=f"{shelf_path}/Shelf_{self.shelf_id}_position.json"
        pass

    def Load_shelf_position(self,id=1,below_coordinate=[0.0,0.0,0.0],above_coordinate=[0.0,0.0,0.0]):
        if id==self.shelf_id and self.already_written==False :
            self.x_below=below_coordinate[0]
            self.x_above=above_coordinate[0]
            self.y_below=below_coordinate[1]
            self.y_above=above_coordinate[1]
            self.theta_below=below_coordinate[2]
            self.theta_above=above_coordinate[2]
            self.already_written=True
            data={
                'From':[self.x_below,self.y_below,self.theta_below],
                'To':[self.x_above,self.y_above,self.theta_above]
            }
            with open(self.file_name,"w") as outfile:
                json.dump(data,outfile)

    def compare_robot_shelf_position(self,x,y,theta):
        if self.using_theta==True:
            self.compare_robot_theta(theta)
            if self.x_below<x<self.x_above and self.y_below<y<self.y_above and self.theta_condition==True:
                self.comparision_result=True
            else:
                self.comparision_result=False   
        else:
            if self.x_below<x<self.x_above and self.y_below<y<self.y_above:
                self.comparision_result=True
            else:
                self.comparision_result=False
        return self.comparision_result
        
    def compare_robot_theta(self,theta):
        theta_range=abs(self.theta_above-self.theta_below)
        if theta_range>=np.pi:
            if theta<0:
                    theta_in=2*np.pi+theta
            else:
                theta_in=theta    
            if self.theta_above>0 and self.theta_below<0:
                theta_below=2*np.pi+self.theta_below
                theta_above=self.theta_above
                if  theta_above<theta_in<theta_below:
                    self.theta_condition=True
                else:
                    self.theta_condition=False
            else:
                self.theta_condition=False            
        else:
            if  self.theta_below<theta<self.theta_above:
                self.theta_condition=True
            else:
                self.theta_condition=False

            


