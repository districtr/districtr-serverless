import json
import pandas as pd
import boto3

s3 = boto3.client('s3')

def lambda_handler(event, context):
    if 'body' in event.keys():
        event = json.loads(event["body"])
    bucket = "districtr"
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")
    assigned_units = set(event["assignment"])
    centroid_key = "centroids/{}_{}.csv".format(state, units)

    try:
        ctr_data = s3.get_object(Bucket=bucket, Key=centroid_key)
        unit_centroids = pd.read_csv(ctr_data['Body'], dtype={"GEOID": str}).set_index("GEOID")
        coords = unit_centroids.loc[assigned_units]
        

        return {
            'statusCode': 200,
            'body': json.dumps({
                        "assigned_units": [
                            float(coords.LNG.min()),
                            float(coords.LAT.min()),
                            float(coords.LNG.max()),
                            float(coords.LAT.max()),
                            
                        ] }),
        }
    
    except Exception as e:
        print(e)
        raise e
