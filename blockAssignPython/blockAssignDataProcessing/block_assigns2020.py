from local_tools import decennial_scraper
from local_tools import states
import requests
import io
import zipfile
import pandas as pd
from states import STATES
import geopandas as gpd
from glob import glob
import json

def download_extract_zip(url, filename):
    """
    Download a ZIP file and extract its contents in memory
    yields (filename, file-like object) pairs
    """
    response = requests.get(url)
    with zipfile.ZipFile(io.BytesIO(response.content)) as thezip:
        with thezip.open(filename) as thefile:
            yield thefile

postal_to_name = {v: k.lower().replace(" ", "_") for k, v in states.name_postal_code_mappings.items()}


for code, st in STATES.items():
    print("{} - {}".format(code, st["STFIPS"]))
    url = "https://www2.census.gov/geo/docs/maps-data/data/baf2020/BlockAssign_ST{}_{}.zip".format(st["STFIPS"],code)
    filename = "BlockAssign_ST{}_{}_CD.txt".format(st["STFIPS"],code)
    for f in download_extract_zip(url, filename):
        df = pd.read_csv(f, delimiter="|", dtype=str)

    df["blockgroup"] = df.BLOCKID.apply(lambda s: s[:-3])
    mappings = {bg: [] for bg in df.blockgroup.unique()}

    for i, row in df.iterrows():
        blocks = mappings[row.blockgroup]
        blocks.append(row.BLOCKID)

    with open("block_lists/{}_blockgroups20.json".format(postal_to_name[code]), "w") as fout:
        json.dump(mappings, fout, indent=2)




for code, st in STATES.items():
    print("{} - {}".format(code, st["STFIPS"]))
    url = "https://www2.census.gov/geo/docs/maps-data/data/baf2020/BlockAssign_ST{}_{}.zip".format(st["STFIPS"],code)
    filename = "BlockAssign_ST{}_{}_VTD.txt".format(st["STFIPS"],code)
    try:
        for f in download_extract_zip(url, filename):
            df = pd.read_csv(f, delimiter="|", dtype=str)
        df["vtds"] = st["STFIPS"] + df.COUNTYFP + df.DISTRICT
        mappings = {bg: [] for bg in df.vtds.unique()}

        for i, row in df.iterrows():
            blocks = mappings[row.vtds]
            blocks.append(row.BLOCKID)

        with open("block_lists/{}_vtds20.json".format(postal_to_name[code]), "w") as fout:
            json.dump(mappings, fout, indent=2)
    except:
        print("No VTDs found")


gdf = gpd.read_file("/Users/jnmatthews/Downloads/nm-precincts-main/nm_precincts.shp")
gdf = gdf.set_index("VTDID")


blks = pd.read_csv("/Users/jnmatthews/Downloads/nm-precincts-main/NM VTD Block Assign FINAL 20210812.csv")

mappings = {gdf.loc[vtd].GEOID20: [] for vtd in blks["VTDID"].unique()}

for i, row in blks.iterrows():
    vtd = row["VTDID"]
    blocks = mappings[gdf.loc[vtd].GEOID20]
    blocks.append(str(row.Block))

with open("block_lists/{}_precincts.json".format("new_mexico"), "w") as fout:
            json.dump(mappings, fout, indent=2)