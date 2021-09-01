import pandas as pd
import json
import geopandas as gpd

files = [
    "Boston Elections - 1st Suffolk State Senate District Primary 2013.csv",
    "Boston Elections - 2nd Suffolk State Senate District Primary 2008.csv",
    "Boston Elections - 7th Congressional District Primary 2018.csv",
    "Boston Elections - 11th Suffolk State House District Primary 2016.csv",
    "Boston Elections - 11th Suffolk State House District Primary 2018.csv",
    "Boston Elections - 12th Suffolk State House District Primary 2016.csv",
    "Boston Elections - 12th Suffolk State House District Primary 2018.csv",
    "Boston Elections - 14th Suffolk State House District Primary 2018.csv",
    "Boston Elections - Mayor's Election 2017.csv"
]

df = pd.DataFrame(columns=["MATCH"])
for f in files:
    elect = pd.read_csv(f)
    df = pd.merge(elect,df, on="MATCH", how="outer")


with open("../localElectionDetails/resources/massachusetts.json", "r") as fin:
    ma = json.load(fin)

cands = ["MATCH"]
for elect in ma["local_elections"]:
    cands += elect["cands"]

df = df[cands].rename(columns={"MATCH": "NAME"})

ma_full = gpd.read_file("/Users/jnmatthews/MGGG/VRA-data-products/Massachusetts/shapes/MA_pcts.shp")

ma_cvap = gpd.read_file("/Users/jnmatthews/MGGG/districtr-serverless/VRAEffectiveness/src/VRAEffectiveness/resources/massachusetts.csv")

cvaps = ["CVAP{}".format(year) for year in [14,16,17,18]]
bcvaps = ["BCVAP{}".format(year) for year in [14,16,17,18]]
df.to_csv("../localElectionDetails/resources/massachusetts.csv", index=False)

df = pd.read_csv("../localElectionDetails/resources/massachusetts.csv")

ma_full[["NAME", "TOTPOP", "VAP",]]

ma_pop = pd.merge(df, ma_full[["NAME", "TOTPOP"]], on="NAME", how="outer")


ma_pop = pd.merge(ma_full[["NAME", "TOTPOP"]], ma_cvap[["NAME"] + cvaps + bcvaps], on="NAME", how="outer")

pd.merge(df, ma_pop, on="NAME", how="outer").to_csv("../localElectionDetails/resources/massachusetts.csv", index=False)

ma_full[["NAME", "VAP", "BVAP"]].rename(columns={"VAP": "VAP10", "BVAP": "BVAP10"})

pd.merge(df, ma_full[["NAME", "VAP", "BVAP"]], on="NAME", how="outer").to_csv("../localElectionDetails/resources/massachusetts.csv", index=False)

df = pd.read_csv("../localElectionDetails/resources/massachusetts.csv")

df_old = pd.read_csv("../localElectionDetails/resources/massachusetts_old.csv")

# df_old[["NAME", "TOTPOP"]]

# pd.merge(df, df_old[["NAME", "TOTPOP"]], on="NAME").drop(columns=["Unnamed: 0"]).to_csv("../localElectionDetails/resources/massachusetts.csv", index=False)

cols = ["NAME", "TOTPOP","VAP10","HVAP10","WVAP10","BVAP10","AMINVAP10","ASIANVAP10","NHPIVAP10","OTHERVAP10","2MOREVAP10"]

df = df.drop(columns=[c for c in df.columns if "CVAP" in c])

df_cvap = df_old[["NAME"] + [c for c in df_old.columns if "CVAP" in c]]

pd.merge(df, df_cvap, on="NAME").to_csv("../localElectionDetails/resources/massachusetts.csv", index=False)



df = pd.read_csv("~/Downloads/WI25.csv", header=0)

df["assignment"] = df["assignment"].apply(lambda x: x+1)

df.to_csv("~/Downloads/WI25.csv", index=False)