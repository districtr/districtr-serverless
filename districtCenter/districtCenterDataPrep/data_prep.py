import pandas as pd
from local_tools import states
from states import STATES
import geopandas as gpd
from glob import glob


postal_to_name = {v: k.lower().replace(" ", "_") for k, v in states.name_postal_code_mappings.items()}


for code, st in STATES.items():
    print("{} - {}".format(code, st["STFIPS"]))
    bg_shapes = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2010/BG/2010/tl_2010_{}_bg10.zip".format(st["STFIPS"]))
    bg_shapes.INTPTLAT10 = bg_shapes.INTPTLAT10.astype(float)
    bg_shapes.INTPTLON10 = bg_shapes.INTPTLON10.astype(float)
    bg_shapes = bg_shapes.rename(columns={"GEOID10": "GEOID", "INTPTLAT10": "LAT", "INTPTLON10": "LNG"})
    bg_shapes = bg_shapes[["GEOID", "LAT", "LNG"]]
    # graph = Graph.from_geodataframe(bg_shapes)
    bg_shapes.to_csv("../districtCenter/resources/{}_blockgroups.csv".format(postal_to_name[code]), index=False)

for code, st in [("IA", STATES["IA"])]:
    print("{} - {}".format(code, st["STFIPS"]))
    bg_shapes = gpd.read_file("https://www2.census.gov/geo/tiger/TIGER2010/COUNTY/2010/tl_2010_{}_county10.zip".format(st["STFIPS"]))
    bg_shapes.INTPTLAT10 = bg_shapes.INTPTLAT10.astype(float)
    bg_shapes.INTPTLON10 = bg_shapes.INTPTLON10.astype(float)
    bg_shapes = bg_shapes.rename(columns={"GEOID10": "GEOID", "INTPTLAT10": "LAT", "INTPTLON10": "LNG"})
    bg_shapes = bg_shapes[["GEOID", "LAT", "LNG"]]
    # graph = Graph.from_geodataframe(bg_shapes)
    bg_shapes.to_csv("../districtCenter/resources/{}_counties.csv".format(postal_to_name[code]), index=False)


## Read in local districtr-shapefiles

LOCAL_PATH = "/Users/jnmatthews/MGGG/districtr_data/*"

id_cols = {"alaska": "ID", "ohio": "PRECODE", 
           "wisconsin": "Code-2", "michigan": "VTD", "texas": "CNTYVTD", 
           "pennsylvania": "GEOID10", "new_mexico": "NAME10",
           "minnesota": "VTDID", "utah": "DsslvID", "louisiana": "GEOID10",
           "massachusetts": "NAME"}

place_dirs = glob(LOCAL_PATH)
for place in place_dirs[1:]:
    name = place[38:]
    print(name)
    id_col = id_cols[name]
    shp_file = glob("{}/*.shp".format(place))[0]
    df = gpd.read_file(shp_file).to_crs("EPSG:4326")
    df["CENTROID"] = df.geometry.centroid
    df["LAT"] = df.CENTROID.apply(lambda p: p.y)
    df["LNG"] = df.CENTROID.apply(lambda p: p.x)
    
    df[[id_col, "LAT", "LNG"]].rename(columns={id_col: "GEOID"}).to_csv("../districtCenter/resources/{}_precincts.csv".format(name), index=False)



