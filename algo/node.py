class Node:
    def __init__(self, latitude, longitude):
        self.id = str(latitude) + '~' + str(longitude)
        self.latitude = latitude                   
        self.longitude = longitude              
        self.distanceFromStart = float('inf')       # g     
        self.estimatedDistanceToEnd = float('inf')  # f
        self.cameFrom = None  
        self.connnectedNodes = {}                       
       

       
    def addConnectedNodes(self, connnectedNodes):
        self.connnectedNodes = connnectedNodes


