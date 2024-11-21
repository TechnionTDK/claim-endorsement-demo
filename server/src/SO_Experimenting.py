import os.path
import re
import sys

from ClaimEndorseFunctions import *



def value_cleaning_helper(x, old_vals_to_new_vals):
    if x in old_vals_to_new_vals:
        return old_vals_to_new_vals[x]
    return x


def value_cleaning_SO(df):
    """
    :param df: the dataframe
    :return: returns the dataframe but changes certain values to be more readable + remove nan columns
    """
    secondary_ed_org = "Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)"
    secondary_ed_new = "Secondary school"
    bachelors_org = "Bachelor’s degree (B.A., B.S., B.Eng., etc.)"
    bachelors_new = "Bachelor’s degree"
    masters_org = "Master’s degree (M.A., M.S., M.Eng., MBA, etc.)"
    masters_new = "Master’s degree"
    ed_level_d = {secondary_ed_org: secondary_ed_new, bachelors_org: bachelors_new, masters_org: masters_new}
    df["EdLevel"] = df["EdLevel"].apply(lambda v: value_cleaning_helper(v, ed_level_d))
    yc_d = {'More than 50 years': '50', 'Less than 1 year': '0'}
    df['YearsCode'] = df['YearsCode'].apply(lambda v: value_cleaning_helper(v, yc_d))
    df['YearsCodePro'] = df['YearsCodePro'].apply(lambda v: value_cleaning_helper(v, yc_d))

    attrs_before = set(df.columns)
    df = df.dropna(axis=1, how='all')
    attrs_after_drop = set(df.columns)
    print(f"Empty columns that were removed:{attrs_before.difference(attrs_after_drop)}")
    return df


def safe_split(s):
    if type(s) != str:
        return s
    return s.split(';')[0]


def read_dataset():
    processed_path = os.path.join(DATA_PATH, "temp_df_for_sql.csv")
    if os.path.exists(processed_path):
        df = pd.read_csv(processed_path, index_col=0)
        return df
    df = pd.read_csv(DATAFRAME_PATH, index_col=0)
    df = value_cleaning_SO(df)
    for col in df.columns:
        if is_multivalue_attr(df, col):
            print(f"Taking first value from multivalue attr: {col}")
            df[col] = df[col].apply(safe_split)
    df.to_csv(processed_path)
    df = pd.read_csv(processed_path, index_col=0)
    return df


def seperate_genders(df):
    # Makes any gender that is not "Man" or "Woman" into Other
    gender_column = df['Gender']
    gender_selection_list = ["Man", "Woman"]

    def simplify_gender(x):
        if x in gender_selection_list:
            return x
        return "Other"

    df['Gender_simplified'] = df['Gender'].apply(simplify_gender)
    # for i in range(gender_column.size):
    #     row = gender_column[i]
    #     if row not in gender_selection_list:
    #         df.at[i, 'Gender'] = "Other"
    # # print(df)
    return df


def woman_greater_than_man_devtype_split(df,pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="DevType", grp_attr="Gender_simplified",
                                        cmp_attr="ConvertedCompYearly", compare_list=[less_than_cmp, "Man", "Woman"],pvalue_filter=pvalue_filter)


def woman_greater_than_man_country_split(df,pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="Country", grp_attr="Gender_simplified",
                                        cmp_attr="ConvertedCompYearly", compare_list=[less_than_cmp, "Man", "Woman"],pvalue_filter=pvalue_filter)


def woman_greater_than_man_ethnicity_split(df,pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="Ethnicity", grp_attr="Gender_simplified",
                                        cmp_attr="ConvertedCompYearly", compare_list=[less_than_cmp, "Man", "Woman"],pvalue_filter=pvalue_filter)


def ethnicity_greater_than_rest(df,pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="Ethnicity", grp_attr="", cmp_attr="ConvertedCompYearly",
                                        compare_list=[less_than_cmp, False, True],pvalue_filter=pvalue_filter)


def highschool_greater_than_bachelors_devtype_split(df,pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="DevType", grp_attr="EdLevel",
                                        cmp_attr="ConvertedCompYearly",
                                        compare_list=[less_than_cmp,
                                                      "Bachelor’s degree",
                                                      "Secondary school",
                                                      ],pvalue_filter=pvalue_filter)


