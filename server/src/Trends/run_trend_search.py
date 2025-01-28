import pandas as pd
from pattern_trend import *
from pattern_trend_w_cache import *


def outlier_removal(df, outlier_percent, method, conf):
    if method == 'lof':
        clf = LocalOutlierFactor(n_neighbors=20, contamination=outlier_percent)
        df['outlier_label'] = clf.fit_predict(df[conf['outcome_attr']].values.reshape(-1, 1))
        b = len(df)
        df = df[df['outlier_label'] == 1]
        print(f"removed {b - len(df)} outlier rows ({outlier_percent}) (by LocalOutlierFactor)")
    elif method == 'quantile':
        # remove outlier_percent from the top values
        q = df[conf['outcome_attr']].quantile(1-outlier_percent)
        df = df[df[conf['outcome_attr']] < q]
    return df


def read_SO_and_conf(outlier_percent=0.02):
    conf = {'database_name': 'stack_overflow',
            'use_sql': False,  # True,
            'agg': 'AVG',
            'gb_attr': 'edlevelnum',
            'outcome_attr': 'ConvertedCompYearly',
            # 'include': ['Gender', 'DevType', 'OrgSize'],
            'include': ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'LearnCode', 'LearnCodeOnline',
                        'LearnCodeCoursesCert', 'YearsCode', 'YearsCodePro', 'DevType', 'OrgSize', 'PurchaseInfluence',
                        'BuyNewTool', 'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith',
                        'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith',
                        'PlatformWantToWorkWith', 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith',
                        'MiscTechHaveWorkedWith', 'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith',
                        'ToolsTechWantToWorkWith', 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith',
                        'OpSysProfessional use', 'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction',
                        'OfficeStackAsyncHaveWorkedWith', 'OfficeStackAsyncWantToWorkWith',
                        'OfficeStackSyncHaveWorkedWith', 'OfficeStackSyncWantToWorkWith', 'Blockchain', 'Age', 'Gender',
                        'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth', 'ICorPM', 'WorkExp',
                        'TimeSearching'],
            'string_cols': ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'LearnCode', 'OrgSize',
                            'LearnCodeOnline', 'LearnCodeCoursesCert', 'DevType', 'PurchaseInfluence', 'BuyNewTool',
                            'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith',
                            'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith',
                            'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith',
                            'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith',
                            'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSysProfessional use',
                            'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction',
                            'OfficeStackAsyncHaveWorkedWith',
                            'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith',
                            'OfficeStackSyncWantToWorkWith',
                            'Blockchain', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility',
                            'MentalHealth',
                            'ICorPM', 'TimeSearching'],
            'max_atoms': 2,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ["YearsCode", "YearsCodePro", "ConvertedCompYearly", "WorkExp"],
            'negate': True,
            'output_path': f"data/SO/trend_results/edlevel_trend_preds_outliers_exclusion_2atom_conj+disj_{outlier_percent}outlier.tsv",
            "gb_query": "",
            "coverage_query": "",
            "outlier_method": "lof",
            }
    # conf['gb_query'] = f"""SELECT "{conf['gb_attr']}",{conf['agg']}("{conf['outcome_attr']}") FROM my_table WHERE "{conf['outcome_attr']}" IS NOT NULL """ + \
    #                   "AND ({cond}) " + \
    #                   f"""GROUP BY "{conf['gb_attr']}";"""
    # conf['coverage_query'] = f"""SELECT COUNT("{conf['outcome_attr']}") FROM my_table
    #                              WHERE "{conf['outcome_attr']}" IS NOT NULL
    #                              AND "{conf['gb_attr']}" IS NOT NULL AND """ + "({cond});"
    # TODO: make a config class?
    df = pd.read_csv("data/SO/temp_df_for_sql.csv", index_col=0)
    edlevel_to_number = {'Primary/elementary school': 1, 'Secondary school': 2, 'Bachelor’s degree': 3,
                         'Master’s degree': 4, 'Other doctoral degree (Ph.D., Ed.D., etc.)': 5}
    df['edlevelnum'] = df['EdLevel'].apply(edlevel_to_number.get)
    b = len(df)
    df = df[~df['edlevelnum'].isna()]
    print(f"removed {b-len(df)} rows with null edlevelnum")
    b = len(df)
    df = df[~df["ConvertedCompYearly"].isna()]
    print(f"removed {b-len(df)} rows with null ConvertedCompYearly")
    if outlier_percent > 0:
        df = outlier_removal(df, outlier_percent, conf['outlier_method'], conf)
    return df, conf


