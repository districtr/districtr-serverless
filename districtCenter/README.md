# districtCenter

Given a set of unit ids that make up a district return the coordinate point (latitude, longitude) of
the centroid of the unit closest the the center of mass of the units.

## Subfolders / Scripts

* `/districtCenter`: subfolder containing python code for AWS Lambda function districtCenter.
    (described above)
    * `lambda_function.py`: script containing code for lambda invokation.
* `/districtCenterDataPrep`: subfolder containing python scripts used to generate CSVs to be uploaded
    in `s3://districtr/centroids` bucket.

## Dependencies
* Lambda Layers
    * DataWrangling v1
* Resources:
    * CSV files in `s3://districtr/centroids` mapping each unit to the latitude/longitude of its
    centroid.  The columns of the CSVs should be named: `GEOID`, `LAT`, `LNG`.

### What places/units are supported

* Blockgroups 2010 - All states
* Blockgroups 2020 - All states
* VTDs 2020 - All state
* Counties
    * Iowa
* Precincts
    * AK
    * LA
    * MA
    * MI
    * MN
    * NM
    * OH
    * PA
    * TX
    * UT
    * WI
* Blocks
