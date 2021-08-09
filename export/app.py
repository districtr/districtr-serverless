import json
import tempfile
import os
import shutil
import geopandas as gpd
import boto3
from flask import request
import flask
import botocore.exceptions
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)


s3 = boto3.client("s3")
session = boto3.Session()


def generate_shapefile_uri(plan: dict) -> str:
    """
    Generates the s3 key from a districtr plan object.
    """
    with open("config.json") as f:
        config = json.loads("".join([x.split("#")[0] for x in f]))

    state = plan["placeId"]
    shapefile_code = state

    if plan["units"]["id"] == "blockgroups" and "_bg" not in shapefile_code:
        shapefile_code += "_bg"
    elif plan["units"]["id"] == "blocks" and state in ["elpasotx"]:
        shapefile_code += "_b"

    if plan["units"]["id"] == "precincts_02_10":
        shapefile_code += "_02"
    elif plan["units"]["id"] == "precincts_12_16":
        shapefile_code += "_12"

    return config[shapefile_code]


def fetch_shapefile(shapefile_uri: str, dir_prefix="/tmp/"):
    """
    Fetch a given shapefile and metadata from S3
    """
    folder = dir_prefix + "/".join(shapefile_uri.split("/")[:-1])
    if not os.path.isdir(folder):
        os.makedirs(folder)

    for endings in [
        ".shp",
        ".shp.xml",
        ".shx",
        ".dbf",
        ".prj",
        ".cpg",
    ]:  # TODO: return error if does not exist
        filename = shapefile_uri + endings
        if not os.path.isfile(filename):
            try:
                s3.download_file("districtr", filename, dir_prefix + filename)
            except botocore.exceptions.ClientError:  # TODO: log this properly
                print(filename)

    return gpd.read_file(dir_prefix + shapefile_uri + ".shp")


def create_export(
    shp: gpd.GeoDataFrame, name: str, ending=".shp", driver="ESRI Shapefile"
):
    """
    Creates shapefile export from GeoDataFrame
    """
    tempdir = tempfile.TemporaryDirectory()
    shp.to_file(f"{tempdir.name}/{name}{ending}", driver=driver)
    shp_archive = shutil.make_archive(f"/tmp/{name}", "zip", tempdir.name)
    return flask.send_file(shp_archive, as_attachment=True)


@app.route("/export", methods=["POST"])
@app.route("/export/<export_format>", methods=["POST"])
@app.route("/export/<export_format>/<full>", methods=["POST"])
def export(export_format="ESRI Shapefile", full=False):
    """
    Exports a districtr json object using the specified driver
    """
    plan = request.get_json()
    coi_mode = ("type" in plan["problem"]) and (plan["problem"]["type"] == "community")

    shapefile_uri = generate_shapefile_uri(plan)
    shp = fetch_shapefile(shapefile_uri)
    assignment = {
        k[0]: v if isinstance(k, list) else k for k, v in plan["assignment"].items()
    }

    if coi_mode:  # coi_mode will return a partial map of the state
        shp = shp[assignment.keys()]

    # The shapefile will default to -1 if unassigned
    idColumn = plan["idColumn"]["key"]
    shp["districtr"] = shp[idColumn].apply(lambda x: assignment.get(x, -1))

    filename = plan["id"] + "-export"
    if export_format.lower() == "geojson":
        driver = "GeoJSON"
        ending = ".geojson"
    elif export_format.lower() == "gpkg":
        driver = "GPKG"
        ending = ".gpkg"
    else:
        driver = "ESRI Shapefile"
        ending = ".shp"

    if full:
        return create_export(shp, filename, ending=ending, driver=driver)
    else:
        return create_export(
            shp[[idColumn, "districtr", "geometry"]],
            filename,
            ending=ending,
            driver=driver,
        )
