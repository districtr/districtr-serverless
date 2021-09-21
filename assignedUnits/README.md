# assignedUnits

Given a plan assignment key list, return the lat/lng bounding box around their centroids

## Subfolders / Scripts

* `lambda_function.py`: script containing code for lambda invokation.

## Dependencies
* Lambda Layers
    * Data Wrangling v1
* Resources:
    * District centroids in `s3://districtr/centroids`

### What places/units are supported

* Blockgroups 2010 - All states
* Blockgroups 2020 - All states
* VTDs 2020 - All modules
