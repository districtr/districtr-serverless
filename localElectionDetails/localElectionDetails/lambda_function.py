import json
import pandas as pd


def get_district_details(dist_asignment, group, state_details, ei_data, other_col="Other"):
    elections = []
    for e in state_details["local_elections"]:
        name = e["name"]
        coc  = e["coc"][group]
        cands = e["cands"]

        cvap_col = state_details["cvap_col"][str(e["year"])]
        vap_col = state_details["vap_col"][str(e["year"])]
        group_cvap_col = state_details["minorities"][group]["cvap_col"][str(e["year"])]
        group_vap_col = state_details["minorities"][group]["vap_col"][str(e["year"])]
        
        coc_support = dist_asignment[coc].sum()
        tot_turout = dist_asignment[cands].sum().sum()
        tot_pop = dist_asignment["TOTPOP"].sum()
        tot_cvap = dist_asignment[cvap_col].sum()
        outside_elect_terrain = dist_asignment[dist_asignment[coc].isna()]
        outside_elect_terrain_group_vap = outside_elect_terrain[group_vap_col].sum()
        outside_elect_terrain_total_vap = outside_elect_terrain[vap_col].sum()
        outside_elect_terrain_non_group_vap = outside_elect_terrain_total_vap - outside_elect_terrain_group_vap

        coc_proj_vote = ei_data[coc][group] * outside_elect_terrain_group_vap + ei_data[coc][other_col] * outside_elect_terrain_non_group_vap
        proj_turout = ei_data[cands].sum(axis=1)
        total_proj_vote = proj_turout[group] * outside_elect_terrain_group_vap + proj_turout[other_col] * outside_elect_terrain_non_group_vap

        elect = {
            "Name": name,
            "CoC": coc,
            "CoCPerc": coc_support / tot_turout if coc_support != 0 else 0,
            "GroupControl": dist_asignment[group_cvap_col].sum() / tot_cvap if tot_cvap != 0 else 0,
            "ElectionOverlap": dist_asignment.dropna(subset=[coc])["TOTPOP"].sum() / tot_pop if tot_pop != 0 else 0,
            "ProjectedCoCPerc": (coc_support + coc_proj_vote) / (tot_turout + total_proj_vote) if tot_pop != 0 else 0
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
        ei_info = pd.read_csv("resources/{}_ei.csv".format(state)).set_index("Race")
        elections["District"] = elections[precID].map(assignment)
        assigned_units = elections.dropna(subset=["District"])
        return {
            'statusCode': 200,
            'body': json.dumps({
                    group: {dist: get_district_details(assigned_units.query("District == @dist"),
                                                       group,
                                                       election_detials,
                                                       ei_info,
                                                       "Other") for dist in set(assignment.values())}
                                    for group in groups
                })
        }
    except Exception as e:
        print(e)
        raise e
    