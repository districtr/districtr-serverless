# planThumbnail

Given a district plan id, generate a png thumbnail and update it's record in the database.

## Subfolders  / Scripts

* `/lambda_function`: code for AWS Lambda function. (described above)

## Dependencies
* Lambda Layers
    * DataWrangling v1
    * DistrictrDB v1
    * Plotting v1
* Resources:
    * Zip file objects in `s3://districtr/shapefiles` which are compressed version of the shapefile
    used to upload the module to districtr.  Should at least contain columns for unit_id and
    geometries.  The zip object should not be nested; all five pieces of the shapefile should be a
    root level of the zip object.

### What places/units are supported

* Blockgroups 2020 - All states
* VTDs 2020 - All modules
