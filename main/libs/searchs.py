from heapq import heappop, heappush
from itertools import count
from math import radians, sin, cos, sqrt, atan2, exp
from random import randint, uniform

def cowl_flew_distance(coordinates, goal_coordinates):
        # Get latitude and longitude coordinates for each city
        lat1, lon1 = coordinates
        lat2, lon2 = goal_coordinates
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        # Calculate the straight-line distance using Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        h = 6371 * c # Radius of the Earth in kilometers
        return h

def uclidian_distance(coordinates, goal_coordinates):
        # Get latitude and longitude coordinates for each city
        lat1, lon1 = coordinates
        lat2, lon2 = goal_coordinates
        
        return sqrt((lat1-lat2)**2 + (lon1-lon2)**2)


def path_distance(G, path):
    G_succ = G._adj  # adjacency list of the graph for speed-up
    dist = 0
    for i in range(len(path)-1):  # for each node in the path
        edge = G_succ[path[i]][path[i+1]]  # get the edge between the current node and the next node
        dist += min(attr.get('length', 1) for attr in edge.values())  # add the length of the edge to the distance
    return dist  # return the total distance of the path


def path_change(G, path):
    begin = randint(0, len(path)-2)  # randomly select a start index
    end = randint(min(begin+20, len(path)-2), min(begin+40, len(path)-1))  # randomly select an end index

    paths = {
        path[begin]: [path[begin]]  # initialize paths with the path from the start node to itself
    }

    UCS(G, path[begin], targets=[path[end]], paths=paths)  # find the shortest path from the start node to the end node
    mini_path = paths[path[end]]  # get the shortest path
    new_path = path[:begin] + mini_path + path[end+1:]  # construct the new path

    return new_path  # return the new path




def Astar(G, sources, paths=None, target=None):
    G_succ = G._pred  # adjacency list of the graph for speed-up

    push = heappush  # alias for heappush function
    pop = heappop  # alias for heappop function
    explored_set = {}  # set of explored nodes

    # use the count c to avoid comparing nodes
    c = count()  # counter for nodes

    # frontier is heapq with 4-tuples (f,c,distance,node)
    frontier = []  # priority queue for frontier nodes
    goal_cord = (G.nodes[target]['x'], G.nodes[target]['y'])  # coordinates of the target node

    for source in sources:  # for each source node
        explored_set[source] = 0  # initialize distance to source itself as 0

        data = G.nodes[source]  # get the data of the source node
        cord = (data['x'], data['y'])  # coordinates of the source node
        h_dist = 1000*uclidian_distance(cord, goal_cord)  # calculate heuristic distance from source to target

        push(frontier, (h_dist, next(c), 0, source))  # push source to frontier with heuristic distance
    while frontier:  # while there are nodes in frontier
        (_, _, dist, current_node) = pop(frontier)  # pop a node from frontier

        if current_node == target:  # if the current node is the target
            break  # we found the shortest path to the target
        for neighbor, edge in G_succ[current_node].items():  # for each neighbor of current node
            cost = min(attr.get('length', 1) for attr in edge.values())  # get the cost of the edge
            data = G.nodes[neighbor]  # get the data of the neighbor
            cord = (data['x'], data['y'])  # coordinates of the neighbor
            h_dist = 1000*uclidian_distance(cord, goal_cord)  # calculate heuristic distance from neighbor to target

            if cost is None:
                continue
            neighbor_dist = dist + cost  # calculate tentative distance to neighbor
            f_dist = neighbor_dist + h_dist  # calculate f-score for neighbor

            if neighbor not in explored_set or neighbor_dist < explored_set[neighbor]:  # if neighbor is not explored or we found a shorter path
                explored_set[neighbor] = neighbor_dist  # update the distance
                push(frontier, (f_dist, next(c), neighbor_dist, neighbor))  # push the neighbor to the frontier

                if paths is not None:
                    paths[neighbor] = paths[current_node] + [neighbor]  # update the path to neighbor

    return dist  # return the shortest distance from the nearest source node to the target node





