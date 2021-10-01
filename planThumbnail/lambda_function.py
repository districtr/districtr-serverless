import base64
import io
import os
import json

import boto3
import geopandas as gpd
import matplotlib.pyplot as plt
from pymongo import MongoClient

dburl = os.environ.get('DATABASE_URL')
client = MongoClient(dburl, connectTimeoutMS=30000, socketTimeoutMS=None, socketKeepAlive=True,
                            connect=False, maxPoolsize=1)
mdb = client.test

s3 = boto3.client('s3')

statewide = [
        'ma',
        'ma_02',
        'ma_12',
        'nc',
        'new_mexico',
        'new_mexico_bg',
        'wadc',
        'dc',
        'indianaprec',
        'wisco2019acs',
        'puertorico_prec',
    ]

def coloration(row, id_column_key, assignment):
    cs_bright = [
        "#555555", "#0099cd", "#ffca5d", "#00cd99", "#99cd00", "#cd0099", "#9900cd", "#8dd3c7",
        "#bebada", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#fccde5", "#bc80bd", "#ccebc5",
        "#ffed6f", "#ffffb3", "#a6cee3", "#1f78b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c",
        "#fdbf6f", "#ff7f00", "#cab2d6", "#6a3d9a", "#b15928", "#64ffda", "#00B8D4", "#A1887F",
        "#76FF03", "#DCE775", "#B388FF", "#FF80AB", "#D81B60", "#26A69A", "#FFEA00", "#6200EA"
    ]
    if (str(row[id_column_key]).replace('.', '÷') in assignment):
        idx = assignment[str(row[id_column_key]).replace('.', '÷')]
        if isinstance(idx, list):
            idx = idx[0]
        idx += 1
        if idx >= len(cs_bright) - 1:
            idx = (idx % (len(cs_bright) - 1)) + 1
        return cs_bright[idx]
    elif (row[id_column_key] in assignment):
        idx = assignment[row[id_column_key]]
        if isinstance(idx, list):
            idx = idx[0]
        idx += 1
        if idx >= len(cs_bright) - 1:
            idx = (idx % (len(cs_bright) - 1)) + 1
        return cs_bright[idx]
    else:
        return cs_bright[0]

def lambda_handler(event, context):
    if 'body' in event.keys():
        event = json.loads(event["body"])
    origin = event['id']
    
    p = mdb.plans.find_one({ 'simple_id': int(origin) })
    if p is None:
        return {
            'statusCode': 404,
            'body': 'Plan not found in db',
        }
    bucket = "districtr"
    plan = p['plan']
    place_id = plan['placeId'] # get the plan id of the Districtr plan
    unit_id = plan["units"]["id"].replace('vtds20', 'vtd20')
    assignment = plan["assignment"] if "assignment" in plan else {}
    id_column_key = plan["idColumn"]["key"]
    key = "shapefiles/{}_{}.zip".format(place_id,unit_id)

    try:
        data = s3.get_object(Bucket=bucket, Key=key)
        geometries = gpd.read_file(data["Body"])

        geometries['color'] = geometries.apply(lambda row: coloration(row, id_column_key, assignment), axis=1)
        geoplt = geometries.plot(figsize=(2.8, 2.8), color=geometries['color'])

        select = geometries[geometries['color'] != '#555555']
        if 'state' not in plan['place']:
            plan['place']['state'] = plan['placeId']
        if (len(select) > 0) and ((len(select) < len(geometries) / 3) or ((plan['place']['state'].lower().replace(' ', '') not in plan['placeId']) and (plan['placeId'] not in statewide))):
            minx, miny, maxx, maxy = select.total_bounds
            geoplt.set_xlim([minx,maxx])
            geoplt.set_ylim([miny,maxy])
        geoplt.set_axis_off()

        pic_IObytes = io.BytesIO()
        geoplt.figure.savefig(pic_IObytes, format='png')
        
        #pic_IObytes.seek(0)
        #pic_hash = str(base64.b64encode(pic_IObytes.read()))
        #mdb.plans.update_one({ 'simple_id': int(origin) }, { '$set': { 'screenshot2': 'data:image/png;base64,' + pic_hash[2:-1] } })
        
        pic_IObytes.seek(0)
        s3.put_object(Bucket="districtr-public", Key=str(origin) + ".png", ContentType='image/png', Body=pic_IObytes)
        mdb.plans.update_one({ 'simple_id': int(origin) }, { '$set': { 'screenshot2': 'https://districtr-public.s3.us-east-1.amazonaws.com/' + str(origin) + '.png' } })

        plt.close(geoplt.figure)

        return {
            'statusCode': 200,
            'body': 'completed'
        }
    
    except Exception as e:
        print(e)
        print(key)
        raise e
