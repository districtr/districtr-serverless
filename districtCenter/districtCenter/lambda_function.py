import json
import pandas as pd
import numpy as np
# import boto3

# s3 = boto3.client('s3')


def district_center_point(district, place_centroids):
    dist_points = place_centroids.loc[district].values
    centroid = dist_points.mean(axis=0)
    nearest_point_id = np.argmin(np.linalg.norm(dist_points - centroid, axis=1))
    lat, lng = dist_points[nearest_point_id]
    return [lng, lat]
    

def lambda_handler(event, context):
    # TODO implement
    
    if 'body' in event.keys():
        event = json.loads(event["body"])
    # bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")
    district = event["dist_id"]
    district_nodes = event["assignment"]
    # key = "block_assign/{}_{}.json".format(state, units)

    try:
        # data = s3.get_object(Bucket=bucket, Key=key)
        unit_centroids = pd.read_csv("resources/{}_{}.csv".format(state, units), dtype={"GEOID": str}).set_index("GEOID")
        center_point = district_center_point(district_nodes, unit_centroids)
        return {
            'statusCode': 200,
            'body': json.dumps({
                    'dist_id': district,
                    'coord': center_point
                })
        }
    
    except Exception as e:
        print(e)
        raise e
    