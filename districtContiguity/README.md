# districtContiguity

Given a set of unit ids that make up a district return whether or not that districts is represents a contiguious region.

## Subfolders 

* `/districtContiguity`: subfolder containing python code / dependencies for AWS Lambda function districtCenter. (described above)
    * `/districtContiguity/package`: zips of dependecies for lambda function.
* `/districtContiguityDataPrep`: subfolder containing python scripts used to generate Json dualgraph objects to be uploaded to the `s3://districtr/dual_graphs` bucket.


### What places/units are included

* Blockgroups 2010 - All states
* Blockgroups 2020 - All states
* VTDs 2020 - All modules