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
        let testInput ="{\"assignment\":{\"2404102-001\":0,\"2404102-002\":0,\"2404105-001\":0},\"state\":\"Maryland\",\"precID\":\"VTD\",\"SeqID\":1,\"alignmentType\":\"CVAP\"}",        // let request = new APIGatewayProxyRequest({Body= testInput})
        let upperCase = lambdaFunction.FunctionHandler testInput context
        let expectation = "/Users/smaug/Documents/MGGG/districtr-serverless/VRAEffectiveness/src/VRAEffectiveness/maryland.json"
        Assert.Equal(expectation, upperCase)


    [<Fact>]
    let ``Trial``() =
        // printfn "%s" <| Function.executingAssembly
        // printfn "%s" <| Function.executingAssemblyDir
        
        Assert.True <| true

    [<EntryPoint>]
    let main _ = 0
