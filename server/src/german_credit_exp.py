from utils import *
import pandas as pd
from statsmodels.stats.proportion import proportions_ztest


def get_personal_status(personal_status_and_sex_code):
    mapping = {'A91': 'divorced/separated',
               'A92': 'divorced/separated/married',
               'A93': 'single',
               'A94': 'married/widowed',
               'A95': 'single',
               }
    return mapping[personal_status_and_sex_code]


def get_gender(personal_status_and_sex_code):
    if personal_status_and_sex_code in ('A91', 'A93', 'A94'):
        return 'male'
    if personal_status_and_sex_code in ('A92', 'A95'):
        return 'female'


def translate_to_readable_strings(df):
    trans = {'checking_account_status': {'A11': "<0", 'A12': "0-200", 'A13': ">=200", 'A14': "No account"},
             'credit_history': {'A30': "no credits taken / paid back duly",
                                'A31': 'all credits at this bank paid back duly',
                                'A32': 'existing credits paid back duly till now',
                                'A33': 'delay in paying off in the past',
                                'A34': 'critical account/other credits existing (not at this bank)'},
             'purpose': {'A40': 'car (new)', 'A41': 'car (used)', 'A42': 'furniture/equipment',
                         'A43': 'radio/television', 'A44': 'domestic appliances', 'A45': 'repairs', 'A46': 'education',
                         'A47': '(vacation - does not exist?)', 'A48': 'retraining', 'A49': 'business',
                         'A410': 'others'},
             # 'amount'
             'savings_account_status': {'A61': '<100', 'A62': '100-500', 'A63': '500-1000', 'A64': '>=1000',
                                        'A65': 'unknown/no savings account'},
             'present_employment_since': {'A71': 'unemployed', 'A72': '<1 yr', 'A73': '1-4 yrs', 'A74': '4-7 yrs',
                                          'A75': '>7 yrs'},
             # 'installment_rate',
             'other_debtors': {'A101': 'none', 'A102': 'co-applicant', 'A103': 'guarantor'},
             # 'present_residence_since',
             'property': {'A121': 'real estate', 'A122': 'savings agreement/life insurance', 'A123': 'car or other',
                          'A124': 'unknown/no property'},
             # 'age_years',
             'other_installment_plans': {'A141': 'bank', 'A142': 'stores', 'A143': 'none'},
             'housing': {'A151': 'own', 'A152': 'rent', 'A153': 'free'},
             # 'num_existing_credits_this_bank',
             'job': {'A171': 'unemployed/ unskilled - non-resident', 'A172': 'unskilled - resident',
                     'A173': 'skilled employee / official',
                     'A174': 'management/ self-employed/highly qualified employee/ officer'},
             # 'num_dependants',
             'telephone': {'A191': 'none', 'A192': 'yes, registered'},
             'foreign_worker': {'A201': 'yes', 'A202': 'no'},
             #'good_or_bad'
             }
    for k in trans:
        df[k] = df[k].apply(trans[k].get)
    return df


def read_german_credit_data():
    fields = ['checking_account_status', 'duration_months', 'credit_history', 'purpose', 'amount',
              'savings_account_status', 'present_employment_since', 'installment_rate', 'personal_status_and_sex',
              'other_debtors', 'present_residence_since', 'property', 'age_years', 'other_installment_plans',
              'housing', 'num_existing_credits_this_bank', 'job', 'num_dependants', 'telephone', 'foreign_worker',
              'good_or_bad']
    df = pd.read_csv("data/german_credit/german.data", delimiter=' ', header=None, names=fields)
    df['personal_status'] = df['personal_status_and_sex'].apply(get_personal_status)
    df['gender'] = df['personal_status_and_sex'].apply(get_gender)
    df['good_or_bad'] = df['good_or_bad'].apply(lambda x: {1: 'good', 2: 'bad'}[x])
    return df


def is_different_good_proportion(df, attr='gender', value1='male', value2='female', print_only_counter_examples=False,
                                 desc='\n'):
    all_v1 = len(df[df[attr] == value1])
    good_v1 = len(df[(df[attr] == value1) & (df['good_or_bad'] == 'good')])
    if all_v1 == 0:
        print(f"No {value1}s found in {desc}")
        return

    all_v2 = len(df[df[attr] == value2])
    good_v2 = len(df[(df[attr] == value2) & (df['good_or_bad'] == 'good')])
    if all_v2 == 0:
        print(f"No {value2}s found in {desc}")
        return

    p1 = good_v1 / all_v1
    p2 = good_v2 / all_v2

    if p1 < p2 or not print_only_counter_examples:
        print("\n")
        print(desc)
        stat, pval = proportions_ztest([good_v1, good_v2], [all_v1, all_v2])
        print(f"{value1}: N1={all_v1}, prop={p1}")
        print(f"{value2}: N2={all_v2}, prop={p2}")
        print(f"Difference pvalue {pval}")


def single_attribute_cherrypicking(df, attr, numeric=False):
    if numeric:
        # basic division to ranges
        interval = value_range_to_interval_size(df[attr].max())
        for i in range(0, df[attr].max(), interval):
            is_different_good_proportion(df[(i <= df[attr]) & (df[attr] <= i + interval)],
                                         print_only_counter_examples=True,
                                         desc=f"{attr}{i}-{i + interval}")
    else:
        values = df[attr].unique()
        for v in values:
            is_different_good_proportion(df[df[attr] == v], print_only_counter_examples=True, desc=f"{attr} = {v}")


def each_attribute_cherrypicking(df):
    exclude = ['gender',  # main claim
               'good_or_bad',  # label
               'personal_status_and_sex',  # problematic because of relation to gender attribute
               'personal_status',  # problematic because of relation to gender attribute
               ]
    numericals = ['amount', 'age_years', 'duration_months',
                  # 'present_residence_since' # numerical but values are only 1-4. Can be treated as categorical.
                  ]
    for c in df.columns:
        if c in exclude:
            continue
        if c in numericals:
            single_attribute_cherrypicking(df, c, numeric=True)
        else:
            single_attribute_cherrypicking(df, c, numeric=False)

# TODO: next step - union of multiple values under the same attribute with good results
# TODO: handle numericals
