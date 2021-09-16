# localElectionDetails

Given a plan return details of how the districts in the place preformed with respect to various 
local/regional elections.

## Subfolders / Scripts 

* `localElectionDetails/lambda_function.py`: code for AWS Lambda function localElectionDetails. (described above)
* `localElectionDetails/resources`: subfolder containing Json/CSV files with election details for each state.
    * `${state_name}.json`: Defines elections, minority groups, and their candidates of choice.
    * `${state_name}.csv`: Tabular election and demographic data by precinct.
    * `${state_name}_ei.csv`: EI support for each candidate by demographic group.

## Dependencies
* Lambda Layers
    * DataWrangling v1

### What places/units are supported

* VRA Dashboard modules
    * Massachusetts