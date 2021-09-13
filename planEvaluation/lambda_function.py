import json
import statistics
import networkx as nx
from networkx.readwrite import json_graph
from gerrychain import Graph, GeographicPartition, updaters, metrics
import boto3
s3 = boto3.client('s3')

def plan_evaluation(partition):
    graph = partition.graph

    # Naming constants
    county_column = "COUNTY"
    municipality_column = "TOWN"

    # Contiguity
    split_districts = []
    for district in partition.parts.keys():
        if district != -1:
            part_contiguous = nx.is_connected(partition.subgraphs[district])
            if not part_contiguous:
                split_districts.append(district)
    contiguity = (len(split_districts) == 0)

    # Calculate cut edges
    cut_edges = updaters.cut_edges(partition)

    # Polsby Popper
    try:
        polsbypopper = [v for _k, v in metrics.polsby_popper(partition).items()]
        polsbypopper_stats = {
            'max': max(polsbypopper),
            'min': min(polsbypopper),
            'mean': statistics.mean(polsbypopper),
            'median': statistics.median(polsbypopper)
        }
        if len(polsbypopper) > 1:
            polsbypopper_stats['variance'] = statistics.variance(polsbypopper)
    except:
        polsbypopper = []
        polsbypopper_stats = "Polsby Popper unavailable for this geometry."

    
    # county splits

    try:
        county_splits = updaters.county_splits("county_splits", county_column)(partition)
        county_response = {}
        counties = set([graph.nodes[n][county_column] for n in graph.nodes])
        county_response['num_counties'] = len(counties)
        try:
            county_partition = GeographicPartition(graph, county_column,
                                                   {"population": updaters.Tally('TOTPOP', alias="population")})
            county_pop_dict = {c: county_partition.population[c] for c in counties}
            county_response['population'] = county_pop_dict
        except KeyError:
            county_response['population'] = -1
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
    except:
        county_response = -1

    # municipality splits
    try:
        municipality_splits = updaters.county_splits("muni_splits", municipality_column)(partition)
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
    except:
        muni_response = -1

    # Build Response dictionary
    response = {
        'cut_edges': len(cut_edges),
        'contiguity': contiguity,
        'split': split_districts,
        'polsbypopper': polsbypopper_stats,
        'pp_scores': polsbypopper,
        'num_units': len(graph.nodes),
        'counties': county_response,
        'municipalities': muni_response
    }
    return response

def lambda_handler(event, context):
    if 'body' in event.keys():
        event = json.loads(event["body"])
    bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")
    # district = event["dist_id"]
    plan_assignment = event["assignment"]
    keys = set(plan_assignment.keys())
    key = "dual_graphs/{}_{}.json".format(state, units)

    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        g = json_graph.adjacency_graph(json.load(data['Body']))
        graph = Graph(g)
        assignment = {n: plan_assignment[n] if n in keys else -1 for n in graph.nodes()}
        part = GeographicPartition(graph, assignment)
        return {
            'statusCode': 200,
            'body': json.dumps(plan_evaluation(part))
        }
    
    except Exception as e:
        print(e)
        return {
            "error": "This state/units ({}, {}) is not supported".format(event["state"], event["units"])
        }
