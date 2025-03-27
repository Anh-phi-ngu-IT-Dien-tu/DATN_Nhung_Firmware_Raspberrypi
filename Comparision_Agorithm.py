import json



class Shelf:
    def __init__(self,shelf={"object1","object2","object3"},shelf_id=1,shelf_name="shelf1_1"):
        self.shelf=shelf
        self.shelf_name=shelf_name
        self.shelf_id=shelf_id
        self.file_name=f"Wrong_object_in_{self.shelf_name}.json"
        self.file_data=[]
        self.condition=False
        with open(self.file_name,"w") as outfile:
            json.dump(self.file_data,outfile)
        pass

    def shelf_object_comparision(self,id,label,x,y,theta):
        if id==self.shelf_id:
            if label in self.shelf:
                print(f"label {label} in shelf {self.shelf_name}")
                pass
            else:    
                if self.file_data==[]:
                    temp_dictionary={"object":label,
                                "x":x,
                                "y":y,
                                "theta":theta}
                    self.file_data.append(temp_dictionary)
                    return
                        
                for dictionary in self.file_data:
                    if dictionary["object"]==label:
                        self.condition=False
                        break
                    else:
                        self.condition=True
                if self.condition==True:
                    temp_dictionary={"object":label,
                                "x":x,
                                "y":y,
                                "theta":theta}
                    self.file_data.append(temp_dictionary)
        else:
            pass

    def write_data_to_json(self):
        with open(self.file_name,"w") as outfile:
            json.dump(self.file_data,outfile,indent=4)

    
    

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