module VRAEffectiveness
open FSharp.Data
open Deedle
open MathNet.Numerics.LinearAlgebra

type MinorityGroup = HISPANIC | BLACK | ASIAN | AMIN | NEITHER

type Column = string

module Minority = 
    type Name = MinorityGroup
    type MinCVAPCol = Column
    type TotCVAPCol = Column
    type Minority = Name * MinCVAPCol * TotCVAPCol


type District<'a when 'a : equality> = Frame<'a, Column>

type Election(cands: Column array) = 
    let candidates = cands

    /// <summary>
    /// Get vote share for candidates in the election.
    /// </summary>
    /// <param name="districtData"> Frame where each row is a precinct within the district and contains
    /// candidate columns.
    /// </param>
    /// <returns> Series of candidates and their vote share.  </returns>
    member this.VoteShares (districtData: District<'a>) = 
        let voteCounts = districtData |> Frame.sliceCols cands
                                      |> Frame.reduceValues (+)
        let totalVotes = Stats.sum voteCounts
        voteCounts |> Series.mapValues (fun a -> float a / float totalVotes)

type CandidatesOfChoice = Map<Minority.Name,Column>

type ElectionGroup = 
    {
        Name: string
        Score: Map<Minority.Name, float>
        Primary: Election
        PrimaryCoC: CandidatesOfChoice
        Runoff: Election option
        RunoffCoC: CandidatesOfChoice option
        General: Election option
        GeneralCoC: CandidatesOfChoice option
    }

type LogitParams = 
    {
        Coef: float
        Intercept: float
    }

type SuccessFunction<'a when 'a : equality> =  District<'a> -> Minority.Name -> ElectionGroup -> float

/// <summary>
///     Represents Success of a candidate of choice in LA with respect to the passed election group
/// </summary>
/// <param name="district"></param> Frame where each row is a precinct within the district and contains
/// candidate columns.
/// <param name="minority"></param>
/// <param name="election"></param>
/// <returns> 1. if the CoC was successful and 0. otherwise.</returns>
let CoCCarriesElectLA (district: District<'a>) (minority: Minority.Name) (election: ElectionGroup) = 
        let PrimaryVoteShares = election.Primary.VoteShares district |> Series.sortBy (fun v -> - v)
        let PrimCoCVoteShare = PrimaryVoteShares.[election.PrimaryCoC.[minority]]
        let PrimaryAdvance = match PrimCoCVoteShare with
                             | maj when maj > 0.5 -> 1.
                             | x when Stats.max PrimaryVoteShares < 0.5 & (Series.getAt 0 PrimaryVoteShares = x)  -> 1.
                             | x when Stats.max PrimaryVoteShares < 0.5 & (Series.getAt 1 PrimaryVoteShares = x)   -> 1.
                             | _ -> 0.
        let GenWin = match election.General, election.GeneralCoC with
                     | None, None -> 1.
                     | Some election, Some cand when (election.VoteShares district).[cand.[minority]] > 0.5 -> 1.
                     | _ -> 0.
        
        match election.Name.[0..3] with
        | "PRES" when (Series.getAt 0 PrimaryVoteShares = PrimCoCVoteShare) -> GenWin
        | "PRES" -> 0.
        | _ -> PrimaryAdvance * GenWin
        

/// <summary>
///     Represents Success of a candidate of choice in TX with respect to the passed election group
/// </summary>
/// <param name="district"></param>
/// <param name="minority"></param>
/// <param name="election"></param>
/// <returns> 1. if the CoC was successful and 0. otherwise.</returns>
let CoCCarriesElectTX (district: District<'a>) (minority: Minority.Name) (election: ElectionGroup) = 
        let PrimaryVoteShares = election.Primary.VoteShares district |> Series.sortBy (fun v -> - v)
        let PrimCoCVoteShare = PrimaryVoteShares.[election.PrimaryCoC.[minority]]
        let PrimaryAdvance = match PrimCoCVoteShare with
                             | maj when maj > 0.5 -> 1.
                             | x when Stats.max PrimaryVoteShares < 0.5 & (Series.getAt 0 PrimaryVoteShares = x)  -> 1.
                             | x when Stats.max PrimaryVoteShares < 0.5 & (Series.getAt 1 PrimaryVoteShares = x)   -> 1.
                             | _ -> 0.
        let RunoffWin = match election.Runoff, election.RunoffCoC with
                        | None, None -> 1.
                        | Some election, Some cand when (election.VoteShares district).[cand.[minority]] > 0.5 -> 1.
                        | _ -> 0.
        let GenWin = match election.General, election.GeneralCoC with
                     | None, None -> 1.
                     | Some election, Some cand when (election.VoteShares district).[cand.[minority]] > 0.5 -> 1.
                     | _ -> 0.
        PrimaryAdvance * RunoffWin * GenWin


/// <summary>
/// Compute the group alignment of a district; aka twice the minorities CVAP share capped at 1.
/// </summary>
/// <param name="districtData"> Frame where each row is a precinct within the district and contains
/// CVAP columns.
/// </param>
/// <param name="minority"> With respect to which minority?
///</param>
/// <returns> Twice the minorities CVAP share capped at 1. </returns>
let alignment (districtData: District<'a>) (minority: Minority.Minority) = 
    let _, MinCVAPCol, TotCVAPCol = minority
    let DistrictMinorityCVAP = Stats.sum districtData.[MinCVAPCol]
    let DistrictTotalCVAP = Stats.sum districtData.[TotCVAPCol]
    min (2. * DistrictMinorityCVAP / DistrictTotalCVAP) 1.



let DistrictVRAEffectiveness (districtData: District<'a>) ((name, MinCol, TotCol): Minority.Minority)
                             (elections: ElectionGroup array) (successFunc: SuccessFunction<'a>)
                             (logitParams: LogitParams option) = 
    let districtAlignment = alignment districtData (name, MinCol, TotCol)
    let electionWeights = elections |> Array.map (fun (e: ElectionGroup) -> e.Score.[name]) 
                                    |> Vector<float>.Build.DenseOfArray
    let minPrefWins = elections |> Array.map (successFunc districtData name) 
                                |> Vector<float>.Build.DenseOfArray
    let minVRAscore = (electionWeights.DotProduct minPrefWins) * (districtAlignment / electionWeights.Sum())
    match logitParams with
    | Some {LogitParams.Coef = coef; LogitParams.Intercept = intercept} -> 1./(1. + exp -(coef*minVRAscore + intercept))
    | None -> minVRAscore
