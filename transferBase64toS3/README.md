# transferBase64toS3

Given a district plan id, 
load the base64-encoded string version of the image from the database,
 convert to binary data,
 and store the binary in a public S3 bucket.

## Subfolders  / Scripts

* `/lambda_function`: code for AWS Lambda function transferBase64toS3. (described above)

## Dependencies
* Lambda Layers
    * DataWrangling v1
    * DistrictrDB v1

### What places/units are supported

* Any previously stored plan thumbnail
