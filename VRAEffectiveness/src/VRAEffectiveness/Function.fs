namespace VRAEffectivenessLambda
open Amazon.Lambda.Core
open Amazon.Lambda.APIGatewayEvents
// open Amazon.Lambda.Serialization
open FSharp.Data
open Deedle
open VRAEffectiveness
open Newtonsoft.Json



// Assembly attribute to enable the Lambda function's JSON input to be converted into a .NET class.
[<assembly: LambdaSerializer(typeof<Amazon.Lambda.Serialization.SystemTextJson.DefaultLambdaJsonSerializer>)>]
()

type Response = 
    {
        Data: PlanVRASummary<int>
        SeqID: int
    }

type Function() =
    let (+/) path path' = System.IO.Path.Combine(path, path')
    let PathCombine path path' path'' = System.IO.Path.Combine(path, path', path'')

    let StateSuccessFunction: Map<string, SuccessFunction<string>> = Map.ofArray [|"texas", CoCCarriesElectTX; 
                                                                                   "louisiana", CoCCarriesElectLA;
                                                                                   "massachusetts", CoCCarriesElectPlurality|]

    static member executingAssembly = System.Reflection.Assembly.GetExecutingAssembly().Location
    static member executingAssemblyDir = System.IO.Path.GetDirectoryName Function.executingAssembly

    /// <summary>
    /// A simple function that takes a string and does a ToUpper
    /// </summary>
    /// <param name="input"></param>
    /// <returns></returns>
    member __.FunctionHandler (input: APIGatewayProxyRequest) (_: ILambdaContext) =
        // unpack request
        let request = JsonValue.Parse(input.Body)
        let stateName = request.["state"].AsString().ToLower().Replace(" ", "_")
        let PrecinctID = request.["precID"].AsString()
        let requestID = request.["SeqID"].AsInteger()
        let districtID = "District"
        let assignment = request.["assignment"].Properties() |> Array.map (fun (a,b) -> a,b.AsInteger())

        let JsonFile = sprintf "%s.json" <| stateName |> PathCombine Function.executingAssemblyDir "resources"
        let CsvFile = sprintf "%s.csv" <| stateName |> PathCombine Function.executingAssemblyDir "resources"
        
        let JsonValue = JsonValue.Load(JsonFile)
        let StateData = Frame.ReadCsv(CsvFile) |> Frame.indexRowsString PrecinctID
        let PlanData = StateData |> Frame.addCol districtID (assignment |> Series.ofObservations)

        let VRAparser = Parser JsonValue
        let Minorities = VRAparser.Minorities
        let Elections = VRAparser.Elections
        let AlignmentYear = VRAparser.AlignmentYear
        let CoCSuccess = StateSuccessFunction.[stateName]
        
        let vrascores: PlanVRASummary<int> = PlanVRAEffectivenessDetailed PlanData districtID Minorities Elections CoCSuccess AlignmentYear
        
        JsonConvert.SerializeObject {SeqID = requestID; Data=vrascores}