class GPS:
    def __init__(self, location, speed, altitude):
        self.location = location
        self.speed = speed
        self.altitude = altitude
    
    def getPosition(self):
        return self.location
    
    def getSpeed(self):
        return self.speed
    
    def getAltitude(self):
        return self.altitude