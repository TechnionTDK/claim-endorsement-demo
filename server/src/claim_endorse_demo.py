import sqlalchemy

from ClaimEndorseFunctions import run_cherrypicking
import utils
import time

from QueryRunner import connect_sql_db
from constants import *
import pandas as pd
import json
import argparse
from dotenv import load_dotenv
from my_config import DOTENV_PATH
load_dotenv(dotenv_path=DOTENV_PATH)
METRICS_SUBSET = [DF_MI_STRING, DF_ANOVA_F_STAT_STRING, DF_COSINE_SIMILARITY_STRING, DF_COVERAGE_STRING, DF_PVALUE_STRING,]
MAX_ATOMS = 2

# path_prefix = "server/"
path_prefix = ""

db_name_to_config = {
    'ACS7': {
        "data_path": "data/Folkstable/SevenStates",
        #"dataframe_path": "data/Folkstable/SevenStates/Seven_States_grouped.csv",
        "dataframe_path": "data/Folkstable/SevenStates/Seven_States_grouped_disc.csv",
        #"string_cols": ['NAICSP_grouped', 'OCCP_grouped', 'RT', 'NAICSP', 'SOCP'],
        "string_cols": ['NAICSP_grouped', 'OCCP_grouped', 'RT', 'NAICSP', 'SOCP', 'age_disc',
                        'years_since_married_disc', 'wkhp_disc'],
        #"database_name": "ACS7_numeric",
        "database_name": "ACS7_disc",
        "target_attr": "PINCP",
        "translation_func": utils.make_translation_for_ACS,
        "exclude": ["SERIALNO", "PWGTP"] + [f"PWGTP{x}" for x in range(1, 81)] + [
            "PINCP", "INTP", "OIP", "PAP", "RETP", "SEMP", "SSIP", "SSP", "WAGP", "PERNP", "POVPIP", "ADJINC",
            "FPINCP", "FINTP", "FOIP", "FPAP", "FRETP", "FSEMP", "FSSIP", "FSSP", "FWAGP", "FPERNP", "SPORDER"],
        #"is_numeric": ['PINCP', "AGEP", 'CITWP', 'JWMNP', 'MARHYP', 'WKHP', 'YOEP', 'JWAP', 'JWDP'],
        "is_numeric": ['PINCP', 'JWMNP', 'YOEP', 'JWAP', 'JWDP'],
        "col_to_values_dict_path": "data/Folkstable/col_to_values.json",
        "where": "TRUE",
        "min_group_size_in_results": 30,
    },
    'SO': {
        "data_path": path_prefix+"data/SO",
        # "dataframe_path": "data/SO/survey_results_public.csv",
        #"dataframe_path": "data/SO/temp_df_for_sql.csv",
        "dataframe_path": path_prefix+"data/SO/SO_disc.csv",
        "string_cols": ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'EdLevel', 'LearnCode',
                   'LearnCodeOnline', 'LearnCodeCoursesCert', 'DevType', 'OrgSize', 'PurchaseInfluence', 'BuyNewTool',
                   'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith',
                   'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith',
                   'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith',
                   'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith',
                   'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSysProfessional use',
                   'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction', 'OfficeStackAsyncHaveWorkedWith',
                   'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith', 'OfficeStackSyncWantToWorkWith',
                   'Blockchain', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth',
                   'ICorPM', 'TimeSearching', 'YearsCode_disc', 'YearsCode_Pro_disc', 'WorkExp_disc'],
        #"database_name": "stack_overflow",
        "database_name": "SO_disc",
        "target_attr": "ConvertedCompYearly",
        "translation_func": utils.create_column_dictionary_for_SO,
        "exclude": ["ResponseId", "CompTotal", "CompFreq",
                    "Currency", "SOAccount", "NEWSOSites", "SOVisitFreq", "SOPartFreq", "SOComm", "TBranch",
                    "TimeAnswering", "Onboarding", "ProfessionalTech", "SurveyLength", "SurveyEase",
                    "ConvertedCompYearly", "VCHostingProfessional use", "VCHostingPersonal use", "YearsCode",
                    "YearsCodePro", "WorkExp"] + \
                   ["Knowledge_" + str(i) for i in range(1, 8)] +
                   ["Frequency_" + str(i) for i in range(1, 4)] +
                   ["TrueFalse_" + str(i) for i in range(1, 4)],
        "is_numeric": ["ConvertedCompYearly"],
        "col_to_values_dict_path": path_prefix+"data/SO/col_to_values.json",
        "where": "TRUE",
        "min_group_size_in_results": 10,
    },
    'FLIGHTS': {
        "data_path": "data/flights",
        "dataframe_path": "data/flights/flights_with_airports_disc.csv",
        "string_cols": ['AIRLINE', 'TAIL_NUMBER', 'ORIGIN_AIRPORT_CODE', 'ORIGIN_AIRPORT', 'ORIGIN_CITY', 'ORIGIN_STATE',
                        'ORIGIN_COUNTRY', 'DEST_AIRPORT_CODE', 'DEST_AIRPORT', 'DEST_CITY', 'DEST_STATE', 'DEST_COUNTRY',
                        'CANCELLATION_REASON', 'day_of_month', 'distance_disc', 'scheduled_departure_hour', 'departure_hour'],
        #"database_name": "flights_large",
        "database_name": "flights_disc",
        "target_attr": "DEPARTURE_DELAY",
        "translation_func": utils.make_translation_for_flights,
        "exclude": ['TAIL_NUMBER', 'CANCELLED', 'ORIGIN_AIRPORT_CODE',
                   'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
                    'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY', 'DELAYED', 'DEST_COUNTRY', 'ORIGIN_COUNTRY'],
        "is_numeric": ['DAY',
                       'SCHEDULED_DEPARTURE', 'DEPARTURE_TIME',
                       'DEPARTURE_DELAY', 'TAXI_OUT', 'WHEELS_OFF', 'SCHEDULED_TIME', 'ELAPSED_TIME', 'AIR_TIME',
                       'DISTANCE',
                       'WHEELS_ON', 'TAXI_IN', 'SCHEDULED_ARRIVAL', 'ARRIVAL_TIME', 'ARRIVAL_DELAY', 'AIR_SYSTEM_DELAY',
                       'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY', 'ORIGIN_LATITUDE',
                       'ORIGIN_LONGITUDE', 'DEST_LATITUDE', 'DEST_LONGITUDE'],
        "col_to_values_dict_path": "data/flights/col_to_values.json",
        "where": '"DEPARTURE_DELAY" > 10',
        "min_group_size_in_results": 30,
    },
    'H&M': {
        "data_path": "data/hm",
        "dataframe_path": "data/hm/merged.csv",
        "string_cols": ['prod_name', 'product_type_name', 'product_group_name', 'graphical_appearance_name',
                        'colour_group_name', 'perceived_colour_value_name', 'perceived_colour_master_name',
                        'department_name', 'index_name', 'index_group_name', 'section_name', 'garment_group_name',
                        'club_member_status', 'fashion_news_frequency'],
        "database_name": "hm",
        "target_attr": "price",
        "translation_func": utils.make_translation_for_hm,
        "exclude": ['article_id', 'product_code', 'product_type_no', 'graphical_appearance_no', 'colour_group_code',
                    'perceived_colour_value_id', 'perceived_colour_master_id', 'index_code', 'index_group_no',
                    'section_no', 'garment_group_no', 'detail_desc', 't_dat', 'customer_id', 'price', 'month', 
                    'age', # age is the called-for group by attribute - but possibly add it back and remove the actual gb attribute
                    'postal_code', 'prod_name', 'department_no'],
        "is_numeric": ['price'],
        "col_to_values_dict_path": "data/hm/col_to_values.json",
        "where": 'True',
        "min_group_size_in_results": 30,
    },
    'diabetes': {
        'data_path': 'data/diabetes2',
        "dataframe_path": "data/diabetes2/diabetes_prediction_dataset_binned_age.csv",
        "string_cols": ['smoking_history', 'gender', 'Age_Category', 'bmi_category'],
        "database_name": "diabetes",
        "target_attr": "diabetes",
        "translation_func": utils.make_translation_for_diabetes,
        "exclude": ['age', 'diabetes10', 'age_category_numeric_consecutive', 'age_category_numeric', 'bmi'],
        "is_numeric": ['age',  'bmi'],
        "col_to_values_dict_path": "data/diabetes2/col_to_values.json", # TODO create
        "where": 'True',
        "min_group_size_in_results": 5,
    },
    'zillow': {
        'data_path': 'data/zillow/zillow-prize-1',
        "dataframe_path": "data/zillow/zillow-prize-1/properties_2016_clean_binned.csv",
        "string_cols": ["bathroomcnt", "bedroomcnt", "calculatedfinishedsquarefeet", "fireplacecnt", "garagecarcnt",
                        "hashottuborspa", "regionidcity", "regionidcounty", "unitcnt", "fireplaceflag",
                        "year_range_built"],
        "database_name": "zillow",
        "target_attr": "taxvaluedollarcnt",
        "translation_func": utils.make_translation_for_zillow,
        "exclude": ['assessmentyear', 'basementsqft', 'buildingqualitytypeid', 'calculatedbathnbr',
                    'censustractandblock', 'decktypeid', 'finishedfloor1squarefeet', 'finishedsquarefeet12',
                    'finishedsquarefeet13', 'finishedsquarefeet15', 'finishedsquarefeet50', 'finishedsquarefeet6',
                    'fips', 'fullbathcnt', 'garagetotalsqft', 'landtaxvaluedollarcnt', 'latitude', 'longitude',
                    'lotsizesquarefeet', 'parcelid', 'poolsizesum', 'pooltypeid10', 'pooltypeid2', 'pooltypeid7',
                    'propertycountylandusecode', 'propertyzoningdesc', 'rawcensustractandblock', 'regionidneighborhood',
                    'regionidzip', 'roomcnt', 'structuretaxvaluedollarcnt', 'taxamount', 'taxdelinquencyflag',
                    'taxdelinquencyyear', 'taxvaluedollarcnt', 'threequarterbathnbr', 'yardbuildingsqft17',
                    'yardbuildingsqft26', 'year_range_built_numeric', 'yearbuilt'],
        # Is binning needed - controlled by is_numeric
        "is_numeric": [],
        "col_to_values_dict_path": "data/zillow/zillow-prize-1/col_to_values.json",
        "where": 'True',
        "min_group_size_in_results": 5,
    }
}

