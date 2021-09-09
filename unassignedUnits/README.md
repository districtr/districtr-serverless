# unassignedUnits

Given a plan assignement return the conected componets of the unassigned units

## Subfolders / Scripts

* `lambda_function.py`: script containing code for lambda invokation.

## Dependencies
* Lambda Layers
    * Graphs v1
* Resources:
    * Json dualgraph objects in `s3://districtr/dual_graphs`.  Node ids should match districtr unit
      id column.  Only node ids and adjacencies are needed.

### What places/units are supported

* Blockgroups 2010 - All states
* Blockgroups 2020 - All states
* VTDs 2020 - All modules
