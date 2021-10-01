from os import environ
import json
import base64
from pymongo import MongoClient
import boto3

s3 = boto3.client('s3')

dburl = environ.get('DATABASE_URL')
client = MongoClient(dburl, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                            connect=False, maxPoolsize=1)
mdb = client.test

def lambda_handler(event, context):
    id = int(event["queryStringParameters"]["simple_id"])
    fname = str(id) + '.png'
    plan = mdb.plans.find_one({ 'simple_id': id }, { 'simple_id': 1, 'screenshot2': 1 })
    result = 'no screenshot'
    
    if (plan is not None)  and ('screenshot2' in plan):
        oldpng = plan['screenshot2']
        if 'data:image' in oldpng:
            pngout = base64.b64decode(oldpng[22:])
            s3.put_object(Bucket="districtr-public", Key=fname, ContentType='image/png', Body=pngout)
            mdb.plans.update_one({ 'simple_id': id }, { '$set': { 'screenshot2': 'https://districtr-public.s3.us-east-1.amazonaws.com/' + fname } })
            result = 'uploaded'
        else:
            result = 'no data url'
    
    return {
        'statusCode': 200,
        'body': result
    }
