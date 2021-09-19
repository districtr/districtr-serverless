import statistics
import networkx as nx
from gerrychain import GeographicPartition, updaters, metrics

# Naming constants
county_column = "COUNTY"
municipality_column = "TOWN"

def district_contiguity(district, graph):
    district_graph = graph.subgraph(district)
    return nx.is_connected(district_graph)

def polsby_popper(part):
    scores = [v for _k, v in metrics.polsby_popper(part).items()]
    stats = {
        'max': max(scores),
        'min': min(scores),
        'mean': statistics.mean(scores),
        'median': statistics.median(scores)
    }
    if len(scores) > 1:
        stats['variance'] = statistics.variance(scores)

    return scores, stats


def county_split_info(graph, part, county_pops):
    county_splits = updaters.county_splits("county_splits", county_column)(part)
    county_response = {}
    counties = set([graph.nodes[n][county_column] for n in graph.nodes])
    county_response['num_counties'] = len(counties)
    county_response['population'] = {k: v["population"] for k, v in county_pops.items()}
    
    split_list = {}
    splits = 0
    num_split = 0
    for c in counties:
        s = county_splits[c].contains
        # this is caused by a bug in some states in gerrychain I think
        if -1 in s:
            s.remove(-1)
        if len(s) > 1:
            num_split += 1
            split_list[c] = list(s)
            splits += len(s) - 1
    county_response['splits'] = splits
    county_response['split_list'] = split_list
    return county_response

def municipality_split_info(graph, part):
    municipality_splits = updaters.county_splits("muni_splits", municipality_column)(part)
    muni_response = {}
    munis = set([graph.nodes[n][municipality_column] for n in graph.nodes])
    muni_response['num_counties'] = len(munis)
    try:
        muni_partition = GeographicPartition(graph, municipality_column,
                            {"population": updaters.Tally('TOTPOP', alias="population")})
        muni_pop_dict = {m: muni_partition.population[m] for m in munis}
        muni_response['population'] = muni_pop_dict
        muni_response['num_counties'] = len(munis)
    except KeyError:
        muni_response['population'] = -1
    split_list = {}
    splits = 0
    num_split = 0
    for m in munis:
        s = municipality_splits[m].contains
        # this is caused by a bug in some states in gerrychain I think
        if -1 in s:
            s.remove(-1)
        if len(s) > 1:
            num_split += 1
            split_list[m] = list(s)
            splits += len(s) - 1
    muni_response['splits'] = splits
    muni_response['split_list'] = split_list

def partisan_metrics(part, elections):
    """
    Return information about partisanship metric:
    Scores by elections:
        * seats
        * efficiency gap,
        * mean median
        * partisan bias
        * Eugia's metric (by county)
        * Eugia's metric (by vtds20)

    Scores by plan:
        * # Swing districts
        * # Competitive districts
    """
    response = {"election_scores": {e.name: {} for e in elections},
                "plan_scores": {}}
    return response