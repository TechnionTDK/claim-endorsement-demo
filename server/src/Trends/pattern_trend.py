import itertools
import os
import sys
import time
import sqlalchemy
import pandas as pd
from tqdm import tqdm

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import age_bucketize, remove_outliers, get_outliers
from Trends.DT_pattern_finder import DecisionTreePatternFinder
from QueryRunner import SQLEngineSingleton
#from ClaimEndorseFunctions import Bucket
# from SO_Experimenting import value_cleaning_SO, is_multivalue_attr, safe_split
# from config import *


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


def conjunct_to_sql_cond(conj):
    # list of tuples of the form (A, sign, v)
    template = """ "{a}"{sign}'{v}' """
    s = " AND ".join([template.format(a=a, sign=sign, v=clean_value(v)) for a, sign, v in conj])
    return f"({s})"


def disjunct_to_sql_cond(disj):
    # a disjunction is a tuple of lists of tuples.
    # each list of tuples represents a conjunct.
    return " OR ".join([conjunct_to_sql_cond(conj) for conj in disj])


def sign_to_pandas_sign(sign_str):
    if sign_str == '=':
        return '=='
    return sign_str


def agg_to_pandas_agg(agg_str):
    if agg_str == 'AVG':
        return 'mean'
    return agg_str


def conjunct_to_pandas_cond(conj):
    # list of tuples of the form (A, sign, v)
    template = """ {a}{sign}'{v}' """
    s = " and ".join([template.format(a=a, sign=sign_to_pandas_sign(sign), v=v) for a, sign, v in conj])
    return f"({s})"


def disjunct_to_pandas_cond(disj):
    # a disjunction is a tuple of lists of tuples.
    # each list of tuples represents a conjunct.
    return " or ".join([conjunct_to_pandas_cond(conj) for conj in disj])


def num_atoms_in_disj(disj):
    return sum([len(conj) for conj in disj])


