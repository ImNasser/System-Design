import tkinter as tk
from tkinter import ttk
from tkinter import *
from GpsMap import Map
import Navigation
import DataSaver

from tkinter import *
 
 
class Table:
     
    def tableClickHandler(self,value):
        #widget = self.root.grid_slaves(row=r, column=c)[0]
        print(value)
    def __init__(self,root,total_rows,total_columns,data):
         
        self.root=root
        for i in range(total_rows):
            for j in range(total_columns):
                 
                 
                value=str(i+5)
                e = Entry(root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                e.grid(row=i+5, column=j)             
                e.insert(END, data[i][j])
                
                #print("Value:{0}".format(value))                
                e.bind("<Button-1>", lambda e=e:self.tableClickHandler(e))
                

                
                
 

class FrontEnd:
    def __init__(self):
        print("working")
        
        # self.menu = menu
        # self.mode = mode
        self.map = Map()
        self.dataSaver=DataSaver.DataSaver()
        self.vehicle = Navigation.Navigation(self.dataSaver)
        
        self.sourceEntry=None
        self.destinationEntry=None
        # #Map.__init__(self, self.map['location'], self.map['settings'])
        #Vehicle.__init__(self, self.vehicle['make'], self.vehicle['model'], self.vehicle['year'], self.vehicle['color'])
        self.root=None
        self.approvalButton=None
        self.approvalDone=False
        self.navLabel=None


    
        
    def temp_text(self,e):
        self.sourceEntry.delete(0,"end")
    
    def okayButtonHandler(self,e):
        print("Okay button clicked")
        source=self.sourceEntry.get()
        destination=self.destinationEntry.get()
        #save the source and destination in datasaver
        self.dataSaver.create("source",source)
        self.dataSaver.create("destination",destination)
        
        output=self.map.getGpsLocationFromAddress(destination)
        # lon=output.x
        # lat=output.y
        count=0
        for info in output:
         count=count+1
         #self.outputEntry.insert(tk.END,str(lat)+","+str(lon))
         name=info["name"]
         highway=info["highway"]
         maxSpeed=info["maxspeed"]
         #maxSpeed=0
         result="Name:{0} Highway:{1} MaxSpeed:{2} \n\n".format(name,highway,maxSpeed)
         self.dataSaver.create("name",name)
         self.dataSaver.create("highWay",highway)
         self.dataSaver.create("maxspeed",maxSpeed)
         self.dataSaver.saveDataFile()
         
         
         print("Output: {0}".format(info))
         if (count==5):
             break

        #self.outputEntry.insert(tk.END,result)
        #print("Output: lat:{0} lon:{1}".format(output))




        tableList=[]
        count=0
        item=("OsmID","Name","Highway","MaxSpeed")
        tableList.append(item)
        for info in output:
            #self.outputEntry.insert(tk.END,str(lat)+","+str(lon))
            name=info["name"]
            highway=info["highway"]
            maxSpeed=info["maxspeed"]
            #maxSpeed=0
            osmId=info["osmid"]
            result="Name:{0}, Highway:{1}, MaxSpeed:{2}".format(name,highway,maxSpeed)
            #print("Output: {0}".format(info))
            
            
            item=(osmId,name,highway,maxSpeed)
            tableList.append(item)

            count=count+1
            

     



        
        # find total number of rows and
        # columns in list
        total_rows = len(tableList)
        total_columns = len(tableList[0])
        
        # create root window
       
        t = Table(self.root,total_rows,total_columns,tableList)

        self.approvalButton["state"]=NORMAL
        










    def approveButtonHandler(self,e):
        print("Approving")
        source=self.sourceEntry.get()
        destination=self.destinationEntry.get()
        sourceID=self.map.getLatLonFromAddress(source)
        destID=self.map.getLatLonFromAddress(destination)
        self.map.findShortestRoute(sourceID,destID)
        print("DONE")
        self.approvalDone=True
        self.navLabel["bg"]="green"
        self.root.destroy()
        

    def createMapWindow(self):
        print("Set Map Destination")
        window=tk.Tk()
        window.title("Map Destination")
        window.geometry("950x700")
        self.root=window
                   
        menuLabel=Label(window,text="My Location",font=("Arial",20), anchor="e")
        #menuLabel.config(bg="black",fg="white")
        menuLabel.grid(row=0,column=0)

        self.sourceEntry=Entry(window,text="Source",font=("Arial",20))
        self.sourceEntry.grid(row=0,column=1)


        self.sourceEntry.insert(tk.END, "London Eye")
        #self.sourceEntry.config(state=DISABLED)
        #self.sourceEntry.grid()

        #self.sourceEntry.bind("<FocusIn>", self.temp_text)
        



        destLabel=Label(window,text="Destination",font=("Arial",20), anchor="e")
        #menuLabel.config(bg="black",fg="white")
        destLabel.grid(row=1,column=0)
        destinationEntry=Entry(window,text="Type address",font=("Arial",20))
        destinationEntry.insert(tk.END,"London Borough")
        self.destinationEntry=destinationEntry
        destinationEntry.grid(row=1,column=1)


        # self.outputEntry=tk.Text(window)
        # self.outputEntry.pack(pady=0)

        
        
        okayButton=Button(window,text="Find",font=("Arial",20))
        okayButton.grid(row=2,column=0,padx=0,pady=10)
        okayButton.bind("<Button-1>",self.okayButtonHandler)


        nearestLabel=Label(window,text="Nearest Streets",font=("Arial",20), anchor="e")
        #menuLabel.config(bg="black",fg="white")
        nearestLabel.grid(row=3,column=1,pady=10)


        approveButton=Button(window,text="Approve Route",font=("Arial",20))
        approveButton.grid(row=4,column=1,padx=0,pady=10)
        approveButton.bind("<Button-1>",self.approveButtonHandler)
        approveButton["state"]=DISABLED
        self.approvalButton=approveButton


        # #events
        # startFrame.bind("<Button-1>",self.setMapHandler)
        # navigationLabel.bind("<Button-1>",self.setMapHandler)





        window.mainloop()
    def getMap(self):
        return self
    
    def endJourney(self):
        print("Journey has ended.")
    
    def getVehicle(self):
        return self
    
    
    
    def createDiagWindow(self):
        print("Diagnostics windwos")
        window=tk.Tk()
        window.title("Diagnostics Window")
        window.geometry("950x700")
       # self.root=window
                   
        
        self.outputEntry=tk.Text(window)
        self.outputEntry.pack(pady=0)
        list=self.dataSaver.list
        print("List:{0}".format(list))
        for d in list:
            result=str(d["name"])+str(d["value"])+"\n"

            self.outputEntry.insert(tk.END,result)

        
        
        # okayButton=Button(window,text="Find",font=("Arial",20))
        # okayButton.grid(row=2,column=0,padx=0,pady=10)
        # okayButton.bind("<Button-1>",self.okayButtonHandler)


        
        # #events
        # startFrame.bind("<Button-1>",self.setMapHandler)
        # navigationLabel.bind("<Button-1>",self.setMapHandler)





        window.mainloop()
    def setMapHandler(self,e):
        print("Mouse button clicked")
        #self.map.showMap()
        self.createMapWindow()

    def setDriveHandler(self,e):
        print("Mouse button clicked")
        #self.map.showMap()
        self.vehicle.move(0)
    def setDiagHandler(self,e):

        self.dataSaver.saveDataFile()
        self.dataSaver.retrieveDataFile()
        self.createDiagWindow()




    def showMainMenu(self):
        print("Main menu is being displayed.")
        window=tk.Tk()
        window.title("Main Menu")
        window.geometry("750x450")

        startFrame=Frame(window,highlightbackground="black",highlightthickness=2,bd=0)
        driveFrame=Frame(window,highlightbackground="black",highlightthickness=2,bd=0)
        diagnosticsFrame=Frame(window,highlightbackground="black",highlightthickness=2,bd=0)



            
        menuLabel=Label(window,text="Welcome to Autonomous Vehicle Menu",font=("Arial",20), anchor="e")
        menuLabel.config(bg="black",fg="white")
        menuLabel.pack(pady=20)

        navigationLabel=Label(startFrame,text="Set Map Destination",font=("Arial",20), anchor="e")
        navigationLabel.pack(pady=20)
        self.navLabel=startFrame

        
        
        driveLabel=Label(driveFrame,text="Start Driving Autonomous Vehicle",font=("Arial",20))
        driveLabel.pack(pady=20)
        
        
        diagLabel=Label(diagnosticsFrame,text="Show Diagnostics",font=("Arial",20))
        diagLabel.pack(pady=20)
        
        
        startFrame.pack()
        driveFrame.pack(pady=20)
        diagnosticsFrame.pack(pady=0)
        
        startFrame.pack_propagate(False)
        driveFrame.pack_propagate(False)
        diagnosticsFrame.pack_propagate(False)

        startFrame.config(width=490, height=80)
        driveFrame.config(width=490, height=80)
        diagnosticsFrame.config(width=490, height=80)

        

        #events
        startFrame.bind("<Button-1>",self.setMapHandler)
        navigationLabel.bind("<Button-1>",self.setMapHandler)

        driveLabel.bind("<Button-1>",self.setDriveHandler)
        driveFrame.bind("<Button-1>",self.setDriveHandler)

        diagLabel.bind("<Button-1>",self.setDiagHandler)
        diagnosticsFrame.bind("<Button-1>",self.setDiagHandler)





        window.mainloop()
        #window.wait_window(window)


if __name__=="__main__":
 gui=FrontEnd()
 gui.showMainMenu()
