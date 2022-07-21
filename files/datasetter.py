import os
import json
from flask import Blueprint, jsonify, request, current_app,  make_response




def setTotalCases(baragay_name, totalCases):
    temp = [None, None]
    a_file = open("disrtictIII.geojson", "r")
    a_json_object = json.load(a_file)
    a_file.close()
    
    for idx, obj in enumerate(a_json_object['features']):
    
        if(obj['properties']['brgy_name'] == baragay_name):
            a_json_object['features'][idx]['properties']['total_cases'] = totalCases
            temp[0] = totalCases
            temp[1] = obj['properties']['active_cases']

    a_file = open("disrtictIII.geojson", "w") 
    json.dump(a_json_object, a_file) 
    a_file.close()

    b_file = open("brgy_description.geojson", "r")
    b_json_object = json.load(b_file)
    b_file.close()
    
    for idx1, obj1 in enumerate(b_json_object['features']):
    
        if(obj1['properties']['brgy_name'] == baragay_name):
            t = f"<strong>{baragay_name}</strong><p> Active Cases: {temp[1]}</p><p> Total Cases: {temp[0]}</p>"
            b_json_object['features'][idx1]['properties']['description'] = t

    b_file = open("brgy_description.geojson", "w") 
    json.dump(b_json_object, b_file) 
    b_file.close() 




def addDataToMap(routesGraph):
  
    c_file = open("files/map.json", "r")
    c_json_object = json.load(c_file)
    c_file.close()

    # --------------
    for currentRoute in routesGraph:
        
        
        step_locations = currentRoute["step_locations"]
       
        for idx, stepsInfo in enumerate(step_locations):
            
            location = stepsInfo["location"]
            activeCovidWeights = stepsInfo["active_covid_weight"]
            covidWeights = stepsInfo["covid_weight"]
            barangay_name = None

            if "barangay_name" in stepsInfo:
                barangay_name = stepsInfo["barangay_name"]

            lng, lat = location[0], location[1]

            # access the next location
            theIdNextNode = None
            if(idx < (len(step_locations) - 1)):
                nextNode = step_locations[idx + 1]["location"]
                nextLng, nextLat = nextNode[0], nextNode[1]
                theIdNextNode = str(nextLat) + "~" + str(nextLng)
            
            
            # check if current coordinate is already exist in our map
            theCurrentCoordinate = str(lat) + "~" + str(lng)
           

            isCurrentCoordinateExist = False

            if theCurrentCoordinate in c_json_object:
                isCurrentCoordinateExist = c_json_object[theCurrentCoordinate]

            # if current coordinate is not exist in the map
            # then do this operation.

            if(not isCurrentCoordinateExist):
                coordInfo = {
                    "connected_nodes" : {},
                    "active_cases": activeCovidWeights,
                    "covidWeights": covidWeights,
                    "barangay": barangay_name
                }
                if(idx < (len(step_locations) - 1)):           
                    # add neighbor coordinate
                    coordInfo["connected_nodes"][theIdNextNode] = ""
              

                # create the coordinate in our data  
                c_json_object[theCurrentCoordinate] = coordInfo

            else:
                isNextCoordAlreadyConnected = False 
                isPrevCoordAlreadyConnected = False

                if theIdNextNode in c_json_object[theCurrentCoordinate]["connected_nodes"]:
                    isNextCoordAlreadyConnected = True

                # if theIdPrevNode in c_json_object[theCurrentCoordinate]["connected_nodes"]:
                #     isPrevCoordAlreadyConnected = True
                

                if(not isNextCoordAlreadyConnected):
                    if(idx < (len(step_locations) - 1)):
                        c_json_object[theCurrentCoordinate]["connected_nodes"][theIdNextNode] = ""
        
                
    # --------------
    print("This is the total number of nodes from nodes map: ", len(c_json_object))
   
    a_file = open("files/map.json", "w") 
    json.dump(c_json_object, a_file) 
    a_file.close()
    
    generatePointsGEOJSON(c_json_object)
    


        
        


    



