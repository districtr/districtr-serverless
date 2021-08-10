import json
import pandas as pd

# import boto3


def get_district_details(dist_asignment, group, state_details):
    elections = []
    for e in state_details["local_elections"]:
        name = e["name"]
        coc  = e["coc"][group]
        cvap_col = state_details["cvap_col"][str(e["year"])]
        group_cvap_col = state_details["minorities"][group]["cvap_col"][str(e["year"])]
        cands = e["cands"]
        coc_support = dist_asignment[coc].sum()
        
        elect = {
            "Name": name,
            "CoC": coc,
            "CoCPerc": coc_support / dist_asignment[cands].sum().sum() if coc_support != 0 else 0,
            "GroupControl": dist_asignment[group_cvap_col].sum() / dist_asignment[cvap_col].sum(),
            "ElectionOverlap": dist_asignment.dropna(subset=[coc])["TOTPOP"].sum() / dist_asignment["TOTPOP"].sum()
        }
        elections.append(elect)

    return {"ElectionDetails": elections}


def lambda_handler(event, context):
   
    if 'body' in event.keys():
        event = json.loads(event["body"])
    state = event["state"].lower().replace(" ", "_")
    assignment = event["assignment"]
    groups = event["groups"]
    precID = event["precID"]

    try:
        # data = s3.get_object(Bucket=bucket, Key=key)
        elections = pd.read_csv("resources/{}.csv".format(state))
        with open("resources/{}.json".format(state)) as fin:
            election_detials = json.load(fin)
        elections["District"] = elections[precID].map(assignment)
        assigned_units = elections.dropna(subset=["District"])
        return {
            'statusCode': 200,
            'body': json.dumps({
                    group: {dist: get_district_details(assigned_units.query("District == @dist"),
                                                       group,
                                                       election_detials) for dist in set(assignment.values())} for group in groups
                })
        }
    except Exception as e:
        print(e)
        raise e
    