def UCS(G, source, paths=None, targets=None):
    G_succ = G._adj  # adjacency list of the graph for speed-up

    push = heappush  # alias for heappush function
    pop = heappop  # alias for heappop function
    dist = {}  # dictionary of final distances from source to each node
    explored_set = {}  # set of explored nodes

    # use the count c to avoid comparing nodes (may not be able to)
    c = count()  # counter for nodes
    
    # frontier is heapq with 3-tuples (distance, c, node)
    frontier = []  # priority queue

    push(frontier, (0, next(c), source))  # push source to frontier with distance 0

    while frontier:
        (d, _, current_node) = pop(frontier)  # pop a node from frontier
        if current_node in dist:
            continue  # already searched this node.
        dist[current_node] = d  # update the shortest distance of current node

        if current_node in targets:
            break  # we found the shortest path to the target

        for neighbor, edge in G_succ[current_node].items():  # for each neighbor of current node
            cost = min(attr.get('length', 1) for attr in edge.values())  # get the cost of the edge
            if cost is None:  # if cost is None, skip this neighbor
                continue
            neighbor_dist = dist[current_node] + cost  # calculate tentative distance to neighbor

            if neighbor in dist:  # if neighbor was already visited
                u_dist = dist[neighbor]  # get the shortest known distance to neighbor
                if neighbor_dist < u_dist:  # if we found a shorter path
                    raise ValueError("Contradictory paths found:", "negative weights?")  # this should not happen in UCS

            elif neighbor not in explored_set or neighbor_dist < explored_set[neighbor]:  # if neighbor is not explored or we found a shorter path
                explored_set[neighbor] = neighbor_dist  # update the distance
                push(frontier, (neighbor_dist, next(c), neighbor))  # push the neighbor to the frontier

                if paths is not None:
                    paths[neighbor] = paths[current_node] + [neighbor]  # update the path to neighbor

    return dist, current_node



def Local_beam(G, intial_path, paths_list=None):
    paths = []
    new_paths = []

    for _ in range(10):  # for each iteration
        new_path = path_change(G, intial_path)  # find a better successor path from the initial path
        new_path_length = path_distance(G, new_path)  # calculate the length of the new path

        paths.append((new_path_length, new_path))  # append the new path to paths

    paths.sort()  # sort paths by length

    best_path_length = paths[0][0]  # calculate the length of the best path
    new_best_path_lenght = 0

    tries = 50
    while tries:  # while not break
        for i in range(5):  # for each of the first 10 paths
            for _ in range(2):  # for each iteration
                new_path = path_change(G, paths[i][1])  # change the path
                new_path_length = path_distance(G, new_path)  # calculate the length of the new path
                new_paths.append((new_path_length, new_path))  # append the new path to new_paths

        paths = sorted(new_paths)  # sort new_paths by length
        new_best_path_lenght = paths[0][0]  # get the length of the best new path

        if new_best_path_lenght >= best_path_length:  # if the best new path is not shorter than the previous best path
            tries-=1
        else:
            best_path_length = new_best_path_lenght  # update best_path_length
            tries = 50  # reset tries

        paths_list.append(paths[0][1])

    return paths[0][1]  # return the best path






def Hill_climbing(G, source, paths=None, targets=None):
    G_succ = G._adj  # adjacency list of the graph for speed-up

    # neighbors is heapq with 3-tuples (heuristic cost, distance, node)
    source_cord = (G.nodes[source]['x'], G.nodes[source]['y'])  # coordinates of the source node
    dist = 0  # current distance to 0

    h_target = float('inf')
    goal_cord = (0, 0)
    goal = 0
    for target in targets:
        data = G.nodes[target]  # get the data of the target node
        cord = (data['x'], data['y'])  # coordinates of the target node
        h_dist = 1000*cowl_flew_distance(cord, source_cord)  # calculate heuristic distance from target to source
        if h_target > h_dist:  # search for the target node with the smallest heuristic cost
            h_target = h_dist
            goal_cord = cord
            goal = target

    h_dist = 1000*cowl_flew_distance(source_cord, goal_cord) # calculate heuristic distance from source to target
    neighbors = [(h_dist, 0, source)]  # initialize neighbors with infinite heuristic cost

    pre_h = float('inf')
    r = 200  # number of random rounds
    t = 0  # counter of steps in each random round
    is_found = False  #  indicates whether the target has been found

    while neighbors and r > 0:  # while there are neighbors and r > 0
        (cur_h , dist, current_node) = neighbors[0]  # get the heuristic cost, distance, and node of the closest neighbor to the target

        if current_node == goal:  # if the current node is the target
            is_found = True  # set is_found to True
            break

        if cur_h >= pre_h:  # if the current heuristic cost is greater than or equal to the previous heuristic cost
            r -= 1
            t = 20
        
        if t > 0: 
            t -= 1 
            rand = randint(0, len(neighbors) - 1)  # generate a random index
            (pre_h , dist, current_node) = neighbors[rand]  # get the heuristic cost, distance, and node of the neighbor
        else:
            pre_h = cur_h  # set previous heuristic cost to current heuristic cost
        
        temp_neighbors = []  # initialize a list to store the neighbors of the current node
        for neighbor, edge in G_succ[current_node].items():  # for each neighbor of the current node
            cost = min(attr.get('length', 1) for attr in edge.values())  # get the smallest cost of the edge
            data = G.nodes[neighbor]  # get the data of the neighbor
            cord = (data['x'], data['y'])  # coordinates of the neighbor
            h_dist = 1000*cowl_flew_distance(cord, goal_cord)  # calculate heuristic distance from neighbor to target

            if cost is None:  # if cost is None, skip this neighbor
                continue
            neighbor_dist = dist + cost  # calculate distance to neighbor

            temp_neighbors.append((h_dist, neighbor_dist, neighbor))  # append the neighbor to temp_neighbors
            if paths is not None:  # if paths need to be recorded
                paths[neighbor] = paths[current_node] + [neighbor]  # update the path to neighbor
        
        if temp_neighbors:  # if there are neighbors of the current node
            neighbors = sorted(temp_neighbors)  # sort neighbors by heuristic cost
    
    return dist, is_found, goal  # return the distance and whether the target has been found




