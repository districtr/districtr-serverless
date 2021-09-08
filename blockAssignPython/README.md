# blockAssign

Given a plan in one set of units return the block assignment file for that plan.

## Subfolders / Scripts 

* `/blockAssignPython/lambda_function.py`: code for AWS Lambda function districtCenter.
    (described above)
* `/blockAssignPythonDataPrep`: subfolder containing python scripts used to generate unit to block
    equivelency json files to be uploaded in the `s3://districtr/block_assign` bucket.

## Dependencies
* Resources:
    * Json file objects in `s3://districtr/block_assign`.  Dictonary of unit GEOIDs mapped the list
    of block GEOIDs that are contained within the unit.

### What places/units are supported

* Blockgroups 2010 - All states
* Blockgroups 2020 - All states
* VTDs 2020 - All modules