def clean_value(value):
    if type(value) == str:
        return value.replace("'", "''")
    return value


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
        #self.df = df
        b = len(df)
        self.df = df[(~df[self.gb_attr].isna()) & (~df[self.outcome_attr].isna())]
        a = len(self.df)
        print(f"keeping {a}/{b} rows where outcome and gb attrs are not null.")
        self.partial_order = sorted([a for a in self.df[self.gb_attr].unique() if not pd.isna(a)])
        self.data_size = len(self.df)
        self.include = conf['include']
        self.numeric = conf['numeric']
        #self.bucket_objects = make_buckets(is_numeric)
        self.coverage_query = conf['coverage_query']
        self.max_atoms = conf['max_atoms']
        self.conf = conf

    def evaluate_gb_query(self, pred):
        if self.use_sql_db:
            query = sqlalchemy.text(self.gb_query.format(cond=disjunct_to_sql_cond(pred)))
            query_result = self.engine.execute(query)
            query_result = dict(list(query_result))
            return query_result
        # Use the dataframe
        subset = self.df.query("not (" + disjunct_to_pandas_cond(pred) + ")")
        agg_func = agg_to_pandas_agg(self.conf['agg'])
        query_result = subset.groupby(self.gb_attr)[self.outcome_attr].agg(agg_func).to_dict()
        return query_result

    def evaluate_coverage_query(self, pred):
        if self.use_sql_db:
            coverage_query_result = self.engine.execute(self.coverage_query.format(cond=disjunct_to_sql_cond(pred)))
            coverage = list(coverage_query_result)[0][0]
            return coverage
        # evaluate against df
        subset = self.df.query(disjunct_to_pandas_cond(pred))
        return len(subset)

    def check_view(self, pred):
        # TODO: optimization - incremental removal.
        # remove the pred
        # calculate the query results.
        # query = sqlalchemy.text(self.gb_query.format(cond=disjunct_to_sql_cond(pred)))
        # query_result = self.engine.execute(query)
        # query_result = dict(list(query_result))
        query_result = self.evaluate_gb_query(pred)
        # Validate the partial order over the results.
        for i in range(len(self.partial_order)-1):
            g = self.partial_order[i]
            g_next = self.partial_order[i+1]
            if g not in query_result or g_next not in query_result:
                continue
            try:
                if query_result[g] > query_result[g_next]:
                    return None, None, None, None
            except:
                print(f"check_view: problem with {pred}")
        # check coverage
        #coverage_query_result = self.engine.execute(self.coverage_query.format(cond=pred))
        #coverage = list(coverage_query_result)[0][0]
        coverage = self.evaluate_coverage_query(pred)
        res = [query_result[g] if g in query_result else None for g in self.partial_order]
        num_empty_groups = res.count(None)
        return res, coverage, num_atoms_in_disj(pred), num_empty_groups

    def generate_possible_views(self):
        s1 = time.time()
        # simple - one atom, and then complicate
        single_atoms = {}
        # TODO: support numeric attributes instead of ignoring them
        #subset_df = self.df[(~self.df[self.gb_attr].isna()) & (~self.df[self.outcome_attr].isna())]
        cols_for_pattern = [c for c in self.include if c not in self.numeric]
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
        print(f"Finished generating {len(atoms)} atoms in {s2-s1} seconds")
        conjunctions = {1: [[a] for a in atoms]}
        for i in range(2, self.max_atoms + 1):
            conjunctions[i] = []
            # Create all conjunctions (of size i) that are not empty.
            # First, create attribute combinations of size i
            attr_combs = itertools.combinations(cols_for_pattern, i)
            # For each one, find all value combinations.
            for attr_comb in attr_combs:
                value_combs = self.df[list(attr_comb)].value_counts().index
                for vc in value_combs:
                    # create all equality conjunctions.
                    conjunctions[i].append([(attr_comb[j], "=", vc[j]) for j in range(i)])

        all_conjunctions = flatten_extend(conjunctions.values())
        s3 = time.time()
        print(f"Finished generating {len(all_conjunctions)} conjunctions in {s3-s1} seconds after atom creation.")
        disjunctions = []
        if self.conf['enable_dnf']:
            max_atoms = self.max_atoms
        else:
            max_atoms = 1

        for m in range(1, max_atoms + 1):
            print(f"Creating DNFs with m={m}. Note that DNFs with m=1 are just conjunctions.")
            disjunctions_m = itertools.combinations(all_conjunctions, m)
            # print(f"Next, iterate over {len(list(disjunctions_m))} possibilities")
            for disj in tqdm(disjunctions_m):
                if num_atoms_in_disj(disj) <= self.max_atoms:
                    disjunctions.append(disj)

        if self.conf['enable_disjunctions']:
            for m in range(1, self.max_atoms + 1):
                print(f"Creating disjunctions of atoms with m={m}")
                disjunctions.extend(itertools.combinations(conjunctions[1], m))

        print(f"Found {len(all_conjunctions)} conjunctive predicates, {len(disjunctions)} total predicates of up to {self.max_atoms} atoms.")
        return disjunctions

    def search_trend_views(self, output_path):
        t = "\t"
        s1 = time.time()
        preds = self.generate_possible_views()
        s2 = time.time()
        print(f"Generating all predicates took {s2-s1} seconds.")
        with open(output_path, "w") as f:
            order_str = t.join([str(x) for x in self.partial_order])
            f.write(f"excluded_pred{t}coverage{t}num_atoms{t}num_empty{t}{order_str}\n")
        #preds = [([('Country', '=', 'United States of America')], [('OfficeStackAsyncHaveWorkedWith', '=', 'Adobe Workfront')])]
        for pred in tqdm(preds):
            res, coverage, num_atoms, num_empty = self.check_view(pred)
            if res is not None:
                print(pred)
                with open(output_path, "a") as f:
                    f.write(f"{disjunct_to_sql_cond(pred)}{t}{coverage/self.data_size}{t}{num_atoms}{t}{num_empty}{t}{t.join([str(x) for x in res])}\n")
        s3 = time.time()
        print(f"Finished the search, time: {s3-s2} seconds. Total time: {s3-s1} seconds.")


