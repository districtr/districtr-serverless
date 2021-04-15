# AWS Lambda VRAEffectiveness Project

This starter project consists of:
* Function.fs - Code file containing the function handler method
* aws-lambda-tools-defaults.json - default argument settings for use with Visual Studio and command line deployment tools for AWS
* VRAEffectiveness.fs - Code file containing representation of VRAEffectiveness score and summary details.

## VRA Effectiveness Score

* The alignment is 2 * (CVAP Share) clamped at 1.  The CVAP share for an election is based on the 5-year ACS where the election is central to the data (when possible.)  A table mapping election years to ACS release is shown below.


|Election Year  |ACS Release  |
|---------|-----------|
|2012     | 2010-2014 |
|2014     | 2012-2016 |
|2015     | 2013-2017 |
|2016     | 2014-2018 |
|2017     | 2015-2019 |
|2018     | 2015-2019 |
|2019     | 2015-2019 |



## Here are some steps to follow from Visual Studio:

To deploy your function to AWS Lambda, right click the project in Solution Explorer and select *Publish to AWS Lambda*.

To view your deployed function open its Function View window by double-clicking the function name shown beneath the AWS Lambda node in the AWS Explorer tree.

To perform testing against your deployed function use the Test Invoke tab in the opened Function View window.

To configure event sources for your deployed function, for example to have your function invoked when an object is created in an Amazon S3 bucket, use the Event Sources tab in the opened Function View window.

To update the runtime configuration of your deployed function use the Configuration tab in the opened Function View window.

To view execution logs of invocations of your function use the Logs tab in the opened Function View window.

## Here are some steps to follow to get started from the command line:

Once you have edited your template and code you can deploy your application using the [Amazon.Lambda.Tools Global Tool](https://github.com/aws/aws-extensions-for-dotnet-cli#aws-lambda-amazonlambdatools) from the command line.

Install Amazon.Lambda.Tools Global Tools if not already installed.
```
    dotnet tool install -g Amazon.Lambda.Tools
```

If already installed check if new version is available.
```
    dotnet tool update -g Amazon.Lambda.Tools
```

Execute unit tests
```
    cd "VRAEffectiveness/test/VRAEffectiveness.Tests"
    dotnet test
```

Deploy function to AWS Lambda
```
    cd "VRAEffectiveness/src/VRAEffectiveness"
    dotnet lambda deploy-function
```