def highschool_greater_than_bachelors_country_split(df,pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="Country", grp_attr="EdLevel",
                                        cmp_attr="ConvertedCompYearly",
                                        compare_list=[less_than_cmp,
                                                      "Bachelor’s degree",
                                                      "Secondary school",
                                                      ],pvalue_filter=pvalue_filter)


def bachelors_greater_than_masters_devtype_split(df,pvalue_filter=False):
    return multichoice_attribute_cherrypicking(df=df, split_attr="DevType", grp_attr="EdLevel",
                                        cmp_attr="ConvertedCompYearly",
                                        compare_list=[less_than_cmp,
                                                      "Master’s degree",
                                                      "Bachelor’s degree",
                                                      ],pvalue_filter=pvalue_filter)


def are_black_greater_than_white_salary(df,pvalue_filter=False):
    ret = multichoice_subgroup_comparison_cherrypicking(df=df, split_attr="Ethnicity",
                                                        cmp_attr="ConvertedCompYearly",
                                                        compare_list=[less_than_cmp, "White", "Black"],pvalue_filter=pvalue_filter)
    print(ret)
    return ret


def any_greater_than_whites_salary(df,pvalue_filter=False):
    ret=multichoice_all_comparison_cherrypicking(df=sep_df, split_attr="Ethnicity",cmp_attr="ConvertedCompYearly",compare_list=[less_than_cmp,"White"],pvalue_filter=pvalue_filter)
    print(ret)
    return ret


def any_greater_than_blacks_salary(df,pvalue_filter=False):
    ret = multichoice_all_comparison_cherrypicking(df=sep_df, split_attr="Ethnicity", cmp_attr="ConvertedCompYearly", compare_list=[less_than_cmp, "Black"],pvalue_filter=pvalue_filter)
    print(ret)
    return ret





def bachelors_greater_than_masters_good_pvalue(df,pvalue_filter=True):
    check_if_true_for_good_pvalue(df=df, split_attr="DevType", grp_attr="EdLevel", cmp_attr="ConvertedCompYearly",
                                  compare_list=[less_than_cmp,
                                                "Master’s degree",
                                                "Bachelor’s degree",
                                                ], pvalue_filter=pvalue_filter)


def masters_greater_than_bachelors_good_pvalue(df, pvalue_filter=True):
    check_if_true_for_good_pvalue(df=df, split_attr="DevType", grp_attr="EdLevel", cmp_attr="ConvertedCompYearly",
                                  compare_list=[less_than_cmp,
                                                "Bachelor’s degree",
                                                "Master’s degree",
                                                ], pvalue_filter=pvalue_filter)


def secondary_greater_than_bachelors_good_pvalue(df,pvalue_filter=True):
    check_if_true_for_good_pvalue(df=df, split_attr="DevType", grp_attr="EdLevel", cmp_attr="ConvertedCompYearly",
                                  compare_list=[less_than_cmp,
                                                "Bachelor’s degree",
                                                "Secondary school",
                                                ],pvalue_filter=pvalue_filter)


def woman_greater_than_man__salary_devtype_split_good_pvalue(df,pvalue_filter=True):
    check_if_true_for_good_pvalue(df=df, split_attr="DevType", grp_attr="Gender_simplified",
                                  cmp_attr="ConvertedCompYearly", compare_list=[less_than_cmp, "Man", "Woman"],pvalue_filter=pvalue_filter
                                  )


def full_cherrypicking_women_greater_than_men_salary(df,exclude_list, is_numeric,translation_dict,pvalue_filter=False):
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="Gender_simplified", target_attr="ConvertedCompYearly",
                                                    compare_list=[less_than_cmp, "Man", "Woman"], aggr_list=[np.mean,"mean",sp.stats.ttest_ind],
                                                    exclude_list=exclude_list, is_numeric=is_numeric, pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_women_greater_than_men_count(df,exclude_list, is_numeric,pvalue_filter=False):
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="Gender_simplified", target_attr="Age",
                                                    compare_list=[less_than_cmp, "Man", "Woman"],
                                                    aggr_list=[np.ma.count, "count", None],
                                                    exclude_list=exclude_list, is_numeric=is_numeric,
                                                    pvalue_filter=pvalue_filter)


