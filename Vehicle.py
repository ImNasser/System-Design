class Vehicle(Vision, Navigation, GPS, DataSaver):
    def __init__(self, name):
        self.name = name
        self.navigation = Navigation()
        self.vision = Vision()
        self.gps = GPS()
        self.mode = None
        self.state = None
        DataSaver.__init__(self)
    
    def startVehicle(self):
        print("Starting the vehicle...")
    
    def stopVehicle(self):
        print("Stopping the vehicle...")
    
    def performSafetyChecks(self):
        print("Performing safety checks...")
    
    def selectDrivingMode(self, mode):
        self.mode = mode
    
    def startMoving(self):
        print("Starting to move...")
    
    def performMovingChecks(self):
        print("Performing moving checks...")
    
    def getVehicleState(self):
        return self.state