from osmnx import routing
import json
from shapely.geometry import shape, Point


def route_to_geojson(graph,route):
    # receives a route (list of node ID)
    # returns a geojson dictionary for the route used for visualization
    route_edges = routing.route_to_gdf(graph, route, weight='length')
    return route_edges.__geo_interface__

def paths_to_geojson(graph, paths):
    # receives a dictionary of {nodeID: [route]} representing the explored set ordered for graph search
    # or a list for visualizing local search strategies
    # returns a list of geojson dictionary used for visualization
    geo_list = []
    if isinstance(paths,dict):
        fr = True
        for path in paths.values():
            if fr:
                fr = False
                continue
            path = path[-2:]
            gdf = routing.route_to_gdf(graph, path, weight='length')
            geo_list.append(gdf.__geo_interface__)
    elif isinstance(paths,list):
        for path in paths:
            gdf = routing.route_to_gdf(graph, path, weight='length')
            geo_list.append(gdf.__geo_interface__)
    return geo_list

def is_inside_algiers(point, js):
    """
    This function checks if a given point is inside Algiers.
    
    Parameters:
    ----------
    point (shapely.geometry.Point): A point representing a location.
    js (dict): A GeoJSON object representing Algiers.
    
    Returns:
    -------
    bool: True if the point is inside Algiers, False otherwise.
    """
    feature = js['features'][0]
    
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        return True

    return False

def getHospitalsfromSpecialities(hospitals, specialities):
    results = []
    if specialities == "all":
        for hospital in hospitals:
            results.append({"name": hospital["name"], "id": hospital["id"], "c": hospital["x"], "y": hospital["y"]})
        return results

    for hospital in hospitals:
        for spc in specialities:
            if spc in hospital["services"]:
                results.append({"name": hospital["name"], "id": hospital["id"], "c": hospital["x"], "y": hospital["y"]})
                break

    return results


def search_handler(hospitals, graph, request):
    lat = request['latitude']
    long = request['longitude']
    orig = distance.nearest_node(graph, X=long, Y=lat)

    hosps_dict = getHospitalsfromSpecialities(hospitals, request['speciality'], request['special_treatment'])

    hosps = [h["id"] for h in hosps_dict]

    paths, path = GSA(graph, orig, hosps, request['search_strat'])

    for h in hosps_dict:
        if h["id"] == path[-1]:
            cord = (h["c"], h["y"])
            break
    
    paths = paths_to_geojson(graph, paths)

    response = {
        "start": (lat, long),
        "end": cord,
        "paths": paths,
        "o_path": path
    }

    return response
