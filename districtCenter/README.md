# districtCenter

Given a set of unit ids that make up a district return the coordinate point (longitude, latitude) of the centroid of the unit closest the the center of mass of the units.

## Subfolders 

* `/districtCenter`: subfolder containing python code / dependencies for AWS Lambda function districtCenter. (described above)
    * `/districtCenter/package`: zips of dependecies for lambda function.
* `/districtCenterDataPrep`: subfolder containing python scripts used to generate CSVs to be uploaded in `s3://districtr/centroids` bucket.


### What places/units are included

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