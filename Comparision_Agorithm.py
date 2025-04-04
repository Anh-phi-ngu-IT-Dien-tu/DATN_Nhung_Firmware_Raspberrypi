import json
import numpy as np

class Shelf:
    def __init__(self,shelf=["object1","object2","object3"],shelf_id=1,shelf_name="shelf1_1"):
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
        self.shelf_name=shelf_name
        self.shelf_id=shelf_id
        self.wrong_object_file_name=f"Wrong_object_in_{self.shelf_name}.json"
        self.soos_file_name=f"Semi_out_of_stock_report_in_{self.shelf_name}.json"
        self.oos_file_name=f"Out_of_stock_report_in_{self.shelf_name}.json"
        self.wrong_object_data=[]#contains wrong object in shelf
        self.soos_data=dict.fromkeys(shelf,0)#contain object that semi out of stock
        self.soos_data.update({"":0})
        self.oos_data=dict.fromkeys(shelf,0)
        self.oos_data.update({"":0})
        self.wrong_object_non_repeated_condition=False#condition for avoiding repeated data self.wrong_object_data
        with open(self.wrong_object_file_name,"w") as outfile:
            json.dump(self.wrong_object_data,outfile)
        with open(self.soos_file_name,"w") as outfile:
            json.dump(self.soos_data,outfile,indent=4)
        with open(self.oos_file_name,"w") as outfile:
            json.dump(self.oos_data,outfile,indent=4)
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


    def out_of_stock_checking(self,id=1,object_dictionary_list=[{"object":'247',"coordinate":np.array([0,0,0,0])}],stock_stage_dictionary_list=[{"stock stage":'semi-oos',"coordinate":np.array([0,0,0,0])}],threshold=0.5):
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

                for object in object_dictionary_list:
                    if object['object'] not in self.shelf_set:
                        continue
                    else:
                        pass
                    x1o,y1o,x2o,y2o=object['coordinate']
                    x_center_ob=(x1o+x2o)/2
                    y_center_ob=(y1o+y2o)/2

            
        else:
            pass

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