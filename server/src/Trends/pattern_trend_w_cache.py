#import itertools
import os
import sys
import time
from collections import defaultdict

import sqlalchemy
import pandas as pd
from tqdm import tqdm
from itertools import chain, combinations

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Trends.pattern_trend import *





class TrendCherryPickerOptimized(TrendCherryPicker):
    def __init__(self, df, conf):
        """
        :param gb_query: query string with a formatting variable named <cond>
        :param partial_order: a list of groups to check. Assuming the values should be mono increasing.
        :param df:
        :param exclude:
        :param is_numeric:
        """
        super(TrendCherryPickerOptimized, self).__init__(df, conf)
        self.query_results = {}
        self.orig_result_sum = self.evaluate_orig_query('sum')
        self.orig_result_count = self.evaluate_orig_query('count')
        # query_results: agg: {pattern: result}
        if self.conf['agg'].lower() == 'avg':
            self.query_results['sum'] = defaultdict(lambda: {g: 0 for g in self.orig_result_sum})
            self.query_results['count'] = defaultdict(lambda: {g: 0 for g in self.orig_result_count})
        else:
            self.query_results[self.conf['agg']] = defaultdict(lambda: {g: 0 for g in self.orig_result_count})

    def get_negated_result(self, query_result_sum=None, query_result_count=None):
        # compute the query results by removing this result from the original query result.
        # This works for sum, count and avg.
        # TODO: the calculation of num_empty_groups will be wrong because it's based on counting Nones. and we have replaced those with 0's.
        agg = self.conf['agg'].lower()
        if agg == 'sum':
            return {g: self.orig_result_sum[g] - query_result_sum.get(g) for g in self.orig_result_sum}
        if agg == 'count':
            return {g: self.orig_result_count[g] - query_result_count.get(g) for g in self.orig_result_count}
        if agg == 'avg':
            res = {}
            for g in self.orig_result_count:
                c = self.orig_result_count[g] - query_result_count.get(g)
                if c == 0:
                    res[g] = None
                    continue
                s = self.orig_result_sum[g] - query_result_sum.get(g)
                res[g] = s/c
            return res
        raise Exception(f"get_negated_result not implemented for {self.conf['agg']}!")

    # def compute_from_subqueries(self, list_of_query_results_and_factors, agg):
    #     if agg.lower() == 'sum':
    #         orig_result = self.orig_result_sum
    #     elif agg.lower() == 'count':
    #         orig_result = self.orig_result_count
    #     else:
    #         raise Exception(f"compute_from_subqueries not implemented for {self.conf['agg']}!")
    #     res = {}
    #     for g in orig_result:
    #         sg = 0
    #         for qr, factor in list_of_query_results_and_factors:
    #             if g in qr:
    #                 sg += (factor*qr[g])
    #         #res[g] = self.orig_result[g] - sg
    #         res[g] = sg
    #     return res

    # def disj_to_pie_conjunctions(self, disj):
    #     # Compute the conjunctive patterns for the principle of inclusion and exclusion.
    #     res = []
    #     for k in range(1, len(disj)+1):
    #         factor = (-1)**(k-1)
    #         conj_combs = combinations(disj, k)  # conjunction combinations of size k
    #         for list_of_conj in conj_combs:
    #             # For each conj combination, make it into one conjunction (list of atoms), and sort by the attributes.
    #             # there shouldn't be repetitions in the list of conjunctions.
    #             new_conj = sorted(flatten_extend(list_of_conj), key=lambda x: x[0])
    #             new_conj_attributes = [x[0] for x in new_conj]
    #             if len(set(new_conj_attributes)) < len(new_conj_attributes):
    #                 # an attribute appears more than once - the conjunction will be empty (A=a and A=b can't hold).
    #                 continue
    #             res.append((new_conj, factor))
    #     return res

    def evaluate_gb_query(self, pred, negate):
        # First, try to read the result from the cache

        agg = self.conf['agg'].lower()
        if agg in ('count', 'sum', 'avg'):
            # conjunction - list of tuples
            # disjunction - tuple of list of tuples.
            # TODO: we should probably have a better use of types here.
            if type(pred) == tuple:  # disjunction
                if agg == 'sum':
                    res_sum = self.compute_from_subqueries(pred, agg)
                    return self.get_negated_result(query_result_sum=res_sum)
                if agg == 'count':
                    res_count = self.compute_from_subqueries(pred, agg)
                    return self.get_negated_result(query_result_count=res_count)
                if agg == 'avg':
                    res_sum = self.compute_from_subqueries(pred, 'sum')
                    res_count = self.compute_from_subqueries(pred, 'count')
                    return self.get_negated_result(query_result_sum=res_sum, query_result_count=res_count)
            # Not sure this is needed - I don't think it will ever be called
            elif type(pred) == list:  # conjunction
                print("called eval_gb_query with a conjunction. Why?")
                print(pred)
                sys.exit()
                # if agg == 'sum':
                #     return self.get_negated_result(query_result_sum=self.query_results[agg][pred])
                # elif agg == 'count':
                #     return self.get_negated_result(query_result_count=self.query_results[agg][pred])
                # if agg == 'avg':
                #     return self.get_negated_result(query_result_sum=self.query_results['sum'][pred],
                #                                    query_result_count=self.query_results['count'][pred])
        # If it's not in the cache, we compute it
        return super(TrendCherryPickerOptimized, self).evaluate_gb_query(pred, negate=self.conf["negate"])

    # def evaluate_conjunctions(self, agg):
    #     # create all allowed attr combinations.
    #     # run a single query for each combination.
    #     # save the results into self.query_results.
    #     cols_for_pattern = [c for c in self.conf["include"] if c not in self.conf["numeric"]]
    #     attr_combinations = []
    #     for num_atoms in range(1, self.max_atoms+1):
    #         attr_combinations.extend([tuple(sorted(comb)) for comb in combinations(cols_for_pattern, num_atoms)])
    #     print(f"Evaluating conjunctions with agg={agg} up to {self.max_atoms} atoms.")
    #     for comb in tqdm(attr_combinations):
    #         if self.use_sql_db:
    #             comb_str = ", ".join([f'"{col}"' for col in comb])
    #             gb_query = f"""SELECT {comb_str}, "{self.gb_attr}", {agg}("{self.outcome_attr}") FROM my_table
    #                     GROUP BY {comb_str}, "{self.gb_attr}";
    #                     """
    #             query = sqlalchemy.text(gb_query)
    #             query_result = self.engine.execute(query)
    #             res_df = pd.DataFrame(query_result, columns=[*comb, self.gb_attr, self.outcome_attr])
    #         else:
    #             res_df = self.df.groupby([*comb, self.gb_attr])[self.outcome_attr].agg(agg).reset_index()
    #         grouped = res_df.groupby(list(comb))
    #         for vcomb, group in grouped:
    #             # For each group, create a dictionary of G: O pairs
    #             g_o_dict = dict(zip(group[self.gb_attr], group[self.outcome_attr]))
    #             for g in g_o_dict:
    #                 if pd.isna(g_o_dict[g]):  # replace nans with 0
    #                     g_o_dict[g] = 0
    #             self.query_results[agg][str(make_conjunctive_pred(comb, vcomb))] = g_o_dict

    def search_trend_views(self, output_path):
        t = "\t"
        s1 = time.time()
        preds = self.generate_possible_views()
        s2 = time.time()
        print(f"Generating all predicates took {s2-s1} seconds.")
        if self.conf['negate']:
            pred_title = "excluded_pred"
        else:
            pred_title = "included_pred"

        with open(output_path, "w") as f:
            order_str = t.join([str(x) for x in self.partial_order])
            f.write(f"{pred_title}{t}coverage{t}num_atoms{t}num_empty{t}{order_str}\n")

        if self.conf['agg'].lower() == 'avg':
            self.evaluate_conjunctions(agg='sum')
            self.evaluate_conjunctions(agg='count')
        else:
            self.evaluate_conjunctions(self.conf['agg'].lower())
        s3 = time.time()
        print(f"Evaluated conjunctions in {s3-s2} seconds.")
        #preds = [([("product_group_name", '=', 'Garment Upper body')], [("FN", "=", '1.0')])]
        for pred in tqdm(preds):
            res, coverage, num_atoms, num_empty = self.check_view(pred)
            if res is not None:
                print(pred)
                with open(output_path, "a") as f:
                    f.write(f"{disjunct_to_sql_cond(pred, negate=False, for_output=True, buckets=self.bucket_objects)}{t}{coverage/self.data_size}{t}{num_atoms}{t}{num_empty}{t}{t.join([str(x) for x in res])}\n")
        s4 = time.time()
        print(f"Finished the search, time: {s4-s3} seconds. Total time: {s4-s1} seconds.")