def full_cherrypicking_women_greater_than_men_salary_median(df, exclude_list, is_numeric,translation_dict,   pvalue_filter=False):
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="Gender_simplified", target_attr="ConvertedCompYearly",
                                                    compare_list=[less_than_cmp, "Man", "Woman"],
                                                    aggr_list=median_list,
                                                    exclude_list=exclude_list, is_numeric=is_numeric,
                                                    pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_highschool_greater_than_bach_salary_median(df, exclude_list, is_numeric, pvalue_filter=False):
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                    compare_list=[less_than_cmp,
                                                "Bachelor’s degree",
                                                "Secondary school",
                                                ],
                                                    aggr_list=median_list,
                                                    exclude_list=exclude_list, is_numeric=is_numeric,
                                                    pvalue_filter=pvalue_filter)


def full_cherrypicking_highschool_greater_than_bach_salary_median(df, exclude_list, is_numeric, translation_dict,
                                                                      pvalue_filter=False):
        return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                        compare_list=[less_than_cmp,
                                                               "Bachelor’s degree",
                                                               "Secondary school",
                                                               ],
                                                        aggr_list=median_list,
                                                        exclude_list=exclude_list, is_numeric=is_numeric,
                                                        pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_highschool_greater_than_bach_salary_mean(df, exclude_list, is_numeric,translation_dict,
                                                                  pvalue_filter=False):
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                    compare_list=[less_than_cmp,
                                                           "Bachelor’s degree",
                                                           "Secondary school",
                                                           ],
                                                    aggr_list=mean_list,
                                                    exclude_list=exclude_list, is_numeric=is_numeric,
                                                    pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_masters_greater_than_bach_salary_median(df, exclude_list, is_numeric, translation_dict,pvalue_filter=False):
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                    compare_list=[less_than_cmp,
                                                "Bachelor’s degree",
                                                "Master’s degree",
                                                ],
                                                    aggr_list=median_list,
                                                    exclude_list=exclude_list, is_numeric=is_numeric,
                                                    pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_masters_greater_than_bach_salary_mean(df, exclude_list, is_numeric,translation_dict, pvalue_filter=False):
        return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                        compare_list=[less_than_cmp,
                                                               "Bachelor’s degree",
                                                               "Master’s degree",
                                                               ],
                                                        aggr_list=mean_list,
                                                        exclude_list=exclude_list, is_numeric=is_numeric,
                                                        pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_bach_greater_than_masters_salary_median(df, exclude_list, is_numeric,translation_dict, pvalue_filter=False):
    attr_list = list(set(df.columns).difference(set(exclude_list + ["ConvertedCompYearly"])))
    time_before=time.time()
    MI_dict, Anova_dict = create_metrics_dictionary(df, attr_list, "ConvertedCompYearly", is_numeric)
    time_after=time.time()
    print(f"time to calculate anova and mi: {time_after-time_before}")
    sorted_by_anova = sorted(Anova_dict.keys(), key=lambda x: Anova_dict[x][0],reverse=True)
    output_path=os.path.join(DATA_PATH, "SO_bach_greater_master_salary_median_sorted_by_anova_pvalue.csv")
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                    compare_list=[less_than_cmp,
                                              "Master’s degree",
                                              "Bachelor’s degree"],
                                                    aggr_list=median_list,
                                                    exclude_list=exclude_list, is_numeric=is_numeric,
                                                    pvalue_filter=pvalue_filter, translation_dict=translation_dict, sorted_columns=sorted_by_anova,
                                                    MI_dict=MI_dict, Anova_dict=Anova_dict, output_path=output_path)


def full_cherrypicking_bach_greater_than_masters_salary_mean(df, exclude_list, is_numeric, translation_dict,
                                                             pvalue_filter=False):
    return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                    compare_list=[less_than_cmp,
                                                                  "Master’s degree",
                                                                  "Bachelor’s degree"
                                                                  ],
                                                    aggr_list=mean_list,
                                                    exclude_list=exclude_list, is_numeric=is_numeric,
                                                    pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_masters_greater_than_bach_salary_mean(df, exclude_list, is_numeric, translation_dict,
                                                                 pvalue_filter=False):
        return full_multichoice_attribute_cherrypicking(df=df, grp_attr="EdLevel", target_attr="ConvertedCompYearly",
                                                        compare_list=[less_than_cmp,
                                                               "Bachelor’s degree",
                                                               "Master’s degree"
                                                               ],
                                                        aggr_list=mean_list,
                                                        exclude_list=exclude_list, is_numeric=is_numeric,
                                                        pvalue_filter=pvalue_filter, translation_dict=translation_dict)


