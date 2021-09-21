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
      id column.  Only node ids, area, perimeter, and adjacencies are needed. The `COUNTY` column is
      optional, but requried for county split information and more detailed breakdown.  If included
      the county column should contain the three digit county fips code for the county in that state.
    * `resources/county_totpop_2020.json`: Json object mapping each state name to a dictionary that
      maps each county's fips code to it's name and total population.