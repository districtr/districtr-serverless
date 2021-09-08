# districtr-serverless

District backend functionality using AWS Lambda

## Repo Structure

Each directory corresponds to a single lambda function.  It should contain a copy of the code/
resources uploaded to AWS (if written in python, the main function should be called
`lambda_function.py` and any external file dependecies should live in a `resources` folder.). The
directory should also contain additional script used to generate resource dependencies (whether they
live on s3 or in the `resources` folder) as well as a `README.md` documenting: the function; the
scripts/files in the directory; and which AWS Lambda Layers (if any) the function depends on.

## Dependencies

Common groups of dependencies are shared via layers.  To use them in your lambda function add the
layers with the dependicies you need via the AWS Lambda console.

Existing Layers:
* DataWrangling:
    * pandas
    * numpy
    * geopandas
* Graphs
    * networkx
* Plotting
    * matplotlib
* DistrictrDB
    * pymongo

## Contribution Workflow

New functions should be created in a new branch, with a structure as defined above.  When they are
ready for review a Pull Request should be created against the main branch and reviewed.  All code
merged in should have clear documentation and match our existing developement style and structure
(both in code and internal/external dependencies).