def full_cherrypicking_women_greater_men_mean_salary_chatgpt(df,exclude_list,is_numeric,translation_dict):
    fullsplit_with_chatgpt(full_cherrypicking_women_greater_than_men_salary, df, exclude_list, is_numeric,
                           translation_dict, create_sex_string)


def full_cherrypicking_highschool_greater_bach_mean_salary_chatgpt(df,exclude_list,is_numeric,translation_dict):
    fullsplit_with_chatgpt(full_cherrypicking_highschool_greater_than_bach_salary_mean, df, exclude_list, is_numeric,
                           translation_dict, create_education_string)


def full_cherrypicking_bach_greater_masters_mean_salary_chatgpt(df,exclude_list,is_numeric,translation_dict):
    fullsplit_with_chatgpt(full_cherrypicking_bach_greater_than_masters_salary_mean, df, exclude_list, is_numeric,
                           translation_dict, create_education_string)


def full_cherrypicking_masters_greater_bach_mean_salary_chatgpt(df, exclude_list, is_numeric, translation_dict):
        fullsplit_with_chatgpt(full_cherrypicking_masters_greater_than_bach_salary_mean, df, exclude_list, is_numeric,
                               translation_dict, create_education_string)


def full_cherrypicking_women_greater_men_median_salary_chatgpt(df,exclude_list,is_numeric,translation_dict):
    fullsplit_with_chatgpt(full_cherrypicking_women_greater_than_men_salary_median, df, exclude_list, is_numeric,
                           translation_dict, create_sex_string)


def full_cherrypicking_highschool_greater_bach_median_salary_chatgpt(df,exclude_list,is_numeric,translation_dict):
    fullsplit_with_chatgpt(full_cherrypicking_highschool_greater_than_bach_salary_median, df, exclude_list, is_numeric,
                           translation_dict, create_education_string)


def full_cherrypicking_bach_greater_masters_median_salary_chatgpt(df,exclude_list,is_numeric,translation_dict):
    fullsplit_with_chatgpt(full_cherrypicking_bach_greater_than_masters_salary_median, df, exclude_list, is_numeric,
                           translation_dict, create_education_string)


def full_cherrypicking_masters_greater_bach_median_salary_chatgpt(df,exclude_list,is_numeric,translation_dict):
    fullsplit_with_chatgpt(full_cherrypicking_masters_greater_than_bach_salary_median, df, exclude_list, is_numeric,
                           translation_dict, create_education_string)


def create_manual_translation():
    translation_dict = {
        "EdLevel": "Education Level",
        "LearnCodeCoursesCert": "Learn Code Courses Certification",
        "YearsCodePro": "Years Code Professionally",
        "DevType": "Developer Type",
        "OrgSize": "Organization Size",
        "CompTotal": "Compensation Total",
        "CompFreq": "Compensation Frequency",
        "MiscTechHaveWorkedWith": "Miscellaneous Technology Have Worked With",
        "MiscTechWantToWorkWith": "Miscellaneous Technology Want To Work With",
        "OpSysProfessional use": "Operating System Professional use",
        "OpSysPersonal use": "Operating System Personal use",
        "VCInteraction": "Version Control Interaction",
        "VCHostingPersonal use": "Version Control Hosting Personal use",
        "VCHostingProfessional use": "Version Control Hosting Professional use",
        "SOVisitFreq": "Stack Overflow Visit Frequency",
        "WorkExp": "Work Experience",
        "ConvertedCompYearly": "Salary",
    }
    return translation_dict


