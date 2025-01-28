import itertools
import os
import sys
import time
from collections import defaultdict

import sqlalchemy
import pandas as pd
from sklearn.neighbors import LocalOutlierFactor
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ClaimEndorseFunctions import Bucket
from utils import age_bucketize, remove_outliers, get_outliers, calc_anova_for_attrs
from Trends.DT_pattern_finder import DecisionTreePatternFinder
from QueryRunner import SQLEngineSingleton

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'Trendline-Outlier-Detection')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'TupleDeletionForMonotonicityConstraints')))

# Idan's dynamic programming code
# from InputParser import *
# from Utils import *
# from OptimalSubsetWithConstraint import *

# Or's greedy algorithm
# from aggr_main import greedy_algorithm


def flatten_extend(list_of_lists):
    flat_list = []
    for li in list_of_lists:
        flat_list.extend(li)
    return flat_list


def make_buckets(is_numeric, df):
    bucket_objects = {}
    for attr_name in is_numeric:
        bucket = Bucket.from_attr_name(attr_name, df=df)
        bucket_objects[attr_name] = bucket
        print(f"{attr_name} bucket: {bucket.low}, {bucket.high}, {bucket.count}")
    return bucket_objects


def conjunct_to_sql_cond(conj, for_output=False, buckets=None):
    # list of tuples of the form (A, sign, v)
    # TODO is it okay that we have '' here?? (For numeric attributes)
    template = """ "{a}"{sign}'{v}' """
    str_atoms = []
    for a, sign, v in conj:
        orig_attr = a.replace("_binned", "")
        if for_output and orig_attr in buckets:
            val = buckets[orig_attr].bucket_to_range_string(v)
        else:
            val = clean_value(v)
        str_atoms.append(template.format(a=a, sign=sign, v=val))
    s = " AND ".join(str_atoms)
    return f"({s})"


def disjunct_to_sql_cond(disj, negate=True, for_output=False, buckets=None):
    # a disjunction is a tuple of lists of tuples.
    # each list of tuples represents a conjunct.
    if type(disj) == str:
        return disj
    pred_text = " OR ".join([conjunct_to_sql_cond(conj, for_output, buckets) for conj in disj])
    if negate:
        pred_text = f"NOT ({pred_text})"
    return pred_text


def sign_to_pandas_sign(sign_str):
    if sign_str == '=':
        return '=='
    return sign_str


def agg_to_pandas_agg(agg_str):
    if agg_str == 'AVG':
        return 'mean'
    if agg_str == 'MAX':
        return 'max'
    return agg_str


def conjunct_to_pandas_cond(conj, attr_to_type_dict):
    # list of tuples of the form (A, sign, v)
    atoms = []
    object_template = """ `{a}`{sign}'{v}' """
    num_template = """ `{a}`{sign}{v} """
    for a, sign, v in conj:
        if attr_to_type_dict[a] == 'object':
            atoms.append(object_template.format(a=a, sign=sign_to_pandas_sign(sign), v=v))
        else:
            atoms.append(num_template.format(a=a, sign=sign_to_pandas_sign(sign), v=v))
    s = " and ".join(atoms)
    return f"({s})"


def disjunct_to_pandas_cond(disj, attr_to_type_dict, negate=True,):
    # a disjunction is a tuple of lists of tuples.
    # each list of tuples represents a conjunct.
    if type(disj) == str:
        return disj
    pred_text = " or ".join([conjunct_to_pandas_cond(conj, attr_to_type_dict) for conj in disj])
    if negate:
        pred_text = f"not ({pred_text})"
    return pred_text


def make_conjunctive_pred(attr_comb, value_comb):
    if len(attr_comb) != len(value_comb):
        raise Exception(f"len mismatch between attr comb ({len(attr_comb)}) and  value_comb({len(value_comb)}).")
    t = []
    for i in range(len(attr_comb)):
        t.append((attr_comb[i], "=", value_comb[i]))
    return sorted(t, key=lambda x: x[0])  # sort the tuple according to the attribute name


def num_atoms_in_disj(disj):
    return sum([len(conj) for conj in disj])


def clean_value(value):
    if type(value) == str:
        return value.replace("'", "''")
    return value


def check_order(groups_order, query_result):
    effective_order = [g for g in groups_order if g in query_result]
    for i in range(len(effective_order) - 1):
        g = effective_order[i]
        g_next = effective_order[i + 1]
        # if g not in query_result or g_next not in query_result or query_result[g] is None or query_result[g_next] is None:
        #     continue
        #try:
        if query_result[g] > query_result[g_next]:
            return False
        # except:
        #     print(f"check_order: problem with {query_result}")
    return True


