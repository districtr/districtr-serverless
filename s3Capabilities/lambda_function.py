# return JSON description on whether S3 has files to calculate number markers, contiguity, and shapefile export
import boto3
import json

s3 = boto3.client('s3')

def lambda_handler(event, context):
    event = json.loads(event["body"])
    
    state = event["state"].lower().replace(" ", "_")
    units = event["units"].lower().replace(" ", "")
    
    bucket = "districtr"
    
    try:
        key = "centroids/{}_{}.csv".format(state, units)
        s3.head_object(Bucket=bucket, Key=key)
        has_centroid = True
    except Exception as e:
        has_centroid = False

    try:
        key = "dual_graphs/{}_{}.json".format(state, units)
        s3.head_object(Bucket=bucket, Key=key)
        has_graph = True
    except Exception as e:
        has_graph = False

    try:
        key = "shapefiles/{}_{}.shp".format(state, units)
        s3.head_object(Bucket=bucket, Key=key)
        has_shp = True
    except Exception as e:
        has_shp = False

    return {
            'statusCode': 200,
            'body': json.dumps({
                    'has_centroid': has_centroid,
                    'has_graph': has_graph,
                    'has_shp': has_shp,
                })
        }
