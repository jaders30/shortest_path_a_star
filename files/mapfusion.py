import json

# utility function
def mergeMap():
    old_map = open("../files/owel_map_old.json", "r")
    old_json_object = json.load(old_map)
    old_map.close()

    new_map = open("../files/owel_map_new.json", "r")
    new_json_object = json.load(new_map)
    new_map.close()

   
    for nodeName in old_json_object:
        # get info
        nodeInfo = old_json_object[nodeName]
        # check if the node exist
        if nodeName in new_json_object:
            # get all connected nodes
            # print(nodeInfo)
            connectedNodesOfOld = nodeInfo["connected_nodes"]
            # traverse in all connected nodes
            for conn_nodes in connectedNodesOfOld:
                theConnectedNodesOfNewMap = new_json_object[nodeName]["connected_nodes"]
                
                if not conn_nodes in theConnectedNodesOfNewMap:
                    new_json_object[nodeName]["connected_nodes"][conn_nodes] = ""
        else:
            new_json_object[nodeName] = nodeInfo
    

    output_file = open("../files/fusionResult.json", "w") 
    json.dump(new_json_object, output_file) 
    output_file.close()


mergeMap()