def generatePointsGEOJSON(c_json_object):
    
    fuckingTest = c_json_object.keys()


    theJSONKO = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for val in fuckingTest:
        
        lat = val.split('~')[0]
        lng = val.split('~')[1]
        thedatatoPut = {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]
            }
        }
        theJSONKO["features"].append(thedatatoPut)


    thedatapath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'static/assets/js/output.js'))
   
    print(thedatapath) 
        
    # remove first existing data
    open(thedatapath, 'w').close()

    # add the newly plot geojson
    with open(thedatapath, "a") as f:
        print(f"var outputs = {theJSONKO}", file=f)
        # print(theJSONKO, file=f)

def setActiveCases(baragay_name, activeCases):
    
    temp = [None, None]
    a_file = open("disrtictIII.geojson", "r")
    a_json_object = json.load(a_file)
    a_file.close()
    
    for idx, obj in enumerate(a_json_object['features']):
    
        if(obj['properties']['brgy_name'] == baragay_name):
            a_json_object['features'][idx]['properties']['active_cases'] = activeCases
            temp[0] = obj['properties']['total_cases'] 
            temp[1] = activeCases

    a_file = open("disrtictIII.geojson", "w") 
    json.dump(a_json_object, a_file) 
    a_file.close()

    b_file = open("brgy_description.geojson", "r")
    b_json_object = json.load(b_file)
    b_file.close()
    
    for idx1, obj1 in enumerate(b_json_object['features']):
    
        if(obj1['properties']['brgy_name'] == baragay_name):
            t = f"<strong>{baragay_name}</strong><p> Active Cases: {temp[1]}<br/> Total Cases: {temp[0]}</p>"
            b_json_object['features'][idx1]['properties']['description'] = t

    b_file = open("brgy_description.geojson", "w") 
    json.dump(b_json_object, b_file) 
    b_file.close() 

def setActiveCasesToMapJSON(baragay_name, activeCases):
    
  
    map_file = open("map.json", "r")
    map_json_object = json.load(map_file)
    map_file.close()
    
    for idx, obj in enumerate(map_json_object):
        
        if map_json_object[obj]['barangay'] != None:
            if map_json_object[obj]['barangay'] == baragay_name:
                map_json_object[obj]['active_cases'] = activeCases
            
        else:
            map_json_object[obj]['active_cases'] = 0       
          

    map_file = open("map.json", "w") 
    json.dump(map_json_object, map_file) 
    map_file.close()

def setTotalCasesToMapJSON(baragay_name, totalCases):
    
  
    map_file = open("map.json", "r")
    map_json_object = json.load(map_file)
    map_file.close()
    # print(map_json_object)
    for idx, obj in enumerate(map_json_object):
        
        if map_json_object[obj]['barangay'] != None:
            if map_json_object[obj]['barangay'] == baragay_name:
                map_json_object[obj]['covidWeights'] = totalCases
          

    map_file = open("map.json", "w") 
    json.dump(map_json_object, map_file) 
    map_file.close()






# LATEST DATA DONT CHANGE IT!   
# setTotalCases("AMIHAN", 790)
# setTotalCases("BAGUMBAYAN", 2541)
# setTotalCases("BAGUMBUHAY", 1321)
# setTotalCases("BAYANIHAN", 156)
# setTotalCases("BLUE RIDGE A", 242)
# setTotalCases("BLUE RIDGE B", 219)
# setTotalCases("CAMP AGUINALDO", 1440)
# setTotalCases("CLARO", 799)
# setTotalCases("DIOQUINO ZOBEL", 256)
# setTotalCases("DUYAN-DUYAN", 581)
# setTotalCases("E. RODRIGUEZ", 2456)
# setTotalCases("EAST KAMIAS", 1113)
# setTotalCases("ESCOPA I", 348)
# setTotalCases("ESCOPA II", 109)
# setTotalCases("ESCOPA III", 572)
# setTotalCases("ESCOPA IV", 200)
# setTotalCases("LIBIS", 636)
# setTotalCases("LOYOLA HEIGHTS", 2583)
# setTotalCases("MANGGA", 152)
# setTotalCases("MARILAG", 1865)
# setTotalCases("MASAGANA", 901)
# setTotalCases("MATANDANG BALARA", 5887)
# setTotalCases("MILAGROSA", 1120)
# setTotalCases("PANSOL", 2153)
# setTotalCases("QUIRINO 2-A", 830)
# setTotalCases("QUIRINO 2-B", 819)
# setTotalCases("QUIRINO 2-C", 438)
# setTotalCases("QUIRINO 3-A", 268)
# setTotalCases("ST. IGNATIUS", 306)
# setTotalCases("SAN ROQUE", 2324)
# setTotalCases("SILANGAN", 834)
# setTotalCases("SOCORRO", 4980)
# setTotalCases("TAGUMPAY", 229)
# setTotalCases("UGONG NORTE", 1658)
# setTotalCases("VILLA MARIA CLARA", 478)
# setTotalCases("WEST KAMIAS", 819)
# setTotalCases("WHITE PLAINS", 634)


