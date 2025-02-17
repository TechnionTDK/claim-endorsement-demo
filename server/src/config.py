import os
from constants import *
import utils

RUN_ACS7 = False
RUN_CHICAGO = False
RUN_SO = True
RUN_FLIGHTS = False
RUN_COMPAS = False

RUN_ACTUAL_CP = True
CREATE_FIGURES = False  #chicago is not ready for creating figures
MAX_ATOMS = 2
STOP_AT_TIME = None #60*20  # 20 minutes
REMOVE_NULL_PREDICATES = True
PVALUE_FILTER = False
USE_SQL = True
WHERE = 'TRUE' # default - no condition

# SORT_BY = DF_COSINE_SIMILARITY_STRING
# SORT_BY = 'random_shuffle'
#SORT_BY = 'original_order'
#SORT_BY = DF_ANOVA_F_STAT_STRING
# SORT_BY = DF_MI_STRING
# SORT_BY = 'REGRESSION'
# SORT_BY = 'ALL_TOP_K_MERGED'
#SORT_BY = 'ALL_TOP_K_SERIAL'
#SORT_BY = 'NUM_LARGE_GROUPS'
SORT_BY = 'ALL_TOP_K_MERGED'
METRICS_SUBSET = [DF_MI_STRING, DF_ANOVA_F_STAT_STRING, DF_COSINE_SIMILARITY_STRING, DF_COVERAGE_STRING, DF_PVALUE_STRING,
        #'Count STD'
        ]
#METRICS_SUBSET = []
SAMPLE_SIZE = None  # for sample-guided search: run first on a sample of this size, and then use the results to guide the search on the full DB.
SAMPLE_STR = f'_{SAMPLE_SIZE}sample' if SAMPLE_SIZE is not None else ''
ITER_INDEX = 1

####################### ACS Seven states Config #################################
if RUN_ACS7:
    DATA_PATH = "data/Folkstable/SevenStates"
    DATAFRAME_PATH = "data/Folkstable/SevenStates/Seven_States_grouped.csv"
    STRING_COLS = ['NAICSP_grouped', 'OCCP_grouped', 'RT', 'NAICSP', 'SOCP']
    # DATABASE_NAME = "ACS7"
    DATABASE_NAME = "ACS7_numeric"
    TARGET_ATTR = "PINCP"
    GRP_ATTR = "SEX"
    COMPARE_LIST = [utils.less_than_cmp, 1, 2]  # 1 = Male, 2 = Female
    # GRP_ATTR = "SCHL"
    # COMPARE_LIST = [utils.less_than_cmp, 22, 21]  # 21 = Bachelor's, 22 = Master's
    # AGG_TYPE = 'median'
    AGG_TYPE = 'mean'
    MIN_GROUP_SIZE_SQL = 30  # for filtering the returned predicates.
    GROUP_SIZE_FILTER_THRESHOLD = 30  # for filtering attr combinations in advance
    OUTPUT_DIR = os.path.join(DATA_PATH, "results")
    QUERY_DESC = "F_gt_M"
    # if SAMPLE_SIZE is not None:
    #     OUTPUT_PATH = os.path.join(
    #         OUTPUT_DIR,
    #         "sampling",
    #         f"{DATABASE_NAME}_{AGG_TYPE}_{MAX_ATOMS}atoms_F_gt_M_{SORT_BY.replace(' ', '_')}{SAMPLE_STR}_guided{ITER_INDEX}.csv")
    # else:
    #     OUTPUT_PATH = os.path.join(
    #         OUTPUT_DIR,
    #         f"{DATABASE_NAME}_{AGG_TYPE}_{MAX_ATOMS}atoms_F_gt_M_{SORT_BY.replace(' ', '_')}{SAMPLE_STR}_guided{ITER_INDEX}.csv")

####################### Chicago Config #################################
if RUN_CHICAGO:
    DATA_PATH = "data/chicago_crime"
    DATAFRAME_PATH = "data/chicago_crime/chicago_to_DB.csv"
    DATABASE_NAME = "ChicagoDB"
    GRP_ATTR = "District"
    TARGET_ATTR = "Number of Crimes"
    COMPARE_LIST = [utils.less_than_cmp, 8, 24]  # 8, 24 are districts
    AGG_TYPE = 'count'
    MIN_GROUP_SIZE_SQL = 30  # for filtering the returned predicates.
    GROUP_SIZE_FILTER_THRESHOLD = 30  # for filtering attr combinations in advance
    OUTPUT_DIR = os.path.join(DATA_PATH, "results")
    QUERY_DESC = "district8_lt_district24"

