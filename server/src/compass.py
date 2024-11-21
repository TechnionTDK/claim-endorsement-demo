from ClaimEndorseFunctions import *
import sqlite3 as sql

def female_greater_than_male_race_split(df, pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="race", grp_attr="sex",
                                               cmp_attr="two_year_recid",
                                               compare_list=[less_than_cmp,
                                                             "Male",
                                                             "Female",
                                                             ], pvalue_filter=pvalue_filter)

def white_greater_than_black_age_cat_split(df, pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="age_cat", grp_attr="race",
                                               cmp_attr="two_year_recid",
                                               compare_list=[less_than_cmp,
                                                             "African-American",
                                                             "Caucasian",
                                                             ], pvalue_filter=pvalue_filter)

def white_greater_than_hispanic_age_cat_split(df, pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="age_cat", grp_attr="race",
                                               cmp_attr="two_year_recid",
                                               compare_list=[less_than_cmp,
                                                             "Hispanic",
                                                             "Caucasian",
                                                             ], pvalue_filter=pvalue_filter)

exclude_list = ['id','name','first','last', 'r_case_number', 'vr_case_number', 'compas_screening_date', 'dob']
is_numeric = []

if __name__ == '__main__':

    df=pd.read_csv("data/compas/compas-scores-two-years.csv")
    #df_to_sql_DB(df)
    trans_dict = {x:x for x in df.columns}
    result_df = run_cherrypicking_with_config(df, exclude_list, is_numeric, trans_dict)


    # print(df)
    # gb=df.groupby(["race","sex"])["id"].count()
    # print(gb)
    # female_greater_than_male_race_split(df)
    #white_greater_than_black_age_cat_split(df)
    #white_greater_than_hispanic_age_cat_split(df)
    
    #con = sql.connect("data/Compas/compas.db")
    #cur = con.cursor()
    #df = pd.read_sql_query("SELECT * from compas", con)
    #print(len(df))
    #x=5



