import statistics
import networkx as nx
import numpy as np
from gerrychain import GeographicPartition, updaters, metrics


class PlanMetrics:
    def __init__(self, part, county_pops, elections, county_col="COUNTY", municipality_col="Town") -> None:
        self.part = part
        self.graph = part.graph
        self.county_column = county_col
        self.municipality_column = municipality_col
        self.county_pops = county_pops
        self.elections = elections


    def district_contiguity(self, district):
        district_graph = self.graph.subgraph(district)
        return nx.is_connected(district_graph)


    def polsby_popper(self):
        scores = [v for _k, v in metrics.polsby_popper(self.part).items()]
        stats = {
            'max': max(scores),
            'min': min(scores),
            'mean': statistics.mean(scores),
            'median': statistics.median(scores)
        }
        if len(scores) > 1:
            stats['variance'] = statistics.variance(scores)

        return scores, stats


    def county_split_info(self):
        county_splits = updaters.county_splits("county_splits", self.county_column)(self.part)
        county_response = {}
        counties = set([self.graph.nodes[n][self.county_column] for n in self.graph.nodes])
        county_response['num_counties'] = len(counties)
        county_response['population'] = {k: v["population"] for k, v in self.county_pops.items()}
        
        split_list = {}
        splits = 0
        num_split = 0
        for c in counties:
            s = county_splits[c].contains
            # this is caused by a bug in some states in gerrychain I think
            if -1 in s:
                s.remove(-1)
            if len(s) > 1:
                num_split += 1
                split_list[c] = list(s)
                splits += len(s) - 1
        county_response['splits'] = splits
        county_response['split_list'] = split_list
        return county_response


    def municipality_split_info(self):
        municipality_splits = updaters.county_splits("muni_splits", self.municipality_column)(self.part)
        muni_response = {}
        munis = set([self.graph.nodes[n][self.municipality_column] for n in self.graph.nodes])
        muni_response['num_counties'] = len(munis)
        try:
            muni_partition = GeographicPartition(self.graph, self.municipality_column,
                                {"population": updaters.Tally('TOTPOP', alias="population")})
            muni_pop_dict = {m: muni_partition.population[m] for m in munis}
            muni_response['population'] = muni_pop_dict
            muni_response['num_counties'] = len(munis)
        except KeyError:
            muni_response['population'] = -1
        split_list = {}
        splits = 0
        num_split = 0
        for m in munis:
            s = municipality_splits[m].contains
            # this is caused by a bug in some states in gerrychain I think
            if -1 in s:
                s.remove(-1)
            if len(s) > 1:
                num_split += 1
                split_list[m] = list(s)
                splits += len(s) - 1
        muni_response['splits'] = splits
        muni_response['split_list'] = split_list
        return muni_response

    def eguia_metric(self, e, party):
        seat_share = self.part[e].seats(party) / len(self.part.parts)
        county_part = GeographicPartition(self.graph, self.county_column, self.part.updaters)
        counties = county_part.parts
        county_results = np.array([county_part[e].won(party, c) for c in counties])
        county_pops = np.array([self.county_pops[c]["population"] for c in counties])
        ideal = np.dot(county_results, county_pops) / county_pops.sum()
        return ideal - seat_share


    def partisan_metrics(self):
        """
        Return information about partisanship metric:
        Scores by elections:
            * seats
            * efficiency gap,
            * mean median
            * partisan bias
            * Eugia's metric (by county)
            * TODO::Eugia's metric (by vtds20)

        Scores by plan:
            * # Swing districts
            * # Competitive districts
        """
        party = self.part[self.elections[0]].election.parties[0]

        ## Plan wide scores
        election_results = np.array([np.array(self.part[e].percents(party)) for e in self.elections])
        num_competitive_districts = np.logical_and(election_results > 0.47, election_results < 0.53).sum()
        election_stability = (election_results > 0.5).sum(axis=0)
        num_swing_districts = np.logical_and(election_stability != 0, election_stability != len(self.elections)).sum()

        response = {"election_scores": {self.part[e].election.name: {
                                                    "seats": self.part[e].seats(party),
                                                    "efficiency_gap": self.part[e].efficiency_gap(),
                                                    "mean_median": self.part[e].mean_median(),
                                                    "partisan_bias": self.part[e].partisan_bias(),
                                                    "eguia_county": self.eguia_metric(e, party)
                                                } for e in self.elections},
                    "plan_scores": {
                                        "num_swing_districts": int(num_swing_districts),
                                        "num_competitive_districts": int(num_competitive_districts)
                                },
                    "party": party}
        return response