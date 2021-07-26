from local_tools import decennial_scraper
from local_tools import states
import requests
import pandas as pd
import json
import urllib




for state in states.district_states:
    parsed_name = state.lower().replace(" ", "_")
    print(parsed_name)
    url_suffix = urllib.parse.quote("{}.zip".format(state))
    df = pd.read_csv("https://transition.fcc.gov/form477/Geo/CensusBlockData/CSVFiles/{}".format(url_suffix), 
                     dtype=str)
    df["blockgroup"] = df.blockcode.apply(lambda s: s[:-3])
    mappings = {bg: [] for bg in df.blockgroup.unique()}

    for i, row in df.iterrows():
        blocks = mappings[row.blockgroup]
        blocks.append(row.blockcode)

    with open("block_lists/{}_blockgroups.json".format(parsed_name), "w") as fout:
        json.dump(mappings, fout, indent=2)


# Need to redo new mexico, northern_mariana_islands, puerto rico, manually; 
# wrong encoding / spelling doesn't match
for state in ["New Mexico", "Puerto Rico"]:
    parsed_name = state.lower().replace(" ", "_")
    print(parsed_name)
    df = pd.read_csv("~/Downloads/{}.csv".format(state),dtype=str)
    df["blockgroup"] = df.blockcode.apply(lambda s: s[:-3])
    mappings = {bg: [] for bg in df.blockgroup.unique()}

    for i, row in df.iterrows():
        blocks = mappings[row.blockgroup]
        blocks.append(row.blockcode)

    with open("block_lists/{}_blockgroups.json".format(parsed_name), "w") as fout:
        json.dump(mappings, fout, indent=2)