def string_to_int(s):
    try:
        return int(s)
    except ValueError:
        return s


def string_to_float(s):
    try:
        return float(s)
    except ValueError:
        return s


def verify_group_values(g1, g2, grp_attr, col_to_values_dict):
    grp_attr_values = col_to_values_dict[grp_attr]
    group_values = [g1, g2]
    for i in range(2):
        g = group_values[i]
        if g not in grp_attr_values:
            g = string_to_int(g)
            if type(g) == str:
                g = string_to_float(g)
            if g not in grp_attr_values:
                raise Exception(f"{g} not in value list for {grp_attr}.\nValid values are: {grp_attr_values}.")
        group_values[i] = g
    if group_values[0] in grp_attr_values and group_values[1] in grp_attr_values:
        return group_values[0], group_values[1]
    raise Exception(f"{group_values[0]} or {group_values[1]} not in value list for {grp_attr}.\nValid values are: {grp_attr_values}.")


def claim_endorse(db_name, agg_type, grp_attr, g1, g2, output_path):
    conf = db_name_to_config[db_name]
    if db_name == "zillow":
        df = pd.read_csv("data/zillow/zillow-prize-1/properties_2016_clean_binned.csv", index_col=0, dtype={'fireplacecnt': str})
    else:
        df = pd.read_csv(conf["dataframe_path"], index_col=0)

    trans_dict = conf["translation_func"](df.columns)
    allocation_flags = [col for col in df.columns if "allocation flag" in trans_dict[col]]
    exclude_list = conf["exclude"] + allocation_flags
    # print(f"exclude ({len(exclude_list)}) : {exclude_list}")
    col_to_values_dict = json.loads(open(conf["col_to_values_dict_path"], "r").read())
    g1, g2 = verify_group_values(g1, g2, grp_attr, col_to_values_dict)
    result_df = run_cherrypicking(df, exclude_list, conf["is_numeric"], trans_dict, metrics_subset=METRICS_SUBSET,
                                  output_path=output_path, main_table="my_table", sort_by='ALL_TOP_K_MERGED',
                                  sample_size=None,
                                  start_time=time.time(), target_attr=conf["target_attr"], grp_attr=grp_attr,
                                  compare_list=[utils.less_than_cmp, g1, g2], agg_type=agg_type,
                                  shuffle_iter_index=None,
                                  reference=None,
                                  progressive_output_path=output_path, where=conf["where"],
                                  string_cols=conf["string_cols"], max_atoms=MAX_ATOMS, db_name=conf["database_name"],
                                  data_path=conf["data_path"], dataframe_path=conf["dataframe_path"],
                                  min_group_size_in_results=conf["min_group_size_in_results"])


