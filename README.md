# districtr-serverless

District backend functionality using AWS Lambda

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