def read_german_and_conf(outlier_percent=0):
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
            'include': [c for c in df.columns if c not in ('good_or_bad', 'present_employment_since')],
            'max_atoms': 3,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ['age_years', 'duration_months', 'amount'],
            'gb_query': "",
            'coverage_query': "",
            'negate': True,
            'outlier_method': 'lof',
            'output_path': "data/german_credit/trend_results/employment_trend_preds_3atom_disj_debug2.tsv",
            }
    if outlier_percent > 0:
        df = outlier_removal(df, outlier_percent, conf['outlier_method'], conf)
    return df, conf


def read_hm_and_conf(month=11, outlier_percent=0):
    output_path = f"data/hm/month{month}.csv"
    if os.path.exists(output_path):
        print(f"reading csv from {output_path}")
        m = pd.read_csv(output_path, index_col=0)
    else:
        print("Reading articles..")
        a = pd.read_csv("data/hm/articles.csv", index_col=0)
        print("Reading customers..")
        c = pd.read_csv("data/hm/customers.csv", index_col=0)
        print("Reading transactions..")
        t = pd.read_csv("data/hm/transactions.csv", index_col=0)
        t['month'] = t.t_dat.apply(lambda x: int(x.split("-")[1]))
        t['day_of_month'] = t.t_dat.apply(lambda x: int(x.split("-")[2]))
        # Maybe add day?
        c['age_group'] = c['age'].apply(age_bucketize)
        c['age_group_order'] = c['age_group'].apply({'25-34': 5, '35-44': 4, '45-54': 3, '56-64': 2, '>65': 1}.get)
        t2 = t[t["month"] == month]
        m = a.merge(t2, on='article_id').merge(c, on="customer_id")
        m['prod_name'] = m['prod_name'].apply(lambda x: x.replace("'", ""))
        m['FN'] = m['FN'].fillna(0)
        m.to_csv(output_path)
    conf = {'database_name': '',
            'use_sql': False,
            # 'agg': 'count',
            'agg': 'sum',
            'gb_attr': 'age_group_order',
            #'outcome_attr': 't_dat',
            'outcome_attr': 'price',
            'include': [
                'prod_name',
                # 'product_type_no',
                'product_type_name', 'product_group_name',  # 'graphical_appearance_no',
                'graphical_appearance_name', 'colour_group_name', 'perceived_colour_value_name',
                'perceived_colour_master_name', 'department_no', 'department_name',  # 'index_code',
                'index_name',
                # 'index_group_no',
                'index_group_name',  # 'section_no',
                'section_name',  # 'garment_group_no',
                'garment_group_name',
                # 'detail_desc',
                # 'price', # TODO bring it back
                'sales_channel_id', 'FN', 'Active',
                'club_member_status', 'fashion_news_frequency',
                #'postal_code'
            ],
            'max_atoms': 2,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ['price'],
            'gb_query': "",
            'coverage_query': "",
            'negate': True,
            'outlier_method': 'lof',
            }
    conf["string_cols"] = [c for c in conf["include"] if c != 'price']
    # remove nans from group by attribute.
    m = m[~m[conf['gb_attr']].isna()]
    if outlier_percent > 0:
        m = outlier_removal(m, outlier_percent, conf['outlier_method'], conf)
    return m, conf


def age_to_age_group(x):  # edit for a decreasing trend
    # if 25 <= x < 30:
    #     return 1
    # if 30 <= x < 35:
    #     return 2
    # if 35 <= x < 40:
    #     return 3
    if x > 40 or x < 25:
        return None
    return x


