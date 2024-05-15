import json
import osmnx as ox
from osmnx import distance
import geopandas as gpd
import networkx as nx

place_name = "Algiers, Algeria"
network_type = 'drive'
graph = ox.graph_from_place(place_name, network_type=network_type, simplify=True)


with open('hopitaux.json') as f:
    data = json.load(f)
for hospital in data["hospitals"]:
    theX = hospital["x"]
    theY = hospital["y"]
    id = distance.nearest_nodes(graph, X=theX, Y=theY)
    print(id)
    # print(f"{hospital["name"]}: {id}")
    hospital["id"] = id

with open("hospitalWithID.json", "w") as file:
    json.dump(data, file, indent=4)