# if __name__ == '__main__':
#     # stack overflow + decision tree + outlier removal
#     #df, conf = read_SO_and_conf(outlier_percent=0.02)
#     # ids_to_remove = get_outliers(df, 'ConvertedCompYearly')
#     # #ids_to_remove = [61044, 72941, 202, 62027, 70523, 18923, 62224, 66496, 47934, 27426, 20250, 30824, 40790, 1799, 10331, 1889, 39216, 61968, 31042, 51600, 11639, 20938, 50406, 14795, 21415, 21480, 37697, 47086, 62235, 53498, 66811, 67034, 67855, 8344, 16127, 39444, 20165, 309, 1741, 5233]
#     # real_ids_to_remove = [id for id in ids_to_remove if id in df['ResponseId'].values]
#     # print(f"already removed during outlier removal: {set(ids_to_remove).difference(set(real_ids_to_remove))}, remaining: {real_ids_to_remove}")
#     # conf["ids_to_remove"] = real_ids_to_remove
#     # dt = DecisionTreePatternFinder(df, conf)
#     # attrs = list(set(dt.find_prominent_attributes()))
#     # print(f"Focusing search on these attributes: {attrs}")
#     # conf["include"] = attrs
#
#     # German credit
#     # df, conf = read_german_and_conf()
#     #output_path = "data/german_credit/trend_results/employment_trend_preds_3atom_disj.tsv"
#
#     # H&M
#     # df, conf = read_hm_and_conf2(month=5)
#
#     # Zillow
#     df, conf = read_zillow_and_conf(outlier_percent=0.05)
#
#     tcp = TrendCherryPickerOptimized(df, conf)
#     # tcp.generate_possible_views()
#     tcp.search_trend_views(conf['output_path'])

