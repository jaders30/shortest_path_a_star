import json
from flask import Blueprint, jsonify, request, current_app,  make_response
from algo.aStar import aStarAlgorithm
from files.datasetter import addDataToMap
from pprint import pprint 
api = Blueprint('api', __name__)


@api.route('/possibleroutes', methods = ['POST'])
def possibleroutes():
    requestData  = json.loads(request.data)
   
    thedata = requestData["lisOfAllRoutes"]

    # get the first example route
    lclen = len(thedata[0]["step_locations"])
    pp  = thedata[0]["step_locations"][0]["location"]
    pp1 = thedata[0]["step_locations"][lclen - 1]["location"]
    
    # make tuple
    point1 = (pp[1], pp[0])
    point2 = (pp1[1], pp1[0])
   
    # put the search path in our map
    addDataToMap(thedata)

    shortest_route = []

    shortest_route = aStarAlgorithm(point1, point2)
    
    _result = {
        "shortest_route": shortest_route 
    } 

    return jsonify(_result) 



