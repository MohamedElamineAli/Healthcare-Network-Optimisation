from osmnx import routing, distance
from shapely.geometry import shape, Point
from . import searchs



def route_to_geojson(graph,route):
    # receives a route (list of node ID)
    # returns a geojson dictionary for the route used for visualization
    route_edges = routing.route_to_gdf(graph, route, weight='length')
    return route_edges.__geo_interface__


def paths_to_geojson(graph, paths, astar=False):
    # receives a dictionary of {nodeID: [route]} representing the explored set ordered for graph search
    # or a list for visualizing local search strategies
    # returns a list of geojson dictionary used for visualization
    geo_list = []
    if isinstance(paths, dict):
        print("dict")
        for path in paths.values():
            if len(path) == 1:
                continue
            if astar:
                path = path[:2]
            else:
                path = path[-2:]
            #if path.__contains__(2273311835):
                #print(path)
            gdf = routing.route_to_gdf(graph, path, weight='length')
            geo_list.append(gdf.__geo_interface__)
    elif isinstance(paths, list):
        print("list")
        for path in paths:
            gdf = routing.route_to_gdf(graph, path, weight='length')
            geo_list.append(gdf.__geo_interface__)
    return geo_list


def is_inside_algiers(long, lat, js):
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
    point = Point(long, lat)
    feature = js['features'][0]
    polygon = shape(feature['geometry'])
    if polygon.contains(point):
        return True
    return False


def getHospitalsfromSpecialities(hospitals, specialities, general=False):
    results = []
    if general:
        specialities.append("General Emergency")
    if specialities == "all":
        for hospital in hospitals:
            results.append({"name": hospital["name"], "id": hospital["id"], "x": hospital["x"], "y": hospital["y"]})
        return results
    for hospital in hospitals:
        for spc in specialities:
            if spc in hospital["services"]:
                results.append({"name": hospital["name"], "id": hospital["id"], "x": hospital["x"], "y": hospital["y"]})
                break

    return results


def search_handler(hospitals, graph, request):
    lat = request['latitude']
    long = request['longitude']
    orig = distance.nearest_nodes(graph, X=long, Y=lat)
    hosps_dict = getHospitalsfromSpecialities(hospitals, [request['speciality']], general=request['special_general'])
    hosps = [h["id"] for h in hosps_dict]
    hosps_name = [h["name"] for h in hosps_dict]
    print("origin node: ", orig)
    print("names of hospitals to search: ", hosps_name)
    print("searching for a path")
    paths, path = searchs.GSA(graph, orig, hosps, request['search_strat'])
    if paths is None and path is None:
        print("search failed")
        res = {
            "start": (lat, long),
            "end": cord,
            "paths": None,
            "o_path": None,
            "vis_type": None
        }
        return res
    print("search terminated")
    print("generating visualization")
    for h in hosps_dict:
        if h["id"] == path[-1]:
            cord = (h["x"], h["y"])
            break
    route = route_to_geojson(graph, path)
    vis_paths = None
    if request["search_tpe"] == "paths" and request['speciality'] not in ["simulated annealing", "hill climbing"]:
        vis_paths = paths_to_geojson(graph, paths, astar=request["search_strat"] == "astar")
    print("visualization generated")
    response = {
        "start": (lat, long),
        "end": cord,
        "paths": vis_paths,
        "o_path": route,
        "vis_type": "local search" if request["search_strat"] == "local beam" else "graph search"
    }

    return response