# def read_SO_dataset():
#     processed_path = os.path.join("../data/SO", "temp_df_for_sql_only_single_value.csv")
#     if os.path.exists(processed_path):
#         df = pd.read_csv(processed_path, index_col=0)
#         return df
#     df = pd.read_csv("../data/SO/survey_results_public.csv", index_col=0)
#     df = value_cleaning_SO(df)
#     # removing multivalue attrs.
#     df = df[[col for col in df.columns if (not is_multivalue_attr(df, col))]]
#     #for col in df.columns:
#     #    if is_multivalue_attr(df, col):
#     #        print(f"Taking first value from multivalue attr: {col}")
#     #        df[col] = df[col].apply(safe_split)
#     df.to_csv(processed_path)
#     df = pd.read_csv(processed_path, index_col=0)
#     print(f"{len(df.columns)} columns remain")
#     return df


def bucketize(x, thresholds, labels=None):
    # labels should be longer than thresholds by 1 item.
    for i, t in enumerate(thresholds):
        if x <= t:
            if labels is not None:
                return labels[i]
            return i+1  # default labels: 1,2,3,...
        if x > thresholds[-1]:
            if labels is not None:
                return labels[len(thresholds)]
            return len(thresholds)+1


def bmi_bucketize(x):
    return bucketize(x, [24.9, 29.9, 39.9])


# def bmi_bucketize(x):
#     if x <= 24.9:
#         return 1
#     if x <= 29.9:
#         return 2
#     if x <= 39.9:
#         return 3
#     if x > 40:
#         return 4

def read_SO_and_conf():
    df = pd.read_csv("data/SO/temp_df_for_sql.csv", index_col=0)
    edlevel_to_number = {'Primary/elementary school': 1, 'Secondary school': 2, 'Bachelor’s degree': 3,
                         'Master’s degree': 4, 'Other doctoral degree (Ph.D., Ed.D., etc.)': 5}
    df['edlevelnum'] = df['EdLevel'].apply(edlevel_to_number.get)
    conf = {'database_name': 'stack_overflow',
            'use_sql': True,
            'agg': 'AVG',
            'gb_attr': 'edlevelnum',
            'outcome_attr': 'ConvertedCompYearly',
            # 'include': ['Gender', 'DevType', 'OrgSize'],
            'include': ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'LearnCode', 'LearnCodeOnline', 'LearnCodeCoursesCert', 'YearsCode', 'YearsCodePro', 'DevType', 'OrgSize', 'PurchaseInfluence', 'BuyNewTool', 'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith', 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith', 'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith', 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSysProfessional use', 'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction', 'OfficeStackAsyncHaveWorkedWith', 'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith', 'OfficeStackSyncWantToWorkWith', 'Blockchain', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth', 'ICorPM', 'WorkExp', 'TimeSearching'],
            'string_cols': ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'LearnCode', 'OrgSize',
                            'LearnCodeOnline', 'LearnCodeCoursesCert', 'DevType', 'PurchaseInfluence', 'BuyNewTool',
                            'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith',
                            'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith',
                            'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith',
                            'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith',
                            'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSysProfessional use',
                            'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction', 'OfficeStackAsyncHaveWorkedWith',
                            'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith', 'OfficeStackSyncWantToWorkWith',
                            'Blockchain', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth',
                            'ICorPM', 'TimeSearching'],
            'max_atoms': 2,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ["YearsCode", "YearsCodePro", "ConvertedCompYearly", "WorkExp"],
            }
    conf['gb_query'] = f"""SELECT "{conf['gb_attr']}",{conf['agg']}("{conf['outcome_attr']}") FROM my_table WHERE "{conf['outcome_attr']}" IS NOT NULL """ + \
                        "AND NOT ({cond}) " + \
                        f"""GROUP BY "{conf['gb_attr']}";"""
    conf['coverage_query'] = f"""SELECT COUNT("{conf['outcome_attr']}") FROM my_table WHERE "{conf['outcome_attr']}" IS NOT NULL AND """ + "{cond};"
    return df, conf