def read_hm_and_conf2(month, outlier_percent=0):
    output_path = 'data/hm/merged.csv'
    if os.path.exists(output_path):
        m = pd.read_csv(output_path, index_col=0)
    else:
        print("Reading articles..")
        a = pd.read_csv("data/hm/articles.csv", index_col=0)
        print("Reading customers..")
        c = pd.read_csv("data/hm/customers.csv", index_col=0)
        print("Reading transactions..")
        t = pd.read_csv("data/hm/transactions.csv", index_col=0)
        t['month'] = t.t_dat.apply(lambda x: int(x.split("-")[1]))
        t['day_of_month'] = t.t_dat.apply(lambda x: int(x.split("-")[2]))
        #c['age_group'] = c['age'].apply(age_bucketize)
        #c['age_group_order'] = c['age'].apply({25 + i: 16 - i for i in range(16)}.get)

        #c['age_group_order'] = c['age_group'].apply({'25-34': 5, '35-44': 4, '45-54': 3, '56-64': 2, '>65': 1}.get)
        #t2 = t[t["month"] == 11]
        m = a.merge(t, on='article_id').merge(c, on="customer_id")
        m['prod_name'] = m['prod_name'].apply(lambda x: x.replace("'", ""))
        m['FN'] = m['FN'].fillna(0)
        m.to_csv("data/hm/merged.csv")
    m['age_group_order'] = m['age'].apply(age_to_age_group)
    m['age_group_order_rev'] = m['age_group_order'].apply(lambda x: 40 - x)
    if month is not None:
        m = m[m['month'] == month]

    conf = {'database_name': '',
            'use_sql': False,
            'agg': 'sum',
            'gb_attr': 'age_group_order',
            'outcome_attr': 'price',
            'output_path': f'data/hm/trend_results/month{month}_sum_price_gb_age25-40_2atoms_conj_disj.tsv',
            'include': [
                'prod_name',
                # 'product_type_no',
                'product_type_name', 'product_group_name',  # 'graphical_appearance_no',
                'graphical_appearance_name', 'colour_group_name', 'perceived_colour_value_name',
                'perceived_colour_master_name', 'department_no', 'department_name',  # 'index_code',
                'index_name',
                # 'index_group_no',
                'index_group_name',  # 'section_no',
                'section_name',  # 'garment_group_no',
                'garment_group_name',
                # 'detail_desc',
                # 'price', # TODO bring it back
                'sales_channel_id', 'FN', 'Active',
                'club_member_status', 'fashion_news_frequency',
                #'postal_code',
                'day_of_month',
                #'month',
            ],
            'max_atoms': 2,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ['price'],
            'gb_query': "",
            'coverage_query': "",
            'negate': True,
            'outlier_method': 'lof',
            }
    conf["string_cols"] = [c for c in conf["include"] if c != 'price']
    # remove nans from group by attribute.
    m = m[~m[conf['gb_attr']].isna()]
    if outlier_percent > 0:
        m = outlier_removal(m, outlier_percent, conf['outlier_method'], conf)
    return m, conf


