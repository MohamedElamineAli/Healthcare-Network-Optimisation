from osmnx import routing
import json
from shapely.geometry import shape, Point


def route_to_geojson(graph,route):
    # receives a route (list of node ID)
    # returns a geojson dictionary for the route used for visualization
    route_edges = routing.route_to_gdf(graph, route, weight='length')
    return route_edges.__geo_interface__

def paths_to_geojson(graph, paths):
    # receives a dictionary of {nodeID: [route]} representing the explored set ordered
    # returns a list of geojson dictionary used for visualization
    geo_list = []
    fr = True
    for path in paths.values():
        if fr:
            fr = False
            continue
        path = path[-2:]
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