def get_violations(groups_order, query_result):
    effective_order = [g for g in groups_order if g in query_result]
    violations = [max(0, query_result[effective_order[i]] - query_result[effective_order[i+1]])
                  for i in range(len(effective_order)-1)]
    return sum(violations)


class TrendCherryPicker(object):
    def __init__(self, df, conf):
        """
        :param gb_query: query string with a formatting variable named <cond>
        :param partial_order: a list of groups to check. Assuming the values should be mono increasing.
        :param df:
        :param exclude:
        :param is_numeric:
        """
        # query string
        self.gb_query = conf['gb_query']
        self.gb_attr = conf['gb_attr']  # numeric group by attribute
        self.outcome_attr = conf['outcome_attr']
        self.use_sql_db = conf['use_sql']
        if self.use_sql_db:
            self.engine = SQLEngineSingleton(conf['database_name'])
        # self.df = df
        b = len(df)
        self.df = df[(~df[self.gb_attr].isna()) & (~df[self.outcome_attr].isna())]
        a = len(self.df)
        print(f"keeping {a}/{b} rows where outcome and gb attrs are not null.")
        if conf.get('partial_order') is not None:
            self.partial_order = conf.get('partial_order')
        else:
            # assume numeric gb attribute.
            self.partial_order = sorted([a for a in self.df[self.gb_attr].unique() if not pd.isna(a)])
        self.data_size = len(self.df)
        # self.include = conf['include']
        # self.numeric = conf['numeric']
        self.conf = conf
        numeric_include = [col for col in conf['include'] if col in conf['numeric']]
        self.bucket_objects = make_buckets(numeric_include, self.df)
        for attr, bucket in self.bucket_objects.items():
            self.df[f"{attr}_binned"] = self.df[attr].apply(bucket.value_to_bucket_id)
            self.conf["include"].append(f"{attr}_binned")
            print(f"{attr}_binned: {bucket}")
        self.coverage_query = conf['coverage_query']
        self.max_atoms = conf['max_atoms']
        self.attr_types = {col: self.df[col].dtype for col in self.df.columns}
        self.orig_result_sum = self.evaluate_orig_query('sum')
        self.orig_result_count = self.evaluate_orig_query('count')
        self.query_results = {}
        for agg in {'count', self.conf['agg']}:
            self.query_results[agg] = defaultdict(lambda: {g: 0 for g in self.orig_result_count})

    def evaluate_orig_query(self, agg=None):
        conf = self.conf
        if agg is None:
            agg = conf['agg']
        if self.use_sql_db:
            query = f"""SELECT "{conf['gb_attr']}",{agg}("{conf['outcome_attr']}") FROM my_table WHERE "{conf['outcome_attr']}" IS NOT NULL """ + \
                    f"""GROUP BY "{conf['gb_attr']}";"""
            query = sqlalchemy.text(query)
            query_result = self.engine.execute(query)
            query_result = dict(list(query_result))
            return query_result
        # Use the dataframe
        agg_func = agg_to_pandas_agg(agg)
        query_result = self.df.groupby(self.gb_attr)[self.outcome_attr].agg(agg_func).to_dict()
        return query_result

    def evaluate_gb_query(self, pred, negate):
        if self.use_sql_db:
            query = sqlalchemy.text(self.gb_query.format(cond=disjunct_to_sql_cond(pred, negate)))
            query_result = self.engine.execute(query)
            query_result = dict(list(query_result))
            return query_result
        # Use the dataframe
        subset = self.df.query(disjunct_to_pandas_cond(pred, self.attr_types, negate))
        agg_func = agg_to_pandas_agg(self.conf['agg'])
        query_result = subset.groupby(self.gb_attr)[self.outcome_attr].agg(agg_func).to_dict()
        return query_result

    def evaluate_coverage_query(self, pred):
        # for coverage queries, never negate. We want the size of the removed population.
        if self.use_sql_db:
            coverage_query_result = self.engine.execute(
                self.coverage_query.format(cond=disjunct_to_sql_cond(pred, negate=False)))
            coverage = list(coverage_query_result)[0][0]
            return coverage
        # evaluate against df
        subset = self.df.query(disjunct_to_pandas_cond(pred, self.attr_types, negate=False))
        return len(subset)

    def evaluate_conjunctions(self, agg):
        # create all allowed attr combinations.
        # run a single query for each combination.
        # save the results into self.query_results.
        cols_for_pattern = [c for c in self.conf["include"] if c not in self.conf["numeric"]]
        attr_combinations = []
        for num_atoms in range(1, self.max_atoms+1):
            print(f"num_atoms={num_atoms}")
            attr_combinations.extend([tuple(sorted(comb)) for comb in itertools.combinations(cols_for_pattern, num_atoms)])
        print(f"Evaluating conjunctions with agg={agg} up to {self.max_atoms} atoms.")
        for comb in tqdm(attr_combinations):
            if self.use_sql_db:
                comb_str = ", ".join([f'"{col}"' for col in comb])
                gb_query = f"""SELECT {comb_str}, "{self.gb_attr}", {agg}("{self.outcome_attr}") FROM my_table 
                        GROUP BY {comb_str}, "{self.gb_attr}";
                        """
                query = sqlalchemy.text(gb_query)
                query_result = self.engine.execute(query)
                res_df = pd.DataFrame(query_result, columns=[*comb, self.gb_attr, self.outcome_attr])
            else:
                res_df = self.df.groupby([*comb, self.gb_attr])[self.outcome_attr].agg(agg).reset_index()
            grouped = res_df.groupby(list(comb))
            for vcomb, group in grouped:
                # For each group, create a dictionary of G: O pairs
                g_o_dict = dict(zip(group[self.gb_attr], group[self.outcome_attr]))
                for g in g_o_dict:
                    if pd.isna(g_o_dict[g]):  # replace nans with 0
                        g_o_dict[g] = 0
                self.query_results[agg][str(make_conjunctive_pred(comb, vcomb))] = g_o_dict

    def compute_from_subqueries(self, disj_pred, agg):
        conjs_and_factors = self.disj_to_pie_conjunctions(disj_pred)
        list_of_query_results_and_factors = [(self.query_results[agg][str(conj)], factor)
                                             for conj, factor in conjs_and_factors]
        if agg.lower() == 'sum':
            orig_result = self.orig_result_sum
        elif agg.lower() == 'count':
            orig_result = self.orig_result_count
        else:
            raise Exception(f"compute_from_subqueries not implemented for {self.conf['agg']}!")
        res = {}
        for g in orig_result:
            sg = 0
            for qr, factor in list_of_query_results_and_factors:
                if g in qr:
                    sg += (factor*qr[g])
            res[g] = sg
        return res

    def disj_to_pie_conjunctions(self, disj):
        # Compute the conjunctive patterns for the principle of inclusion and exclusion.
        res = []
        for k in range(1, len(disj)+1):
            factor = (-1)**(k-1)
            conj_combs = itertools.combinations(disj, k)  # conjunction combinations of size k
            for list_of_conj in conj_combs:
                # For each conj combination, make it into one conjunction (list of atoms), and sort by the attributes.
                # there shouldn't be repetitions in the list of conjunctions.
                new_conj = sorted(flatten_extend(list_of_conj), key=lambda x: x[0])
                new_conj_attributes = [x[0] for x in new_conj]
                if len(set(new_conj_attributes)) < len(new_conj_attributes):
                    # an attribute appears more than once - the conjunction will be empty (A=a and A=b can't hold).
                    continue
                res.append((new_conj, factor))
        return res

    def check_view(self, pred, calc_impact=False):
        # TODO separate the violations to another function
        query_result = self.evaluate_gb_query(pred, self.conf["negate"])
        # Validate the partial order over the results.
        order_holds = check_order(self.partial_order, query_result)
        if not order_holds and not calc_impact:
            return None, None, None, None
        # check coverage
        coverage = self.compute_from_subqueries(pred, 'count')
        #coverage = self.evaluate_coverage_query(pred)
        res = [query_result[g] if g in query_result else None for g in self.partial_order]
        num_empty_groups = res.count(None)
        if calc_impact:
            sum_violations = get_violations(self.partial_order, query_result)
            return res, coverage, num_atoms_in_disj(pred), num_empty_groups, sum_violations
        return res, coverage, num_atoms_in_disj(pred), num_empty_groups

    def generate_possible_views(self):
        s1 = time.time()
        # simple - one atom, and then complicate
        single_atoms = {}
        cols_for_pattern = [c for c in self.conf["include"] if c not in self.conf["numeric"]]
        # cols_for_pattern = self.conf["include"]
        for column in cols_for_pattern:
            single_atoms[column] = []
            for value in self.df[column].unique():
                # TODO: support the operand "!=" ?
                if pd.isna(value):
                    continue
                # if type(value) == str:
                #     clean_value = value.replace("'", "''")
                # else:
                #     clean_value = value
                single_atoms[column].append((column, "=", value))
        atoms = flatten_extend(single_atoms.values())
        if self.max_atoms == 1:
            return [[a] for a in atoms]
        s2 = time.time()
        print(f"Finished generating {len(atoms)} atoms in {s2 - s1} seconds")
        conjunctions = {1: [[a] for a in atoms]}
        for i in range(2, self.max_atoms + 1):
            conjunctions[i] = []
            # Create all conjunctions (of size i) that are not empty.
            # First, create attribute combinations of size i
            attr_combs = itertools.combinations(cols_for_pattern, i)
            # For each one, find all value combinations.
            for attr_comb in attr_combs:
                sorted_comb = sorted(attr_comb)
                value_combs = self.df[sorted_comb].value_counts().index
                for vc in value_combs:
                    # create all equality conjunctions.
                    conjunctions[i].append([(sorted_comb[j], "=", vc[j]) for j in range(i)])

        all_conjunctions = flatten_extend(conjunctions.values())
        s3 = time.time()
        print(f"Finished generating {len(all_conjunctions)} conjunctions in {s3 - s1} seconds after atom creation.")

        if self.conf['enable_dnf']:
            max_atoms = self.max_atoms
        else:
            max_atoms = 1
        disjunctions = []
        for m in range(1, max_atoms + 1):
            print(f"Creating DNFs with m={m}. Note that DNFs with m=1 are just conjunctions.")
            disjunctions_m = itertools.combinations(all_conjunctions, m)
            disjunctions.append(disjunctions_m)
            # print(f"Next, iterate over {len(list(disjunctions_m))} possibilities")
            #for disj in tqdm(disjunctions_m):
            #    if num_atoms_in_disj(disj) <= self.max_atoms:
            #        disjunctions.append(disj)

        if self.conf['enable_disjunctions']:
            for m in range(1, self.max_atoms + 1):
                print(f"Creating disjunctions of atoms with m={m}")
                #disjunctions.extend(itertools.combinations(conjunctions[1], m))
                disjunctions.append(itertools.combinations(conjunctions[1], m))

        disjunctions = itertools.chain.from_iterable(disjunctions)
        if self.conf['enable_dnf']:
            disjunctions = itertools.filterfalse(lambda disj: num_atoms_in_disj(disj) > self.max_atoms,
                                                 disjunctions)

        print(
            f"Found {len(all_conjunctions)} conjunctive predicates.")  #, {len(disjunctions)} total predicates of up to {self.max_atoms} atoms.
        return disjunctions

    def search_trend_views(self, output_path):
        t = "\t"
        s1 = time.time()
        preds = self.generate_possible_views()
        s2 = time.time()
        print(f"Generating all predicates took {s2 - s1} seconds.")
        with open(output_path, "w") as f:
            order_str = t.join([str(x) for x in self.partial_order])
            f.write(f"excluded_pred{t}coverage{t}num_atoms{t}num_empty{t}{order_str}\n")
        # preds = [([('Country', '=', 'United States of America')], [('OfficeStackAsyncHaveWorkedWith', '=', 'Adobe Workfront')])]
        for pred in tqdm(preds):
            res, coverage, num_atoms, num_empty = self.check_view(pred)
            if res is not None:
                print(pred)
                with open(output_path, "a") as f:
                    f.write(
                        f"{disjunct_to_sql_cond(pred, for_output=True, buckets=self.bucket_objects)}{t}{coverage / self.data_size}{t}{num_atoms}{t}{num_empty}{t}{t.join([str(x) for x in res])}\n")
        s3 = time.time()
        print(f"Finished the search, time: {s3 - s2} seconds. Total time: {s3 - s1} seconds.")

    def greedy_search_trend_views(self, output_path, beam_size=100):
        output_path_beam = output_path.split(".")[0]+"_beam_log.tsv"
        t = "\t"
        order_str = t.join([str(x) for x in self.partial_order])
        with open(output_path, "w") as f:
            f.write(f"excluded_pred{t}coverage{t}num_atoms{t}num_empty{t}{order_str}\n")
        with open(output_path_beam, "w") as f:
            f.write(f"excluded_pred{t}atoms{t}impact{t}coverage{t}{order_str}\n")

        max_atoms = self.max_atoms
        self.max_atoms = 1
        self.conf['enable_disjunctions'] = False
        atoms = self.generate_possible_views()  # atoms
        self.max_atoms = max_atoms
        print(f"evaluating conjunctions up to {max_atoms}")
        self.evaluate_conjunctions(agg='count')

        # atoms = self.generate_possible_views()  # atoms
        preds = [[a] for a in atoms]
        best_found = {}  # top k for each number of atoms
        query_result = self.evaluate_orig_query()
        sum_violations_orig = get_violations(self.partial_order, query_result)
        m = 1
        while m <= max_atoms:
            print(f"searching with {m} atoms")
            # for each atom, check the impact
            impacts = []
            coverages = []
            results = []
            for pred in tqdm(preds):
                res, coverage, num_atoms, num_empty, sum_violations_pred = self.check_view(pred, calc_impact=True)
                if sum_violations_pred == 0:
                    with open(output_path, "a") as f:
                        f.write(
                            f"{disjunct_to_sql_cond(pred, negate=False, for_output=True, buckets=self.bucket_objects)}{t}{coverage / self.data_size}{t}{num_atoms}{t}{num_empty}{t}{t.join([str(x) for x in res])}\n")
                impacts.append(sum_violations_orig - sum_violations_pred)  # allow negative impact (for now)
                coverages.append(coverage)
                results.append(res)
            # get top preds so far
            best_found_idx = sorted(range(len(preds)), key=impacts.__getitem__, reverse=True)[:beam_size]
            best_found[m] = [(preds[i], impacts[i], coverages[i], results[i]) for i in best_found_idx]
            # print(best_found[m])
            with open(output_path_beam, "a") as f:
                for pred, impact, coverage, res in best_found[m]:
                    f.write(f"{disjunct_to_sql_cond(pred, negate=False, for_output=True, buckets=self.bucket_objects)}{t}{m}{t}{impact}{t}{coverage/self.data_size}{t}{t.join([str(x) for x in res])}\n")
            # make new preds
            print(f"creating new predicates with {m}+1 atoms")
            preds = []
            for pred, impact, pred_coverage, _ in best_found[m]:
                for atom in atoms:
                    if atom in pred:
                        continue
                new_pred = sort_disj_by_atoms(pred + [atom])
                new_pred_coverage = self.compute_from_subqueries(new_pred, 'count')
                if pred_coverage == new_pred_coverage:  # The added atom does not change the set of tuples. It only complicates the predicate.
                    continue
                if new_pred not in preds:
                    preds.append(new_pred)
            m += 1