####################### Stack Overflow Config #################################
if RUN_SO:
    DATA_PATH = "data/SO"
    #DATAFRAME_PATH = "data/SO/survey_results_public.csv"
    DATAFRAME_PATH = "data/SO/temp_df_for_sql.csv"
    STRING_COLS = ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'EdLevel', 'LearnCode',
                   'LearnCodeOnline', 'LearnCodeCoursesCert', 'DevType', 'OrgSize', 'PurchaseInfluence', 'BuyNewTool',
                   'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith',
                   'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith',
                   'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith',
                   'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith',
                   'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSysProfessional use',
                   'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction', 'OfficeStackAsyncHaveWorkedWith',
                   'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith', 'OfficeStackSyncWantToWorkWith',
                   'Blockchain', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth',
                   'ICorPM', 'TimeSearching']
    DATABASE_NAME = "stack_overflow"
    TARGET_ATTR = "ConvertedCompYearly"
    GRP_ATTR = "EdLevel"
    #GRP_ATTR = "MainBranch"
    COMPARE_LIST = [utils.less_than_cmp, 'Master’s degree', 'Bachelor’s degree']
    #COMPARE_LIST = [utils.less_than_cmp, "I am a developer by profession", "None of these"]
    AGG_TYPE = 'median'
    #AGG_TYPE = 'mean'
    MIN_GROUP_SIZE_SQL = 5  # for filtering the returned predicates.
    GROUP_SIZE_FILTER_THRESHOLD = 0  # for filtering attr combinations in advance
    OUTPUT_DIR = os.path.join(DATA_PATH, "results")
    QUERY_DESC = "Bsc_gt_Msc"
    #QUERY_DESC = "test"

####################### Flights Config #################################
if RUN_FLIGHTS:
    DATA_PATH = "data/flights"
    DATAFRAME_PATH = "data/flights/flights_with_airports.csv"
    STRING_COLS = ['AIRLINE', 'TAIL_NUMBER', 'ORIGIN_AIRPORT_CODE', 'ORIGIN_AIRPORT', 'ORIGIN_CITY', 'ORIGIN_STATE',
                   'ORIGIN_COUNTRY', 'DEST_AIRPORT_CODE', 'DEST_AIRPORT', 'DEST_CITY', 'DEST_STATE', 'DEST_COUNTRY',
                   'CANCELLATION_REASON']
    DATABASE_NAME = "flights_large"
    #TARGET_ATTR = "ARRIVAL_DELAY"
    #GRP_ATTR = "AIRLINE"
    #COMPARE_LIST = [utils.less_than_cmp, 'UA', 'AA']
    TARGET_ATTR = 'DEPARTURE_DELAY'
    GRP_ATTR = 'DAY_OF_WEEK'
    COMPARE_LIST = [utils.less_than_cmp, 1, 6] # 1- monday, 6- saturday
    AGG_TYPE = 'count'
    WHERE = '"DEPARTURE_DELAY" > 10'
    MIN_GROUP_SIZE_SQL = 5  # for filtering the returned predicates.
    GROUP_SIZE_FILTER_THRESHOLD = 0  # for filtering attr combinations in advance
    OUTPUT_DIR = os.path.join(DATA_PATH, "results")
    # QUERY_DESC = "AA_gt_UA"
    QUERY_DESC = f"{GRP_ATTR}_{COMPARE_LIST[2]}_gt_{COMPARE_LIST[1]}"

####################### COMPAS Config #################################
if RUN_COMPAS:
    DATA_PATH = "data/compas"
    DATAFRAME_PATH = "data/compas/compas-scores-two-years.csv"
    STRING_COLS = [] # TODO: update before using regression
    DATABASE_NAME = "compas"
    TARGET_ATTR = "two_year_recid"
    GRP_ATTR = "race"
    COMPARE_LIST = [utils.less_than_cmp, 'Caucasian', 'African-American']#, 'Caucasian']
    AGG_TYPE = 'mean'
    MIN_GROUP_SIZE_SQL = 5  # for filtering the returned predicates.
    GROUP_SIZE_FILTER_THRESHOLD = 0  # for filtering attr combinations in advance
    OUTPUT_DIR = os.path.join(DATA_PATH, "results")
    QUERY_DESC = "black_gt_white"


############################# output path ###############################
OUTPUT_PATH = os.path.join(
    OUTPUT_DIR, "m_experiment",
    f"{DATABASE_NAME}_{AGG_TYPE}_{MAX_ATOMS}atoms_{QUERY_DESC}_{SORT_BY.replace(' ', '_')}{SAMPLE_STR}_guided{ITER_INDEX}.csv")
