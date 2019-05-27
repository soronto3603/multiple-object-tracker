import json

filename = "data.json"

json_data = None
try:
    with open(filename) as f:
        json_data = f.read()
        json_data = json.loads(json_data)

except FileNotFoundError as e:
    print("FileNotFoundError : {0}".format(e))
    raise Exception("JSON is None")

geo_json = {
    "type" : "FeatureCollection",
    "features" : [

    ]
}

for v in enumerate(json_data["temporalGeometry"]["values"]):
    v = v[1]
    value = {
        "type" : "Feature",
        "geometry" : {
            "type" : "Point", 
            "coordinates" : [v["lon"],v["lat"]]
        },
        "properties" : {
            "prop0" : "image coord"
        }
        
    }
    geo_json["features"].append(value)

    for k in v["annotations"]:
        if(k["lon"] == None and k["lat"] == None ):
            pass
        else:
            value = {
                "type" : "Feature",
                "geometry" : {
                    "type" : "Point", 
                    "coordinates" : [k["lon"],k["lat"]]
                },
                "properties" : {
                    "prop0" : k["id"]
                }
                
            }
with open("C:/Users/MCA/Documents/1/multiple-object-tracker/result/data.json", 'w') as outfile:
    json.dump(geo_json, outfile)
# {
#   "type": "FeatureCollection",
#   "features": [
#     {
#       "type": "Feature",
#       "geometry": {
#         "type": "Point",
#         "coordinates": [102.0, 0.5]
#       },
#       "properties": {
#         "prop0": "value0"
#       }
#     },
#     {
#       "type": "Feature",
#       "geometry": {
#         "type": "LineString",
#         "coordinates": [
#           [102.0, 0.0], [103.0, 1.0], [104.0, 0.0], [105.0, 1.0]
#         ]
#       },
#       "properties": {
#         "prop0": "value0",
#         "prop1": 0.0
#       }
#     },
#     {
#       "type": "Feature",
#       "geometry": {
#         "type": "Polygon",
#         "coordinates": [
#           [
#             [100.0, 0.0], [101.0, 0.0], [101.0, 1.0],
#             [100.0, 1.0], [100.0, 0.0]
#           ]
#         ]
#       },
#       "properties": {
#         "prop0": "value0",
#         "prop1": { "this": "that" }
#       }
#     }
#   ]
# }