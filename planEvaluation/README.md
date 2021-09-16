# planEvaluation

Given a plan assignment, return information about how it preforms with respect to compactness
and municipality splits.

## Subfolders  / Scripts

* `/lambda_function`: code for AWS Lambda function districtCenter. (described above)

## Dependencies
* Lambda Layers
    * Graphs v2
* Resources:
    * Json dualgraph objects in `s3://districtr/dual_graphs`.  Node ids should match districtr unit
      id column.  Only node ids, area, perimeter, and adjacencies are needed. `COUNTY`, and `TOTPOP`
      column optional, but requried for county split information and more detailed breakdown.