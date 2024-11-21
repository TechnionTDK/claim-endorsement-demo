import itertools
import os
import sqlalchemy
import pandas as pd
from tqdm import tqdm
from QueryRunner import SQLEngineSingleton
from ClaimEndorseFunctions import Bucket
from SO_Experimenting import value_cleaning_SO, is_multivalue_attr, safe_split
from config import *


def flatten_extend(list_of_lists):
    flat_list = []
    for li in list_of_lists:
        flat_list.extend(li)
    return flat_list


def make_buckets(is_numeric):
    bucket_objects = {}
    for attr_name in is_numeric:
        bucket = Bucket.from_attr_name(attr_name)
        bucket_objects[attr_name] = bucket
        print(f"{attr_name} bucket: {bucket.low}, {bucket.high}, {bucket.count}")
    return bucket_objects


class TrendCherryPicker(object):

    def __init__(self, gb_query, partial_order, df, exclude, is_numeric, coverage_query, max_atoms):
        """
        :param gb_query: query string with a formatting variable named <cond>
        :param partial_order: a list of groups to check. Assuming the values should be mono increasing.
        :param df:
        :param exclude:
        :param is_numeric:
        """
        # query string
        self.gb_query = gb_query
        # list of group names that should have monotonic increasing values.
        # TODO: Consider taking instead a list of pairs.
        self.partial_order = partial_order
        self.engine = SQLEngineSingleton()
        self.df = df
        self.data_size = len(self.df)
        self.exclude = exclude
        self.bucket_objects = make_buckets(is_numeric)
        self.coverage_query = coverage_query
        self.max_atoms = max_atoms

    def check_view(self, pred):
        # TODO: optimization - incremental removal.
        # remove the pred
        # calculate the query results.
        query = sqlalchemy.text(self.gb_query.format(cond=pred))
        query_result = self.engine.execute(query)
        query_result = dict(list(query_result))
        # Validate the partial order over the results.
        for i in range(len(self.partial_order)-1):
            g = self.partial_order[i]
            g_next = self.partial_order[i+1]
            if g not in query_result or g_next not in query_result:
                continue
            try:
                if query_result[g] > query_result[g_next]:
                    return None, None
            except:
                print(f"check_view: problem with {pred}")
        # check coverage
        coverage_query_result = self.engine.execute(self.coverage_query.format(cond=pred))
        coverage = list(coverage_query_result)[0][0]
        return [query_result[g] if g in query_result else -1 for g in self.partial_order], coverage

    def generate_possible_views(self):
        # simple - one atom, and then complicate
        single_atoms = {}
        for column in self.df.columns:
            if column in self.exclude:
                continue
            if column in self.bucket_objects:
                # TODO: handle numeric attrs instead of ignoring them
                continue
            single_atoms[column] = []
            for value in self.df[column].unique():
                # TODO: support the operand "!=" ?
                if type(value) == str:
                    clean_value = value.replace("'", "''")
                else:
                    clean_value = value
                single_atoms[column].append(f""" "{column}"='{clean_value}' """)
        if self.max_atoms == 1:
            return flatten_extend(single_atoms.values())
        if self.max_atoms > 2:
            print(f"Not supported {self.max_atoms} max atoms.")
        # enable conjuncts of 2 attributes and disjunctions of the same attribute
        preds = flatten_extend(single_atoms.values())
        print(f"Found {len(preds)} single atom predicates")
        # conjunctive
        attr_combs = itertools.combinations_with_replacement(single_atoms.keys(), 2)
        # attr_combs = itertools.combinations(single_atoms.keys(), 2)
        and_preds = 0
        or_preds = 0
        for col1, col2 in attr_combs:
            for pred1 in single_atoms[col1]:
                for pred2 in single_atoms[col2]:
                    preds.append(f"{pred1} OR {pred2}")
                    or_preds += 1
                    if col1 != col2:
                        preds.append(f"{pred1} AND {pred2}")
                        and_preds += 1
        print(f"Found {and_preds} conjunctive predicates, {or_preds} disjunctive predicates of 2 atoms.")
        disj = []
        # for pred1, pred2 in itertools.combinations(preds, 2):
        #     disj.append(f"({pred1}) OR ({pred2})")
        # print(f"Found {len(disj)} disjunctive predicates.")
        return preds + disj

    def search_trend_views(self, output_path):
        t="\t"
        preds = self.generate_possible_views()
        #success = []
        with open(output_path, "w") as f:
            order_str = t.join(self.partial_order)
            f.write(f"pred{t}coverage{t}{order_str}\n")
        for pred in tqdm(preds):
            res, coverage = self.check_view(pred)
            if res is not None:
                print(pred)
                #success.append([pred, coverage/self.data_size, *res])
                with open(output_path, "a") as f:
                    f.write(f"{pred}{t}{coverage/self.data_size}{t}{t.join([str(x) for x in res])}\n")
        #results = pd.DataFrame.from_records(success, columns=["pred", "coverage", *self.partial_order])
        #results.to_csv(output_path)
        #return success


def read_SO_dataset():
    processed_path = os.path.join("data/SO", "temp_df_for_sql_only_single_value.csv")
    if os.path.exists(processed_path):
        df = pd.read_csv(processed_path, index_col=0)
        return df
    df = pd.read_csv("data/SO/survey_results_public.csv", index_col=0)
    df = value_cleaning_SO(df)
    # removing multivalue attrs.
    df = df[[col for col in df.columns if (not is_multivalue_attr(df, col))]]
    #for col in df.columns:
    #    if is_multivalue_attr(df, col):
    #        print(f"Taking first value from multivalue attr: {col}")
    #        df[col] = df[col].apply(safe_split)
    df.to_csv(processed_path)
    df = pd.read_csv(processed_path, index_col=0)
    print(f"{len(df.columns)} columns remain")
    return df


if __name__ == '__main__':
    query = """SELECT "EdLevel", AVG("ConvertedCompYearly") FROM my_table WHERE "ConvertedCompYearly" IS NOT NULL 
               AND NOT ({cond}) GROUP BY "EdLevel"; """
    coverage_query = """SELECT COUNT("ConvertedCompYearly") FROM my_table WHERE "ConvertedCompYearly" IS NOT NULL AND {cond}; """
    partial_order = ["Bachelor’s degree", "Master’s degree", "Other doctoral degree (Ph.D., Ed.D., etc.)"]
    exclude_list = ["ResponseId", "CompTotal", "CompFreq",
                    "Currency", "SOAccount", "NEWSOSites", "SOVisitFreq", "SOPartFreq", "SOComm", "TBranch",
                    "TimeAnswering", "Onboarding", "ProfessionalTech", "SurveyLength", "SurveyEase",
                    "ConvertedCompYearly"]
    exclude_list += ["Knowledge_" + str(i) for i in range(1, 8)]
    exclude_list += ["Frequency_" + str(i) for i in range(1, 4)]
    exclude_list += ["TrueFalse_" + str(i) for i in range(1, 4)]
    is_numeric = ["YearsCode", "YearsCodePro", "ConvertedCompYearly", "WorkExp"]
    # df = remove_outliers(df, "ConvertedCompYearly")
    df = read_SO_dataset()
    tcp = TrendCherryPicker(query, partial_order, df, exclude_list, is_numeric, coverage_query, max_atoms=2)
    # tcp.generate_possible_views()
    # tcp.search_trend_views("data/SO/trend_results/edlevel_trend_preds_disj_of_2atom_conj.csv")
    tcp.search_trend_views("data/SO/trend_results/edlevel_trend_preds_2atom.csv")