def get_original_query_result(db_name, agg_type, grp_attr, g1, g2, output_path):
    conf = db_name_to_config[db_name]
    target_attr = conf["target_attr"]
    agg_func = agg_type.upper() if agg_type != "mean" else "AVG"
    if agg_func == "MEDIAN":
        query_string = f"""SELECT "{grp_attr}", PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "{target_attr}"), count("{target_attr}")
                                   FROM my_table 
                                   WHERE "{grp_attr}" IN ('{g1}','{g2}') GROUP BY "{grp_attr}";"""
    else:
        query_string = f"""SELECT "{grp_attr}", {agg_func}("{target_attr}"), count("{target_attr}")
                           FROM my_table 
                           WHERE "{grp_attr}" IN ('{g1}','{g2}') GROUP BY "{grp_attr}";"""
    query = sqlalchemy.text(query_string)
    engine = connect_sql_db(conf["database_name"])
    with engine.connect() as conn:
        query_result = conn.execute(query)
    #query_result = engine.execute(query)
    res = [x for x in query_result]
    print(res)
    with open(output_path, "w") as out:
        out.write("{")
        out.write('"agg": {')
        for i, t in enumerate(res):
            out.write(f'"{t[0]}": {t[1]}')
            if i < len(res)-1:
                out.write(",")
        out.write("},\n")
        out.write('"count": {')
        for i, t in enumerate(res):
            out.write(f'"{t[0]}": {t[2]}')
            if i < len(res)-1:
                out.write(",")
        out.write("}")
        out.write("}")
        
        




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some parameters for claim_endorse.')
    parser.add_argument('--dbname', type=str, required=True, help='database identifier')
    parser.add_argument('--aggtype', type=str, required=True, help='Aggregate function')
    parser.add_argument('--grpattr', type=str, required=True, help='Group attribute')
    parser.add_argument('--g1', type=str, required=True, help='First comparison group')
    parser.add_argument('--g2', type=str, required=True, help='Second comparison group')
    
    args = parser.parse_args()
    g1=args.g1
    g2=args.g2
    
    
    output_paths = {
        "SO": "data/SO/results/demo_test.csv",
        "ACS7": "data/Folkstable/SevenStates/results/demo_test.csv",
        "FLIGHTS": "data/flights/results/demo_test.csv",
        "HM": "data/hm/results/demo_test.csv",
        "diabetes": "data/diabetes2/results/demo_test.csv",
        "zillow": "data/zillow/results/demo_test.csv"
    }

    #for now use mean, but change it to args.aggtype when you know what values to send
    #claim_endorse("ACS7", "mean", "SEX", 1, 2, "data/Folkstable/SevenStates/results/demo_test.csv")
    #claim_endorse("FLIGHTS","count","DAY_OF_WEEK",1,6,"data/flights/results/demo_test.csv")
    
    
    print("thi is the name")
    dbname = args.dbname
    if args.dbname == "HM":
        dbname = "H&M"
    print(dbname)

    print(args.aggtype)
    aggtype = args.aggtype
    if args.aggtype == "avg":
        aggtype = "mean"

    print(args.grpattr)
    print("---------------------------------------------------------------")
    print(args.g1)
    print(args.g2)
    print("---------------------------------------------------------------")
    print(output_paths[args.dbname])


    g1 = args.g1
    g2 = args.g2
    get_original_query_result(dbname, aggtype, args.grpattr, g1, g2, '../src/assets/demo_test_ORIGINAL.json')
    #claim_endorse("H&M", "count", "age", 25, 40, "data/SO/results/demo_test.csv")

    claim_endorse(dbname, aggtype, args.grpattr, g1, g2, output_paths[args.dbname])
    with open("done_filename.txt", "w") as f:
        f.write("done!")
