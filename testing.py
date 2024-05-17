import json
import _pickle as cPickle
from libs import utils


print("fetching graph..")
with open(r"data/algiers_raw_simplified.pkl", "rb") as input_file:
    graph = cPickle.load(input_file)
print("done fetching")


orig = 1695213633
hosps = [288638091, 317900796, 2273311695, 326287634, 2270089111, 371922651, 975658312, 418189851, 289912820]
paths, path = utils.searchs.GSA(graph, orig, hosps, 'astar')
with open(r"paths_astar.json", 'w') as file:
    json.dump(paths, file,indent=2)
