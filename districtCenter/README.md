# districtCenter

Given a set of unit ids that make up a district return the coordinate point (longitude, latitude) of the centroid of the unit closest the the center of mass of the units.

## Subfolders 

* `/districtCenter`: subfolder containing python code / dependencies for AWS Lambda function districtCenter. (described above)
    * `/districtCenter/package`: zips of dependecies for lambda function.
* `/districtCenterDataPrep`: subfolder containing python scripts used to generate CSVs in `/districtCenter/resources/` folder.


### What places/units are included

* Blockgroups - All states
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