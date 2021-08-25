import pandas as pd
from local_tools import states
from states import STATES
import geopandas as gpd
from glob import glob
from gerrychain import Graph

postal_to_name = {v: k.lower().replace(" ", "_") for k, v in states.name_postal_code_mappings.items()}


for code, st in list(STATES.items())[13:]:
    print("{} - {}".format(code, st["STFIPS"]))
    bg_shapes = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2010/BG/2010/tl_2010_{}_bg10.zip".format(st["STFIPS"]))
    bg_shapes = bg_shapes.rename(columns={"GEOID10": "GEOID"})
    bg_shapes = bg_shapes[["GEOID", "geometry"]].set_index("GEOID")
    graph = Graph.from_geodataframe(bg_shapes)
    graph.to_json("../districtContiguity/graphs/{}_blockgroups.json".format(postal_to_name[code]))
    # bg_shapes.to_csv("../districtCenter/resources/{}_blockgroups.csv".format(postal_to_name[code]), index=False)

for code, st in [("IA", STATES["IA"])]:
    print("{} - {}".format(code, st["STFIPS"]))
    cnty_shapes = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_{}_county10.zip".format(st["STFIPS"]))
    cnty_shapes = cnty_shapes.rename(columns={"GEOID10": "GEOID"})
    cnty_shapes = cnty_shapes[["GEOID", "geometry"]].set_index("GEOID")
    graph = Graph.from_geodataframe(cnty_shapes)
    graph.to_json("../districtContiguity/graphs/{}_counties.json".format(postal_to_name[code]))
    # cnty_shapes.to_csv("../districtCenter/resources/{}_counties.csv".format(postal_to_name[code]), index=False)
