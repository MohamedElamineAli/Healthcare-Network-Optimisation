import json
import osmnx as ox
import geopandas as gpd
import networkx as nx

place_name = "Algiers, Algeria"

graph = ox.graph_from_place(place_name, network_type="all")


with open('hopitaux.json') as f:
    data = json.load(f)
for hospital in data["hospitals"]:
    theX = hospital["x"]
    theY = hospital["y"]
    id = ox.distance.nearest_nodes(graph, X=theX, Y=theY)
    print(f"{hospital["name"]}: {id}")
    hospital["id"] = id

with open("hospitalWithID.json", "w") as file:
    json.dump(data, file, indent=4)
