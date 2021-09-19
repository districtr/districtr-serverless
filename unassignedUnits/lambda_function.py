import json
import networkx as nx
import pandas as pd
from networkx.readwrite import json_graph
import boto3

s3 = boto3.client('s3')

def connected_components(graph):
    return [list(comp) for comp in nx.connected_components(graph)]
    

def lambda_handler(event, context):
    if 'body' in event.keys():
        event = json.loads(event["body"])
    bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")
    assigned_units = set(event["assignment"])
    key = "dual_graphs/{}_{}.json".format(state, units)
    centroid_key = "centroids/{}_{}.csv".format(state, units)

    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        graph = json_graph.adjacency_graph(json.load(data['Body']))
        graph.remove_nodes_from(assigned_units)
        
        hole_ids = connected_components(graph)
        largest_segment_ids = (sorted(hole_ids, key=lambda x: len(x), reverse=True))[0]
        
        ctr_data = s3.get_object(Bucket=bucket, Key=centroid_key)
        unit_centroids = pd.read_csv(ctr_data['Body'], dtype={"GEOID": str}).set_index("GEOID")
        coords = unit_centroids.loc[unit_centroids.index.intersection(set(largest_segment_ids))]
        

        return {
            'statusCode': 200,
            'body': json.dumps({
                        "unassigned_units": [
                            float(coords.LNG.min()),
                            float(coords.LAT.min()),
                            float(coords.LNG.max()),
                            float(coords.LAT.max()),
                            
                        ] }),
        }
    
    except Exception as e:
        print(e)
        raise e
