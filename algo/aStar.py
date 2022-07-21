import json
import time
from algo.haversine import calculateHaversineDistance, Unit
from algo.node import Node
from algo.minheap import MinHeap
from pprint import pprint


def aStarAlgorithm(point1, point2):
    
    # timer start
    start_time = time.time()
  
    # unpack latitude/longitude
    startLat, startLng = point1
    endLat, endLng = point2
    
    #  need to organized first the data here 
    nodes = initializeNodes()
    
      
    # get start node and end node
    startNodeCoordinate = transformLatLngToId(startLat, startLng)
    endNodeCoordinate = transformLatLngToId(endLat, endLng) 
    startNode = nodes[startNodeCoordinate]
    endNode = nodes[endNodeCoordinate]
  
    
    # weight from start is always zero
    startNode.distanceFromStart = 0
    startNode.estimatedDistanceToEnd = calculateHaversineDistance(point1, point2, unit=Unit.METERS)
    
    # Min heap Data structure store all nodes to be process
    # and it arranges all the nodes by its f score in non
    # decreasing order.
    nodesToVisit = MinHeap([startNode])
   

    # if our minheap is not yet empty, meaning
    # there are nodes in the queue to be process.
    while not nodesToVisit.isEmpty():
        

        # Remove the node in the min heap with smallest f score
        # currentMinDistance store the current
        # node to  be computed.
        currentMinDistanceNode = nodesToVisit.remove()

        # we reach the destination meaning there is a path
        # from point a to point b.
        if currentMinDistanceNode.id == endNode.id:
            break
        
        # get all connected node
        neighbors = getNeighboringNodes(currentMinDistanceNode, nodes)
       
       
        for neighbor in neighbors:
                            
            currentPoint = (currentMinDistanceNode.latitude, currentMinDistanceNode.longitude)
            neighborPoint = (neighbor.latitude, neighbor.longitude)


            tentativeDistanceToNeighbor = currentMinDistanceNode.distanceFromStart +  calculateHaversineDistance(currentPoint, neighborPoint, unit=Unit.METERS)
          
            if tentativeDistanceToNeighbor >= neighbor.distanceFromStart:
                continue
                 

            neighbor.cameFrom = currentMinDistanceNode # Tail
            neighbor.distanceFromStart = tentativeDistanceToNeighbor # G
            neighbor.estimatedDistanceToEnd = tentativeDistanceToNeighbor + calculateHaversineDistance(neighborPoint, point2, unit=Unit.METERS) # F = G + H
                 
            if not nodesToVisit.containsNode(neighbor):
                nodesToVisit.insert(neighbor)
            else:
                nodesToVisit.update(neighbor) 

    # This is for printing the response time for A* algorithm  
    # print(Heuristic(heuristic).value)
    # print("--- %s seconds ---" % (time.time() - start_time))      
       
    return reconstructPath(endNode)                

                 
def initializeNodes():

    # store all nodes
    processedNodes = {}

    # read the map
    c_file = open("files/map.json", "r")
    c_json_object = json.load(c_file)
    c_file.close()
    
    # get all nodes in the map
    for key, values in c_json_object.items():
       
        # split the string of coordinate
        # ti get the latitude and longitude.
        lat = float(key.split('~')[0])
        lng = float(key.split('~')[1])
     
        # Finally We will create the Node Object
        # to use by A star. 
        newNode = Node(lat, lng)
        newNode.addConnectedNodes(values["connected_nodes"])

        processedNodes[key] =  newNode
 
    return processedNodes





def getNeighboringNodes(node, nodes):
    neighbors = []

    # get all neighbors of the current node
    allconnectedNodes = node.connnectedNodes

    
    for n in allconnectedNodes:
        if(n != None):
            theNeighborNode = nodes[n]
            neighbors.append(theNeighborNode)

    return neighbors


def transformLatLngToId(lat, lng):
    return str(lat) + "~" + str(lng)

    
def reconstructPath(endNode):
    
    detailed_route_info = {
        "path": [], 
        "weight": 0
    }

    # if the cameFrom Object property is null
    # return the detailed route info 
    # with empty list and zero weight.
    if not endNode.cameFrom:
       return detailed_route_info

    
    currentNode = endNode
    path = []

    while currentNode:
        path.append([currentNode.longitude, currentNode.latitude])
        currentNode = currentNode.cameFrom

    detailed_route_info["weight"] = endNode.estimatedDistanceToEnd
    detailed_route_info["path"] = path[::-1]

    return  detailed_route_info
 
  
