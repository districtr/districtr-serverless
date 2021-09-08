# districtContiguity

Given a set of unit ids that make up a district return whether or not that districts is represents
a contiguious region.

## Subfolders / Scripts

* `/districtContiguity`: subfolder containing python code for AWS Lambda function districtCenter.
    (described above)
    * `lambda_function.py`: script containing code for lambda invokation.
* `/districtContiguityDataPrep`: subfolder containing python scripts used to generate Json dualgraph
    objects to be uploaded to the `s3://districtr/dual_graphs` bucket.

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