# setActiveCases("AMIHAN", 0)
# setActiveCases("BAGUMBAYAN", 1)
# setActiveCases("BAGUMBUHAY", 0)
# setActiveCases("BAYANIHAN", 0)
# setActiveCases("BLUE RIDGE A", 0)
# setActiveCases("BLUE RIDGE B", 0)
# setActiveCases("CAMP AGUINALDO", 0)
# setActiveCases("CLARO", 0)
# setActiveCases("DIOQUINO ZOBEL", 0)
# setActiveCases("DUYAN-DUYAN", 0)
# setActiveCases("E. RODRIGUEZ", 0)
# setActiveCases("EAST KAMIAS", 0)
# setActiveCases("ESCOPA I", 0)
# setActiveCases("ESCOPA II", 0)
# setActiveCases("ESCOPA III", 0)
# setActiveCases("ESCOPA IV", 0)
# setActiveCases("LIBIS", 0)
# setActiveCases("LOYOLA HEIGHTS", 1)
# setActiveCases("MANGGA", 0)
# setActiveCases("MARILAG", 0)
# setActiveCases("MASAGANA", 1)
# setActiveCases("MATANDANG BALARA", 1)
# setActiveCases("MILAGROSA", 0)
# setActiveCases("PANSOL", 1)
# setActiveCases("QUIRINO 2-A", 0)
# setActiveCases("QUIRINO 2-B", 0)
# setActiveCases("QUIRINO 2-C", 0)
# setActiveCases("QUIRINO 3-A", 0)
# setActiveCases("ST. IGNATIUS", 0)
# setActiveCases("SAN ROQUE", 0)
# setActiveCases("SILANGAN", 0)
# setActiveCases("SOCORRO", 1)
# setActiveCases("TAGUMPAY", 0)
# setActiveCases("UGONG NORTE", 3)
# setActiveCases("VILLA MARIA CLARA", 0)
# setActiveCases("WEST KAMIAS", 0)
# setActiveCases("WHITE PLAINS", 1)