def Simulated_annealing(G, source, paths=None, targets=None):
    T0 = 10000000000000000000000  # initial temperature
    a = 0.98  # cooling rate
    G_succ = G._adj  # adjacency list of the graph for speed-up
    source_cord = (G.nodes[source]['x'], G.nodes[source]['y'])  # coordinates of the source node
    dist = 0  # current distance to 0
    last_dist = 0  # previous distance to 0

    h_target = float('inf')
    goal_cord = (0, 0)
    goal = 0
    for target in targets:
        data = G.nodes[target]  # get the data of the target node
        cord = (data['x'], data['y'])  # coordinates of the target node
        h_dist = 1000*cowl_flew_distance(cord, source_cord)  # calculate heuristic distance from target to source
        if h_target > h_dist:  # search for the target node with the smallest heuristic cost
            h_target = h_dist
            goal_cord = cord
            goal = target

    h_dist = 1000*cowl_flew_distance(source_cord, goal_cord) # calculate heuristic distance from source to target
    neighbors = [(h_dist, 0, source)]  # initialize neighbors with infinite heuristic cost
    
    T = T0  # set temperature to initial temperature
    i = -1  # number of iterations
    is_found = False  # indicates whether the target has been found
    while T > 0.01:
        i += 1
        rand = randint(0, len(neighbors)-1)  # generate a random index
        (current_dist, dist, current_node) = neighbors[rand]  # get the heuristic cost, distance, and node of the neighbor at the random index
        Delta = current_dist - last_dist  # calculate the difference between the current heuristic cost and the last heuristic cost

        if Delta < 0:  # if Delta is less than 0
            proba = uniform(0, 1)  # generate a random probability
            if proba > exp(Delta/T):  # if the random probability is greater than the exponential of Delta divided by the temperature
                T = a**i * T0  # update the temperature
                continue  # continue to the next iteration

        T = a**i * T0  # update the temperature

        last_dist = current_dist  # update last_dist to current_dist

        if current_node == goal:
            is_found = True  # if the current node is the target node, set is_found to True
            break
        
        temp_neighbors = []  # initialize temp_neighbors (a list to store the neighbors of the current node)
        for neighbor, edge in G_succ[current_node].items():  # for each neighbor of the current node
            cost = min(attr.get('length', 1) for attr in edge.values())  # get the cost of the edge
            data = G.nodes[neighbor]  # get the data of the neighbor
            cord = (data['x'], data['y'])  # coordinates of the neighbor
            h_dist = 1000*cowl_flew_distance(cord, goal_cord)  # calculate heuristic distance from neighbor to target

            if cost is None:  # if cost is None, skip this neighbor
                continue
            neighbor_dist = dist + cost  # calculate tentative distance to neighbor
            f_dist = h_dist + neighbor_dist  # calculate f-score for neighbor

            temp_neighbors.append((f_dist, neighbor_dist, neighbor))  # append the neighbor to temp_neighbors
            if paths is not None:  # if paths need to be recorded
                paths[neighbor] = paths[current_node] + [neighbor]  # update the path to neighbor
        
        if temp_neighbors:  # if there are neighbors of the current node
            neighbors = temp_neighbors  # update neighbors with temp_neighbors
    
    return dist, is_found, goal  # return the distance of the path and whether the target has been found




