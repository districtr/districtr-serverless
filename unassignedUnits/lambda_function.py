import json
import networkx as nx
from networkx.readwrite import json_graph
import boto3

s3 = boto3.client('s3')

def connected_componets(graph):
    return [list(comp) for comp in nx.connected_components(graph)]
    

def lambda_handler(event, context):
    # TODO implement
    
    if 'body' in event.keys():
        event = json.loads(event["body"])
    bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")
    plan_assignment = event["assignment"]
    assigned_units = set(plan_assignment.keys())
    key = "dual_graphs/{}_{}.json".format(state, units)

    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        graph = json_graph.adjacency_graph(json.load(data['Body']))
        graph.remove_nodes_from(assigned_units)
        return {
            'statusCode': 200,
            'body': json.dumps({
                        "unnassigned_units": connected_componets(graph)}),
        }
    
    except Exception as e:
        print(e)
        raise e
    