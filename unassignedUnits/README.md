# unassignedUnits

Given a plan assignment key list, return the largest network-connected block of unassigned units as a lat/lng bounding box

## Subfolders / Scripts

* `lambda_function.py`: script containing code for lambda invokation.

## Dependencies
* Lambda Layers
    * Graphs v1
    * Data Wrangling v1
* Resources:
    * Json dualgraph objects in `s3://districtr/dual_graphs`.  Node ids should match districtr unit
      id column.  Only node ids and adjacencies are needed.
    * District centroids in `s3://districtr/centroids`

### What places/units are supported

* Blockgroups 2010 - All states
* Blockgroups 2020 - All states
* VTDs 2020 - All modules