# LATEST DATA DONT CHANGE IT!   
# setTotalCasesToMapJSON("AMIHAN", 790)
# setTotalCasesToMapJSON("BAGUMBAYAN", 2152)
# setTotalCasesToMapJSON("BAGUMBUHAY", 1321)
# setTotalCasesToMapJSON("BAYANIHAN", 156)
# setTotalCasesToMapJSON("BLUE RIDGE A", 242)
# setTotalCasesToMapJSON("BLUE RIDGE B", 219)
# setTotalCasesToMapJSON("CAMP AGUINALDO", 1440)
# setTotalCasesToMapJSON("CLARO", 799)
# setTotalCasesToMapJSON("DIOQUINO ZOBEL", 256)
# setTotalCasesToMapJSON("DUYAN-DUYAN", 581)
# setTotalCasesToMapJSON("E. RODRIGUEZ", 2456)
# setTotalCasesToMapJSON("EAST KAMIAS", 1113)
# setTotalCasesToMapJSON("ESCOPA I", 348)
# setTotalCasesToMapJSON("ESCOPA II", 109)
# setTotalCasesToMapJSON("ESCOPA III", 572)
# setTotalCasesToMapJSON("ESCOPA IV", 200)
# setTotalCasesToMapJSON("LIBIS", 636)
# setTotalCasesToMapJSON("LOYOLA HEIGHTS", 2583)
# setTotalCasesToMapJSON("MANGGA", 152)
# setTotalCasesToMapJSON("MARILAG", 1865)
# setTotalCasesToMapJSON("MASAGANA", 901)
# setTotalCasesToMapJSON("MATANDANG BALARA", 5887)
# setTotalCasesToMapJSON("MILAGROSA", 1120)
# setTotalCasesToMapJSON("PANSOL", 2153)
# setTotalCasesToMapJSON("QUIRINO 2-A", 830)
# setTotalCasesToMapJSON("QUIRINO 2-B", 819)
# setTotalCasesToMapJSON("QUIRINO 2-C", 438)
# setTotalCasesToMapJSON("QUIRINO 3-A", 268)
# setTotalCasesToMapJSON("ST. IGNATIUS", 306)
# setTotalCasesToMapJSON("SAN ROQUE", 2324)
# setTotalCasesToMapJSON("SILANGAN", 834)
# setTotalCasesToMapJSON("SOCORRO", 4980)
# setTotalCasesToMapJSON("TAGUMPAY", 229)
# setTotalCasesToMapJSON("UGONG NORTE", 165)
# setTotalCasesToMapJSON("VILLA MARIA CLARA", 478)
# setTotalCasesToMapJSON("WEST KAMIAS", 819)
# setTotalCasesToMapJSON("WHITE PLAINS", 634)



# setActiveCasesToMapJSON("AMIHAN", 0)
# setActiveCasesToMapJSON("BAGUMBAYAN", 1)
# setActiveCasesToMapJSON("BAGUMBUHAY", 0)
# setActiveCasesToMapJSON("BAYANIHAN", 0)
# setActiveCasesToMapJSON("BLUE RIDGE A", 0)
# setActiveCasesToMapJSON("BLUE RIDGE B", 0)
# setActiveCasesToMapJSON("CAMP AGUINALDO", 0)
# setActiveCasesToMapJSON("CLARO", 0)
# setActiveCasesToMapJSON("DIOQUINO ZOBEL", 0)
# setActiveCasesToMapJSON("DUYAN-DUYAN", 0)
# setActiveCasesToMapJSON("E. RODRIGUEZ", 0)
# setActiveCasesToMapJSON("EAST KAMIAS", 0)
# setActiveCasesToMapJSON("ESCOPA I", 0)
# setActiveCasesToMapJSON("ESCOPA II", 0)
# setActiveCasesToMapJSON("ESCOPA III", 0)
# setActiveCasesToMapJSON("ESCOPA IV", 0)
# setActiveCasesToMapJSON("LIBIS", 0)
# setActiveCasesToMapJSON("LOYOLA HEIGHTS", 1)
# setActiveCasesToMapJSON("MANGGA", 0)
# setActiveCasesToMapJSON("MARILAG", 0)
# setActiveCasesToMapJSON("MASAGANA", 1)
# setActiveCasesToMapJSON("MATANDANG BALARA", 1)
# setActiveCasesToMapJSON("MILAGROSA", 0)
# setActiveCasesToMapJSON("PANSOL", 1)
# setActiveCasesToMapJSON("QUIRINO 2-A", 0)
# setActiveCasesToMapJSON("QUIRINO 2-B", 0)
# setActiveCasesToMapJSON("QUIRINO 2-C", 0)
# setActiveCasesToMapJSON("QUIRINO 3-A", 0)
# setActiveCasesToMapJSON("ST. IGNATIUS", 0)
# setActiveCasesToMapJSON("SAN ROQUE", 0)
# setActiveCasesToMapJSON("SILANGAN", 0)
# setActiveCasesToMapJSON("SOCORRO", 1)
# setActiveCasesToMapJSON("TAGUMPAY", 0)
# setActiveCasesToMapJSON("UGONG NORTE", 3)
# setActiveCasesToMapJSON("VILLA MARIA CLARA", 0)
# setActiveCasesToMapJSON("WEST KAMIAS", 0)
# setActiveCasesToMapJSON("WHITE PLAINS", 1)