def hypdb_responsibility_scores(attr_list):
    d = {"BuyNewTool": 0.3422, "LanguageWantToWorkWith": 0.3313, "RemoteWork": 0.3265}
    s = 0
    for attr in attr_list:
        if attr in d:
            s += d[attr]
    return s


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    exclude_list = ["ResponseId", "CompTotal", "CompFreq",
                    "Currency", "SOAccount", "NEWSOSites", "SOVisitFreq", "SOPartFreq", "SOComm", "TBranch",
                    "TimeAnswering", "Onboarding", "ProfessionalTech", "SurveyLength", "SurveyEase",
                    "ConvertedCompYearly"]
    exclude_list += ["Knowledge_" + str(i) for i in range(1, 8)]
    exclude_list += ["Frequency_" + str(i) for i in range(1, 4)]
    exclude_list += ["TrueFalse_" + str(i) for i in range(1, 4)]

    is_numeric = ["YearsCode", "YearsCodePro", "ConvertedCompYearly", "WorkExp"]
    #df = remove_outliers(df, "ConvertedCompYearly")

    df = read_dataset()

    # This should only be done once!
    # print("Uploading to DB")
    # df_to_sql_DB(df)
    # sys.exit()

    # Max naturalness scores from m=2
    # [('YearsCode', 0.500920390946478), ('OpSysProfessional use', 0.500920390946478),
    #  ('YearsCodePro', 0.4336441202314436), ('Country', 0.4336441202314436), ('Employment', 0.4045873504312886),
    #  ('Ethnicity', 0.386169641957749), ('OrgSize', 0.3852105130416362), ('Accessibility', 0.3756537230105102),
    #  ('Trans', 0.373805095304658), ('DatabaseHaveWorkedWith', 0.3647864898742391),
    #  ('LanguageHaveWorkedWith', 0.3616866031069439), ('Gender', 0.3595693173547548),
    #  ('LanguageWantToWorkWith', 0.3555460844702112), ('DevType', 0.351129317760212),
    #  ('MentalHealth', 0.349616695722789), ('DatabaseWantToWorkWith', 0.3495114227954359), ('Age', 0.3489261576172283),
    #  ('WorkExp', 0.3448617721412054), ('MainBranch', 0.3442781667951601), ('OpSysPersonal use', 0.3418066570021112),
    #  ('WebframeWantToWorkWith', 0.3370216277761922), ('LearnCode', 0.3364528423133279),
    #  ('VersionControlSystem', 0.3360023943819384), ('WebframeHaveWorkedWith', 0.3358681934383589),
    #  ('MiscTechWantToWorkWith', 0.3351112852412241), ('BuyNewTool', 0.3334557826059255),
    #  ('LearnCodeCoursesCert', 0.3322969104158327), ('OfficeStackAsyncHaveWorkedWith', 0.3308086741776911),
    #  ('RemoteWork', 0.3268633265244821), ('MiscTechHaveWorkedWith', 0.3267365912445891),
    #  ('NEWCollabToolsWantToWorkWith', 0.3241222506542622), ('ToolsTechHaveWorkedWith', 0.3227633378516907),
    #  ('CodingActivities', 0.3225543631684364), ('NEWCollabToolsHaveWorkedWith', 0.3179818581744196),
    #  ('ToolsTechWantToWorkWith', 0.3161055859742518), ('PurchaseInfluence', 0.3148145667481934),
    #  ('PlatformHaveWorkedWith', 0.3132755775188917), ('PlatformWantToWorkWith', 0.3130875288271288),
    #  ('OfficeStackAsyncWantToWorkWith', 0.3125471792942276), ('Blockchain', 0.3092487676002359),
    #  ('VCInteraction', 0.3083669831477447), ('ICorPM', 0.3081543656095838), ('LearnCodeOnline', 0.3073270351550302),
    #  ('OfficeStackSyncHaveWorkedWith', 0.3064349400254583), ('OfficeStackSyncWantToWorkWith', 0.3020678976230554),
    #  ('Sexuality', 0.3014804716888042), ('TimeSearching', 0.3009555510018649)]

    selected = ['YearsCode', 'OpSysProfessional use', 'YearsCodePro', 'Country', 'Employment', 'Ethnicity', 'OrgSize', 'Accessibility', 'Trans', 'DatabaseHaveWorkedWith']
    exclude_list = [x for x in df.columns if x not in selected]

    remaining = [c for c in df.columns if c not in exclude_list and c not in is_numeric]
    print(f"{len(remaining)} remaining (string) cols after exclusion: {remaining}")
    translation_dict = create_column_dictionary_for_SO(df.columns)

    #df = remove_outliers(df, "ConvertedCompYearly")
    #df=df[["Age","ConvertedCompYearly","EdLevel"]]

    # save three random orders
    #shuffle_and_save(df, exclude_list, is_numeric, translation_dict, start_time, iters=3)
    #run_random_shuffle_over_full_table(df, exclude_list, is_numeric, translation_dict, 3, "Bsc_gt_Msc")

    ####################### main quality / best sample size experiment #################################
    #result_df = run_cherrypicking_with_config(df, exclude_list, is_numeric, translation_dict)
    #sys.exit()

    ############ sample size experiment ##################
    #run_sample_guided_experiment([0.05, 0.1], 3, df, exclude_list, is_numeric, translation_dict)

    ############## num tuples experiment #########################
    methods = ['original_order', 'random_shuffle:1', 'random_shuffle:2', 'random_shuffle:3',
               #'ALL_TOP_K_MERGED',
               '0.01sample:1', '0.01sample:2', '0.01sample:3', 'ALL_TOP_K_SERIAL', 'HYPDB']
    sample_sizes = range(10000, 50001, 5000)
    #num_tuples_vs_time_for_full_run(sample_sizes, df, exclude_list, is_numeric, translation_dict, methods)

    ############## num columns experiment #########################
    col_sample_sizes = range(5, 50, 5)
    # TODO repeat each sample size several times (to do an average later over the results)
    #num_columns_vs_time_for_full_run(col_sample_sizes, df, exclude_list, is_numeric, translation_dict, methods)

    ############## num atoms experiment #########################
    num_atoms = [1, 2, 3, 4, 5]
    num_atoms_vs_time_for_full_run(num_atoms, df, exclude_list, is_numeric, translation_dict, methods)
    sys.exit()

    ############# single metric experiment ######################
    # single_metric_exp(df, exclude_list, is_numeric, translation_dict)

    ################## Predicate Level ##########################
    #pred_level_cherrypicking(df, exclude_list, is_numeric, translation_dict)

    ################## Random Queries ###########################
    remaining = [c for c in df.columns if c not in exclude_list]
    target_attr = "ConvertedCompYearly"
    #random_queries = randomize_queries(10, remaining, is_numeric, df, target_attr)
    random_queries = [#('Ethnicity', [utils.less_than_cmp, "I don't know", 'Indian'], 'median'), # DONE
                      # TODO change to median!
                      #('LearnCodeCoursesCert', [utils.less_than_cmp, 'Pluralsight', 'Codecademy'], 'mean'),
                      #('NEWCollabToolsHaveWorkedWith', [utils.less_than_cmp, 'Visual Studio', 'Nano'], 'median'), # DONE
                      # TODO change to median
                      #('MentalHealth', [utils.less_than_cmp, 'I have a concentration and/or memory disorder (e.g., ADHD, etc.)', 'I have an anxiety disorder'], 'mean'),
                      #('OfficeStackSyncHaveWorkedWith', [utils.less_than_cmp, 'Mattermost', 'Zoom'], 'mean'),
                      #('Trans', [utils.less_than_cmp, 'Yes', 'Or, in your own words:'], 'mean'),
                      ('PlatformWantToWorkWith', [utils.less_than_cmp, 'DigitalOcean', 'VMware'], 'median'), 
                      ('LanguageWantToWorkWith', [utils.less_than_cmp, 'Groovy', 'PowerShell'], 'median'), 
                      ('LearnCodeCoursesCert', [utils.less_than_cmp, 'Udacity', 'Coursera'], 'median'), 
                      ('Accessibility', [utils.less_than_cmp, 'Or, in your own words:', 'Prefer not to say'], 'median'),
                     ]
    #print(random_queries)
    #for grp_attr, compare_list, agg_type in random_queries:
    #    run_multiple_methods_for_query(target_attr, grp_attr, compare_list, agg_type,
    #                                   df, exclude_list, is_numeric, translation_dict, methods, stop_at_recall=True)