def read_zillow_and_conf(outlier_percent=0, outlier_method="LOF"):
    conf = {'database_name': '',
            'use_sql': False,
            'agg': 'median',
            # 'agg': 'avg',
            #'gb_attr': 'roomcnt',
            # 'gb_attr': 'total_area_bucket',
            'gb_attr': 'year_range_built',
            # 'partial_order': ['<1985', '1985-1990', '1990-1995', '1995-2000', '2000-2005', '2005-2010', '2010-2015'],
            'partial_order': ['1985-1989', '1990-1994', '1995-1999', '2000-2004', '2005-2009', '2010-2014'],
            'outcome_attr': 'taxvaluedollarcnt',
            'include': ['airconditioningtypeid', 'architecturalstyletypeid', 'bathroomcnt', 'bedroomcnt',
                        #'buildingclasstypeid', - all Nones
                        'buildingqualitytypeid', 'calculatedbathnbr', 'decktypeid',
                        'fips',  # county
                        'fireplacecnt',
                        'fullbathcnt', 'garagecarcnt',  'hashottuborspa',
                        'heatingorsystemtypeid', #'latitude', 'longitude',
                        'poolcnt', 'poolsizesum', 'pooltypeid10', 'pooltypeid2', 'pooltypeid7',
                        'propertycountylandusecode', 'propertylandusetypeid',
                        'propertyzoningdesc', 'regionidcity',
                        'regionidcounty', 'regionidneighborhood', 'regionidzip',
                        'roomcnt',
                        'storytypeid', 'threequarterbathnbr', 'typeconstructiontypeid', 'unitcnt',
                        #'yearbuilt',
                        'numberofstories', 'fireplaceflag',
                        'assessmentyear',
                        #'taxamount',
                        #'taxdelinquencyflag', 'taxdelinquencyyear',
                        #'censustractandblock', 'rawcensustractandblock',
                        #'basementsqft', 'finishedfloor1squarefeet', 'calculatedfinishedsquarefeet',
                        #'finishedsquarefeet12', 'finishedsquarefeet13', 'finishedsquarefeet15',
                        #'finishedsquarefeet50', 'finishedsquarefeet6', 'garagetotalsqft', 'lotsizesquarefeet',
                        #'yardbuildingsqft17', 'yardbuildingsqft26',
                        #'structuretaxvaluedollarcnt'
                        ],
            #'include': ['bathroomcnt'],
            'max_atoms': 3,
            'enable_disjunctions': True,
            'enable_dnf': False,
            'numeric': ['basementsqft', 'finishedfloor1squarefeet', 'calculatedfinishedsquarefeet',
                        'finishedsquarefeet12', 'finishedsquarefeet13', 'finishedsquarefeet15',
                        'finishedsquarefeet50', 'finishedsquarefeet6', 'garagetotalsqft', 'lotsizesquarefeet',
                        'yardbuildingsqft17', 'yardbuildingsqft26',
                        #'structuretaxvaluedollarcnt'
                        ],
            'gb_query': "",
            'coverage_query': "",
            'negate': True,
            'outlier_method': 'lof',
            'output_path': f"data/zillow/trend_results/yearbuilt_median_value_trend_preds_3atoms_outlier_percent{outlier_percent}_greedy.tsv",
            }
    conf['string_cols'] = [c for c in conf['include'] if c not in conf['numeric']]
    df = pd.read_csv("data/zillow/zillow-prize-1/properties_2016.csv", index_col=0)
    # bucket = Bucket(100, 5300, 10)
    # df['total_area_bucket'] = df['calculatedfinishedsquarefeet'].apply(
    #     lambda x: bucket.bucket_to_range_string(bucket.value_to_bucket_id(x)))
    df = df[df['yearbuilt'] >= 1985]
    # df = df[(df['roomcnt'] >= 2) & (df['roomcnt'] <= 6)]
    df['year_range_built'] = df['yearbuilt'].apply(year_bucketize)
    print(df[['yearbuilt', 'year_range_built']].head())
    print(df['year_range_built'].value_counts())
    b = len(df)
    df = df[~df[conf['outcome_attr']].isna()]
    print(f"removed {b-len(df)} rows with empty {conf['outcome_attr']}")
    if outlier_percent > 0:
        df = outlier_removal(df, outlier_percent, conf['outlier_method'], conf)
    return df, conf


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

    # German credit
    #df, conf = read_german_and_conf()
    # removed = run_dynamic_prog_tuple_deletion(df, conf)
    # print(f"Found {len(removed)} tuples to remove")
    # sys.exit()

    # H&M
    #df, conf = read_hm_and_conf2(month=5)
    #conf["ids_to_remove"] = df[(df.age_group_order == 3) | (df.age_group_order == 4)].index
    #dt = DecisionTreePatternFinder(df, conf)
    #attrs = list(set(dt.find_prominent_attributes()))
    #print(f"Focusing search on these attributes: {attrs}")
    #conf["include"] = attrs


    # Zillow housing
    df, conf = read_zillow_and_conf()
    # ids_to_remove = eval(open("data/zillow/zillow_2016_remove_ids_gb_year_range.txt", "r").read())
    # print(len(ids_to_remove))
    # conf["ids_to_remove"] = ids_to_remove
    # dt = DecisionTreePatternFinder(df, conf)
    # attrs = list(set(dt.find_prominent_attributes()))
    # print(f"Focusing search on these attributes: {attrs}")
    # conf["include"] = attrs

    # attrs = calc_anova_and_get_top_attrs(df, conf, num_top_attrs_to_return=5)
    #conf['include'] = attrs
    #conf['include'] = ['calculatedbathnbr', 'fips', 'regionidcounty', 'regionidcity', 'threequarterbathnbr', 'bedroomcnt', 'garagecarcnt', 'regionidzip', 'fireplacecnt', 'propertylandusetypeid', 'propertycountylandusecode', 'airconditioningtypeid', 'heatingorsystemtypeid', 'yearbuilt', 'regionidneighborhood', 'numberofstories', 'typeconstructiontypeid', 'assessmentyear', 'architecturalstyletypeid']

    #removed = run_greedy_tuple_deletion(df, conf)
    #print(f"removed {removed} tuples")
    #sys.exit()

    tcp = TrendCherryPicker(df, conf)
    # tcp = TrendCherryPickerOptimized(df, conf)
    # tcp.generate_possible_views()
    # tcp.search_trend_views(conf["output_path"])
    tcp.greedy_search_trend_views(conf["output_path"], beam_size=100)