def BFS(G, source, paths=None, targets=None):
    G_succ = G._adj  # adjacency list of the graph for speed-up (and works for both directed and undirected graphs)

    dist = 0  # initialize distance to 0
    explored_set = {}  # set of explored nodes

    # frontier is a list with 2-tuples (distance ,node)
    frontier = []  # list for fringe nodes
    frontier.append((0, source))  # append the source to frontier with distance 0
    while frontier:  # while there are nodes in frontier
        (dist, current_node) = frontier.pop(0)  # pop a node from frontier

        if current_node in targets:  # if the current node is the target
            break  # we found the shortest path to the target
        for neighbor, edge in G_succ[current_node].items():  # for each neighbor of current node
            cost = min(attr.get('length', 1) for attr in edge.values())  # get the cost of the edge

            if cost is None:  # if cost is None, skip this neighbor
                continue
            neighbor_dist = dist + cost  # calculate tentative distance to neighbor

            if neighbor not in explored_set or neighbor_dist < explored_set[neighbor]:  # if neighbor is not explored or we found a shorter path
                explored_set[neighbor] = neighbor_dist  # update the distance
                frontier.append((neighbor_dist, neighbor))  # append the neighbor to the frontier

                if paths is not None:  # if paths need to be recorded
                    paths[neighbor] = paths[current_node] + [neighbor]  # update the path to neighbor

    return dist, current_node  # return the shortest distance from the nearest source node to the target node




def GSA(G, source, targets, strategy):
    """
    Executes a search algorithm on a graph from a single source node to multiple target nodes.

    Parameters:
    ----------
    G : NetworkX graph
        The graph on which the search is to be performed.
    source : int
        The identifier of the starting node.
    targets : list
        A list of goal nodes to be reached.
    strategy : str
        The search algorithm to be used. The available strategies are:
        'bfs' (Breadth-First Search), 'ucs' (Uniform Cost Search), 'astar' (A* Search),
        'simulated annealing', 'hill climbing', and 'local beam'. The strategy names are case-insensitive.

    Returns:
    -------
    tuple
        A tuple containing two elements:
        paths (dict): A dictionary where the keys are node identifiers and the values are lists representing the paths explored by the search.
        path (list): A list representing the solution path.
    """
    print("test 17")
    paths = {}  # dictionary of paths
    targ = None
    strategy = strategy.lower()
    match strategy:
        case "bfs":
            paths[source] = [source]
            _, targ = BFS(G, source, paths, targets)
        
        case "ucs":
            paths[source] = [source]
            _, targ = UCS(G, source, paths, targets)
        
        case "astar":
            for target in targets:
                paths[target] = [target]
            Astar(G, targets, paths=paths, target=source)

        case "simulated annealing":
            paths[source] = [source]
            
            is_found = False
            while not is_found:
                _, is_found, targ = Simulated_annealing(G, source, paths=paths, targets=targets)
        
        case "hill climbing":
            paths[source] = [source]
            
            is_found = False
            while not is_found:
                _, is_found, targ = Hill_climbing(G, source, paths=paths, targets=targets)
        
        case "local beam":
            paths[source] = [source]
            
            is_found = False
            while not is_found:
                _, is_found, targ = Hill_climbing(G, source, paths=paths, targets=targets)
            path = paths[targ]

            paths_list = [path] # list of some paths to represent
            path = Local_beam(G, path, paths_list=paths_list)
            paths_len = int(len(paths_list) / 10)
            new_paths = [paths_list[i*paths_len] for i in range(9)] # choose 9 paths from paths_list
            new_paths.append(path) # add the last and the optimal path found

            return new_paths, path
        
        case _:
            raise ValueError("Invalid strategy")
    
    if strategy == "astar":
        path = paths[source][::-1]  # reverse the path because it is from the target to the source as mentioned in the report
        for key in paths:
            paths[key] = paths[key][::-1]
    else:
        path = paths[targ]

    return paths, path

