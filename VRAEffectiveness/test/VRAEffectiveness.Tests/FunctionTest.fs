namespace VRAEffectiveness.Tests


open Xunit
open Amazon.Lambda.TestUtilities
open Amazon.Lambda.APIGatewayEvents

open VRAEffectivenessLambda


module FunctionTest =
    [<Fact>]
    let ``Invoke ToUpper Lambda Function``() =
        // Invoke the lambda function and confirm the string was upper cased.
        let lambdaFunction = Function()
        // let request = APIGatewayProxyRequest()
        let context = TestLambdaContext()
        let testInput ="{\"state\": \"Texas\",\"precID\": \"CNTYVTD\",\"assignment\": {\"30001\": 1,\"30002\": 1,\"30003\": 1, \"30004\": 1,\"90001\": 1,\"90002\": 1,\"90003\": 1,\"90004\": 1,\"90005\": 1,\"90006\": 1,\"90007\": 1,\"90008\": 1,\"90009\": 1, \"90010\": 1, \"90011\": 1, \"110101\": 0,\"110201\": 0, \"110202\": 0, \"110301\": 0, \"110303\": 0, \"110401\": 0}}"        // let request = new APIGatewayProxyRequest({Body= testInput})
        let upperCase = lambdaFunction.FunctionHandler testInput context
        let expectation = "/Users/smaug/Documents/MGGG/districtr-serverless/VRAEffectiveness/src/VRAEffectiveness/texas.json"
        Assert.Equal(expectation, upperCase)


    [<Fact>]
    let ``Trial``() =
        // printfn "%s" <| Function.executingAssembly
        // printfn "%s" <| Function.executingAssemblyDir
        
        Assert.True <| true

    [<EntryPoint>]
    let main _ = 0