def sort_disj_by_atoms(disj):
    sorted_by_value = sorted(disj, key=lambda x: x[2])
    sorted_by_attribute_and_value = sorted(sorted_by_value, key=lambda x: x[0])
    return sorted_by_attribute_and_value

def bucketize(x, thresholds, labels=None):
    # labels should be longer than thresholds by 1 item.
    for i, t in enumerate(thresholds):
        if x < t:
            if labels is not None:
                return labels[i]
            return i + 1  # default labels: 1,2,3,...
        if x >= thresholds[-1]:
            if labels is not None:
                return labels[len(thresholds)]
            return len(thresholds) + 1


def bmi_bucketize(x):
    return bucketize(x, [24.9, 29.9, 39.9])


def year_bucketize(x):
    return bucketize(x, range(1990, 2016, 5), [f"{i}-{i+4}" for i in range(1985, 2015, 5)] + [">2015"])


def run_dynamic_prog_tuple_deletion(df, conf):
    outcome_attr_index = getAggregationAttributeIndexByName(df, conf['outcome_attr'])
    agg_func = getAggregationFunctionFromInput("SUM")
    gb = groupFrameByAttributes(df, [conf['gb_attr']], conf['outcome_attr'])
    solution = calculateOptimalSubsetWithConstraint(
                    gb,
                    agg_func,
                    outcome_attr_index)
    print(f"Kept {len(solution)}/{len(df)} ({int(len(solution)*100/len(df))}%) rows")
    removed = calculateRemovedTuples(df, solution)
    return removed


def run_greedy_tuple_deletion(df, conf):
    function_map = {"sum": sum, "max": max, "avg": pd.Series.mean}
    agg_func = function_map[conf['agg'].lower()]
    output_path = conf["output_path"].split(".")[0] + "_tuple_del.csv"
    result_df = greedy_algorithm(df, agg_func, grouping_column=conf['gb_attr'], aggregation_column=conf['outcome_attr'], output_csv=output_path)
    removed = calculateRemovedTuples(df, result_df)
    return removed


def calc_anova_and_get_top_attrs(df, conf, num_top_attrs_to_return):
    anova_dict = {}
    for col in conf["include"]:
        anova, pval = calc_anova_for_attrs(df, [col], conf['outcome_attr'], bucket_dict={})
        anova_dict[col] = anova
    print(anova_dict)
    return sorted(anova_dict.keys(), key=anova_dict.get, reverse=True)[:num_top_attrs_to_return]


