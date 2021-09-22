import json
from networkx.readwrite import json_graph
from gerrychain import Graph, GeographicPartition, Election
from plan_metrics import PlanMetrics
import boto3
s3 = boto3.client('s3')

def plan_evaluation(graph, districtr_assignment, county_pops, elections):
    keys = set(districtr_assignment.keys())
    parts = set(districtr_assignment.values())
    assignment = {n: districtr_assignment[n] if n in keys else -1 for n in graph.nodes()}
    election_names = [e["name"] for e in elections]
    ## sort candidates alphabetically so that the "first" party is consistent.
    election_updaters = {e["name"]: Election(e["name"], {c["name"]: c["key"] 
                                                         for c in sorted(e["candidates"], 
                                                                         key=lambda c: c["name"])})
                         for e in elections}
    
    partition = GeographicPartition(graph, assignment, election_updaters)

    metrics = PlanMetrics(partition, county_pops, election_names)

    # Contiguity
    split_districts = [part for part in parts if not metrics.district_contiguity([n for n, p in districtr_assignment.items() if p == part])]
    contiguity = (split_districts == [])

    # Calculate cut edges
    cut_edges = partition["cut_edges"]

    # Polsby Popper
    try:
        polsbypopper, polsbypopper_stats = metrics.polsby_popper()
    except:
        polsbypopper = []
        polsbypopper_stats = "Polsby Popper unavailable for this geometry."

    # county splits
    try:
        county_response = metrics.county_split_info()
    except:
        county_response = -1

    if len(elections) > 0:
        partisanship_metrics = metrics.partisan_metrics()
    else:
        partisanship_metrics = "Partisanship Metrics unavailable for this geometry."


    # Build Response dictionary
    response = {
        'cut_edges': len(cut_edges),
        'contiguity': contiguity,
        'split': split_districts,
        'polsbypopper': polsbypopper_stats,
        'pp_scores': polsbypopper,
        'num_units': len(graph.nodes),
        'counties': county_response,
        'partisanship': partisanship_metrics
    }
    return response

def lambda_handler(event, context):
    if 'body' in event.keys():
        event = json.loads(event["body"])
    bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")

    try:
        elections = event["elections"]
    except:
        elections = []
    plan_assignment = event["assignment"]
    key = "dual_graphs/{}_{}.json".format(state, units)
    with open("resources/county_totpop_2020.json") as fin:
        county_pops = json.load(fin)[state]

    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        g = json_graph.adjacency_graph(json.load(data['Body']))
        graph = Graph(g)
        return {
            'statusCode': 200,
            'body': json.dumps(plan_evaluation(graph, plan_assignment, county_pops, elections))
        }
    
    except Exception as e:
        print(e)
        return {
            "error": "This state/units ({}, {}) is not supported".format(event["state"], event["units"])
        }
