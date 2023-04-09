import pickle
import copy
class DataSaver:
    def __init__(self):
       
        self.list=[]
        self.data2={'name':0,"value":0}
        self.data2['name']=1
        self.data2['value']=2
        self.retrieveDataFile()
        
        
    
    def getPosition(self):
        return self.location
    
    def getSpeed(self):
        return self.speed
    
    def getAltitude(self):
        return self.altitude
    def create(self,name,value):
        self.data2['name']=name
        self.data2['value']=value
        d=copy.deepcopy(self.data2)
        self.list.append(d)
    def saveDataFile(self):
        with open('diag.pkl', 'wb') as f:
         pickle.dump(self.data2, f)
    def retrieveDataFile(self):
        with open('diag.pkl', 'rb') as f:
         try:
          self.data2=pickle.load(f)
         except Exception as ep:
            print(ep)

        

    
    