import json
import numpy as np


class Shelf:
    def __init__(self,shelf=["object1","object2","object3"],shelf_id=1,shelf_name="shelf1_1"):
        self.shelf=[]
        i=0
        for object in shelf:
           i+=1
           temp={
               "object":object,
               "order":i
           }
           self.shelf.append(temp)

        self.shelf_name=shelf_name
        self.shelf_id=shelf_id
        self.file_name=f"Wrong_object_in_{self.shelf_name}.json"
        self.oos_file_name=f"Semi_out_of_stock_report_in_{self.shelf_name}.json"
        self.file_data=[]#contains wrong object in shelf
        self.oos_file_data=[]#contain object that semi out of stock
        self.condition=False#condition for avoiding repeated data self.file_data
        self.semi_condition=False#condition for avoiding out of stock label
        self.oos_condition=False#condition for avoiding repeated data self.oos_file_data
        self.debug_file=f"Debug_{self.shelf_name}.json"
        self.debug_data=[]
        with open(self.file_name,"w") as outfile:
            json.dump(self.file_data,outfile)
        with open(self.oos_file_name,"w") as outfile:
            json.dump(self.oos_file_data,outfile)
        with open(self.debug_file,"w") as outfile:
            json.dump(self.debug_file,outfile)

    def shelf_object_comparision(self,id,label):
        if id==self.shelf_id:

            for dictionary in self.shelf:
                if label ==dictionary['object']:
                    # print(f"label {label} in shelf {self.shelf_name}")
                    pass
                else:    
                    if len(self.file_data)==0:
                        temp_dictionary={'object':label
                                        }
                        self.file_data.append(temp_dictionary)
                        print(f"label {temp_dictionary['object']} not in {self.shelf_name}")
                        return
                            
                    for dictionary in self.file_data:
                        if dictionary['object']==label:
                            self.condition=False
                            break
                        else:
                            self.condition=True
                    if self.condition==True:
                        temp_dictionary={'object':label
                                        }
                        self.file_data.append(temp_dictionary)
                        print(f"label {temp_dictionary['object']} not in {self.shelf_name}")
        else:
            pass
    #x1,y1,x2,y2
    def semi_out_of_stock_object(self,id,label,object_coordinate,soos_label,soos_coordinate,threshold=0.5):
        if id==self.shelf_id:

            if soos_label=='semi-oos':
                for dictionary in self.file_data:
                    if dictionary['object']==label:
                        self.semi_condition=False
                        break
                    else:
                        self.semi_condition=True
                        
                
                if self.semi_condition==True:
                    
                    x1_1, y1_1, x2_1, y2_1 = object_coordinate
                    x1_2, y1_2, x2_2, y2_2 = soos_coordinate

                    # Calculate overlap area
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

                    temp_data={
                        "over_lap":overlap_area,
                        "ooverlap/object":overlap_object
                    }
                    self.debug_data.append(temp_data)
                    if overlap_object>=threshold:
                        if len(self.oos_file_data)==0:
                            temp={
                                'object':label
                            }
                            self.oos_file_data.append(temp)
                            print(f"object {temp['object']} is semi out of stock at shelf {self.shelf_name}")
                            return

                        for dictionary in self.oos_file_data:
                            if dictionary['object']==label:
                                self.oos_condition=False
                                break
                            else:
                                self.oos_condition=True
                        if self.oos_condition==True:
                            temp={
                                'object':label
                            }
                            self.oos_file_data.append(temp)
                            print(f"object {temp['object']} is semi out of stock at shelf {self.shelf_name}")

                    else:
                        if len(self.oos_file_data)==0:
                            temp={
                                'object':"emty semi out of stock"
                            }
                            self.oos_file_data.append(temp)
                            print(f"object {temp['object']} is semi out of stock at shelf {self.shelf_name}")
                            return
                        

                        for dictionary in self.oos_file_data:
                            if dictionary['object']=="emty semi out of stock":
                                self.oos_condition=False
                                break
                            else:
                                self.oos_condition=True
                        if self.oos_condition==True:
                            temp={
                                'object':"emty semi out of stock"
                            }
                            self.oos_file_data.append(temp)
                            print(f"object {temp['object']} is semi out of stock at shelf {self.shelf_name}")

                        pass
                pass

            pass
        
        else:
            pass


    def out_of_stock_object(self,id,label,object_coordinate,soos_label,soos_coordinate,threshold=2):
        if id==self.shelf_id:

            if soos_label=='oos':    
                print(f"{self.shelf_name} has been out of stock")

            pass
        else :
            pass

    def write_data_to_json(self):
        with open(self.file_name,"w") as outfile:
            json.dump(self.file_data,outfile,indent=4)
        with open(self.oos_file_name,"w") as outfile:
            json.dump(self.oos_file_data,outfile,indent=4)
        with open(self.debug_file,"w") as outfile:
            json.dump(self.debug_data,outfile,indent=4)
    

""""""""""""""""""

class Shelf_ver2:
    def __init__(self,shelf=["object1","object2","object3"],shelf_id=1,shelf_name="shelf1_1"):
        self.shelf_set={""}
        self.shelf_set.update(shelf)
        self.shelf_set.remove("")
        self.shelf=[]
        i=0
        for object in shelf:
           i+=1
           temp={
               "object":object,
               "order":i
           }
           self.shelf.append(temp)
        self.shelf_name=shelf_name
        self.shelf_id=shelf_id
        self.wrong_object_file_name=f"Wrong_object_in_{self.shelf_name}.json"
        self.soos_file_name=f"Semi_out_of_stock_report_in_{self.shelf_name}.json"
        self.wrong_object_data=[]#contains wrong object in shelf
        self.soos_data=dict.fromkeys(shelf,0)#contain object that semi out of stock
        self.wrong_object_non_repeated_condition=False#condition for avoiding repeated data self.wrong_object_data



        with open(self.wrong_object_file_name,"w") as outfile:
            json.dump(self.wrong_object_data,outfile)
        with open(self.soos_file_name,"w") as outfile:
            json.dump(self.soos_data,outfile)

        pass


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
                        return
                    
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
        semi_out=[]
        if len(stock_stage_dictionary_list)==0:
            return
        else:
            for stock_stage in stock_stage_dictionary_list:
                if stock_stage['stock stage']=='semi-oos':
                    semi_out.append(stock_stage)

        for semi in semi_out:
            if len(object_dictionary_list)==0:
                self.soos_data[""]=0
                return
            
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


    def write_data_to_json(self):
        with open(self.wrong_object_file_name,"w") as outfile:
            json.dump(self.wrong_object_data,outfile,indent=4)
        with open(self.soos_file_name,"w") as outfile:
            json.dump(self.soos_data,outfile,indent=4)


class Shelf_Position:
    def __init__(self,x_below=0.0,x_above=0.0,y_below=0.0,y_above=0.0,theta_below=0.0,theta_above=0.0):
        self.x_below=x_below
        self.x_above=x_above
        self.y_below=y_below
        self.y_above=y_above
        self.theta_below=theta_below
        self.theta_above=theta_above
        self.comparision_result=False
        pass

    def compare_robot_shelf_position(self,x,y,theta):
        if self.x_below<=x<=self.x_above and self.y_below<=y<=self.y_above and self.theta_below<=theta<=self.theta_above:
            self.comparision_result=True
        else:
            self.comparision_result=False
        return self.comparision_result