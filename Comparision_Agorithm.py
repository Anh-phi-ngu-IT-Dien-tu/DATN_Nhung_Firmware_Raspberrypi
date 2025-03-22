import json



class Shelf:
    def __init__(self,Shelf={""}):
            self.Shelf=Shelf   
            pass

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