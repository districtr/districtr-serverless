import pandas as pd
import geopandas as gpd
import networkx as nx
from networkx.readwrite import json_graph
import json
import glob


 # Blockgroups 20
bg_dgs = glob.glob("bg20_dgs/*")

for dg in bg_dgs:
    st_name = dg.split("/")[-1].split(".")[0]

    with open(dg) as fin:
        data = json.load(fin)

    graph = json_graph.adjacency_graph(data)
    mapping = {n: graph.nodes()[n]["GEOID20"] for n in graph.nodes()}
    nx.relabel.relabel_nodes(graph, mapping=mapping, copy=False)
    data_out = json_graph.adjacency_data(graph)
    node_data = [ {"id": n["id"]} for n in data_out["nodes"]]
    data_out["nodes"] = node_data
    with open("graphs/{}_blockgroups20.json".format(st_name), "w") as fout:
        json.dump(data_out, fout)


 # VTDs 20
vtd_dgs = glob.glob("vtd_dg/*")

for dg in vtd_dgs:
    st_name = dg.split("/")[-1].split(".")[0]

    with open(dg) as fin:
        data = json.load(fin)

    graph = json_graph.adjacency_graph(data)
    mapping = {n: graph.nodes()[n]["GEOID20"] for n in graph.nodes()}
    nx.relabel.relabel_nodes(graph, mapping=mapping, copy=False)
    data_out = json_graph.adjacency_data(graph)
    node_data = [ {"id": n["id"]} for n in data_out["nodes"]]
    data_out["nodes"] = node_data
    with open("graphs/{}_vtds20.json".format(st_name), "w") as fout:
        json.dump(data_out, fout)


for dg in ["vtd_dg/montana.json"]:
    st_name = dg.split("/")[-1].split(".")[0]

    with open(dg) as fin:
        data = json.load(fin)

    graph = json_graph.adjacency_graph(data)
    mapping = {n: graph.nodes()[n]["GEOID20"] for n in graph.nodes()}
    nx.relabel.relabel_nodes(graph, mapping=mapping, copy=False)
    data_out = json_graph.adjacency_data(graph)
    node_data = [ {"id": n["id"]} for n in data_out["nodes"]]
    data_out["nodes"] = node_data
    with open("graphs/{}_vtds20.json".format(st_name), "w") as fout:
        json.dump(data_out, fout)