def read_german_and_conf():
    fields = ['checking_account_status', 'duration_months', 'credit_history', 'purpose', 'amount',
              'savings_account_status', 'present_employment_since', 'installment_rate', 'personal_status_and_sex',
              'other_debtors', 'present_residence_since', 'property', 'age_years', 'other_installment_plans',
              'housing', 'num_existing_credits_this_bank', 'job', 'num_dependants', 'telephone', 'foreign_worker',
              'good_or_bad']
    df = pd.read_csv("data/german_credit/german.data", delimiter=' ', header=None, names=fields)
    # df['personal_status'] = df['personal_status_and_sex'].apply(get_personal_status)
    # df['gender'] = df['personal_status_and_sex'].apply(get_gender)
    df['good_or_bad'] = df['good_or_bad'].apply({1: 1, 2: 0}.get)  # 1 - good, 2 - bad

    employment_to_num = {'A71': 0, 'A72': 1, 'A73': 2, 'A74': 3, 'A75': 4}
    df['present_employment_since'] = df['present_employment_since'].apply(employment_to_num.get)
    conf = {'database_name': '',
            'use_sql': False,
            'agg': 'AVG',
            'gb_attr': 'present_employment_since',
            'outcome_attr': 'good_or_bad',
            'include': [c for c in df.columns if c != 'good_or_bad'],
            'max_atoms': 3,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ['age_years', 'duration_months', 'amount', 'installment_rate', 'present_residence_since'],
            'gb_query': "",
            'coverage_query': ""}
    return df, conf


def read_hm_and_conf():
    a = pd.read_csv("data/hm/articles.csv", index_col=0)
    c = pd.read_csv("data/hm/customers.csv", index_col=0)
    t = pd.read_csv("data/hm/transactions.csv", index_col=0)
    t['month'] = t.t_dat.apply(lambda x: int(x.split("-")[1]))
    # Maybe add day?
    c['age_group'] = c['age'].apply(age_bucketize)
    c['age_group_order'] = c['age_group'].apply({'25-34': 5, '35-44': 4, '45-54': 3, '56-64': 2, '>65': 1}.get)
    t2 = t[t["month"] == 11]
    m = a.merge(t2, on='article_id').merge(c, on="customer_id")

    conf = {'database_name': '',
            'use_sql': False,
            'agg': 'count',
            'gb_attr': 'age_group_order',
            'outcome_attr': 't_dat',
            'include': [
                'prod_name', 'product_type_no', 'product_type_name', 'product_group_name', 'graphical_appearance_no',
                'graphical_appearance_name', 'colour_group_name', 'perceived_colour_value_name',
                'perceived_colour_master_name', 'department_no', 'department_name', 'index_code', 'index_name',
                'index_group_no', 'index_group_name', 'section_no', 'section_name', 'garment_group_no',
                'garment_group_name', 'detail_desc', 'price', 'sales_channel_id', 'FN', 'Active',
                'club_member_status', 'fashion_news_frequency', 'postal_code'],
            'max_atoms': 2,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ['price'],
            'gb_query': "",
            'coverage_query': ""}
    return m, conf


if __name__ == '__main__':
    # stack overflow + decision tree + outlier removal
    # df, conf = read_SO_and_conf()
    # ids_to_remove = get_outliers(df, 'ConvertedCompYearly')
    # #ids_to_remove = [61044, 72941, 202, 62027, 70523, 18923, 62224, 66496, 47934, 27426, 20250, 30824, 40790, 1799, 10331, 1889, 39216, 61968, 31042, 51600, 11639, 20938, 50406, 14795, 21415, 21480, 37697, 47086, 62235, 53498, 66811, 67034, 67855, 8344, 16127, 39444, 20165, 309, 1741, 5233]
    # real_ids_to_remove = [id for id in ids_to_remove if id in df['ResponseId'].values]
    # print(f"already removed during outlier removal: {set(ids_to_remove).difference(set(real_ids_to_remove))}, remaining: {real_ids_to_remove}")
    # conf["ids_to_remove"] = real_ids_to_remove
    # dt = DecisionTreePatternFinder(df, conf)
    # attrs = list(set(dt.find_prominent_attributes()))
    # print(f"Focusing search on these attributes: {attrs}")
    # conf["include"] = attrs
    # output_path = "data/SO/trend_results/edlevel_trend_preds_outliers_exclusion_3atom_conj+disj.tsv"

    # German credit
    #df, conf = read_german_and_conf()
    # output_path = "data/german_credit/trend_results/employment_trend_preds_3atom_disj.tsv"

    # H&M
    df, conf = read_hm_and_conf()
    output_path = "data/german_credit/trend_results/age_count_items_trend_preds_2atom.tsv"

    tcp = TrendCherryPicker(df, conf)
    # tcp.generate_possible_views()
    tcp.search_trend_views(output_path)

