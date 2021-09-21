import json
import pandas as pd


def get_district_details(dist_asignment, group, state_details, ei_data, other_col="Other"):
    elections = []
    for e in state_details["local_elections"]:
        name = e["name"]
        coc  = e["coc"][group]
        cands = e["cands"]
        ei_groups = list(state_details["groups"].keys())

        cvap_col = state_details["cvap_col"][str(e["year"])]
        vap_col = state_details["vap_col"][str(e["year"])]
        pop_key = state_details["pop_col"]
        tot_pop = dist_asignment[pop_key].sum()
        group_cvap_col = state_details["groups"][group]["cvap_col"][str(e["year"])]
        
        coc_support = dist_asignment[coc].sum()
        tot_turout = dist_asignment[cands].sum().sum()

        
        group_vap_cols = [state_details["groups"][group]["vap_col"][str(e["year"])] for group in ei_groups]

        outside_elect_terrain = dist_asignment[~dist_asignment[cands].any(axis="columns")]
        outside_elect_terrain_group_vaps = [outside_elect_terrain[group_vap_col].sum() for group_vap_col in group_vap_cols]
        outside_elect_terrain_total_vap = outside_elect_terrain[vap_col].sum()
        outside_elect_terrain_non_group_vap = outside_elect_terrain_total_vap - sum(outside_elect_terrain_group_vaps)


        outside_elect_terrain_vap_by_group = list(zip(ei_groups, outside_elect_terrain_group_vaps))

        coc_proj_vote = sum([ei_data[coc][group] * outside_elect_terrain_group_vap 
                            for (group,outside_elect_terrain_group_vap) in outside_elect_terrain_vap_by_group]) \
                         + ei_data[coc][other_col] * outside_elect_terrain_non_group_vap
        proj_turout = ei_data[cands].sum(axis=1)
        total_proj_vote = sum([proj_turout[group] * outside_elect_terrain_group_vap
                                for (group,outside_elect_terrain_group_vap) in outside_elect_terrain_vap_by_group]) \
                           + proj_turout[other_col] * outside_elect_terrain_non_group_vap
        
        # Calculate supports.
        coc_perc = coc_support/tot_turout if coc_support != 0 else 0
        projected_coc_perc = (coc_support+coc_proj_vote) / (tot_turout+total_proj_vote) if (tot_turout+total_proj_vote) != 0 else 0

        elect = {
            "Name": name,
            "CoC": coc,
            "CoCPerc": coc_perc,
            "GroupControl": dist_asignment[group_cvap_col].sum() / dist_asignment[cvap_col].sum(),
            "ElectionOverlap": dist_asignment[dist_asignment[cands].any(axis="columns")][pop_key].sum() / tot_pop,
            "ProjectedCoCPerc": projected_coc_perc
        }
        elections.append(elect)

    return {"ElectionDetails": elections}


def lambda_handler(event, context):
   
    if 'body' in event.keys():
        event = json.loads(event["body"])
    state = event["state"].lower().replace(" ", "_")
    assignment = event["assignment"]
    # groups = event["groups"]
    precID = event["precID"]
    places = event["places"]

    try:
        # data = s3.get_object(Bucket=bucket, Key=key)
        elections = pd.read_csv("resources/{}.csv".format(state))
        response = {}
        for place in places:
            place_name = place["name"]
            place_key = place["key"]
            groups = place["groups"]
            with open("resources/{}-{}.json".format(state,place_key)) as fin:
                election_detials = json.load(fin)
            ei_info = pd.read_csv("resources/{}-{}_ei.csv".format(state,place_key)).set_index("Race")
            elections["District"] = elections[precID].map(assignment)
            assigned_units = elections.dropna(subset=["District"])

            response[place_name] = {
                group: {dist: get_district_details(assigned_units.query("District == @dist"),
                                                    group,
                                                    election_detials,
                                                    ei_info,
                                                    "Other") for dist in set(assignment.values())}
                                for group in groups
            }
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
    except Exception as e:
        print(e)
        raise e
    