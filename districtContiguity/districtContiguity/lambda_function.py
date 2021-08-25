import json
import networkx as nx
from networkx.readwrite import json_graph
import boto3

s3 = boto3.client('s3')

def district_contiguity(district, graph):
    district_graph = graph.subgraph(district)
    return [list(comp) for comp in nx.connected_components(district_graph)]
    

def lambda_handler(event, context):
    # TODO implement
    
    if 'body' in event.keys():
        event = json.loads(event["body"])
    bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")
    # district = event["dist_id"]
    plan_assingment = event["assignment"]
    parts = set(plan_assingment.values())
    key = "dual_graphs/{}_{}.json".format(state, units)

    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        graph = json_graph.adjacency_graph(json.load(data['Body']))
        return {
            'statusCode': 200,
            'body': json.dumps({
                        part: district_contiguity([n for n, p in plan_assingment.items() if p == part],
                                                  graph)
                        for part in parts}),
        }
    
    except Exception as e:
        print(e)
        raise e
    