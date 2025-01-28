import pandas as pd
import json
from utils import *
from QueryRunner import connect_sql_db


def ACS_dicts():
    df = pd.read_csv("data/Folkstable/SevenStates/Seven_States_grouped_disc.csv", index_col=0)
    trans_dict = make_translation_for_ACS(df.columns)
    col_to_str = pd.read_csv('data/Folkstable/field_map.tsv', sep='\t')
    col_to_str['field label'] = col_to_str['field label'].apply(lambda s: s.strip('* '))
    exclude_list1 = ["SERIALNO", "PWGTP"] + [f"PWGTP{x}" for x in range(1, 81)]
    exclude_for_PINCP = ["PINCP", "INTP", "OIP", "PAP", "RETP", "SEMP", "SSIP", "SSP", "WAGP", "PERNP", "POVPIP", "ADJINC",
                         "FPINCP", "FINTP", "FOIP", "FPAP", "FRETP", "FSEMP", "FSSIP", "FSSP", "FWAGP", "FPERNP"]
    exclude2 = ["AGEP", "WKHP", "MARHYP", "CITWP"]
    allocation_flags = [col for col in df.columns if "allocation flag" in trans_dict[col]]
    exclude_list = exclude_list1 + exclude_for_PINCP + exclude2 + allocation_flags
    numeric = ['JWMNP', 'YOEP', 'JWAP', 'JWDP']
    col_to_str_inc = col_to_str[~col_to_str['field name'].isin(exclude_list + numeric)]
    col_to_desc = col_to_str_inc.set_index('field name')['field label'].to_dict()

    f = open("data/Folkstable/col_to_desc_dict.json", "w")
    f.write("{")
    for i, col in enumerate(sorted(col_to_desc.keys())):
        f.write(f'"{col}":"{col_to_desc[col]}"')
        if i < len(col_to_desc) - 1:
            f.write(", ")
    f.write("}")
    f.close()
    # f = open("data/Folkstable/col_to_desc_dict1.txt", "w")
    # f.write(str(col_to_desc))
    # f.close()

    col_to_values = {}
    for k in col_to_desc:
        col_to_values[k] = sorted([v for v in df[k].unique() if not pd.isna(v)])
    # convert numpy ints to basic ints for json serialization
    for k in col_to_values:
        vs = col_to_values[k]
        if type(vs[0]) == np.int64:
            col_to_values[k] = [int(v) for v in vs]
    with open("data/Folkstable/col_to_values.json", "w") as outfile:
        json.dump(col_to_values, outfile)

    col_desc_to_values = {}
    for k in col_to_values:
        col_desc_to_values[col_to_desc[k]] = col_to_values[k]
    with open("data/Folkstable/col_desc_to_values.json", "w") as outfile:
        json.dump(col_to_values, outfile)

    col_desc_and_value_to_value_desc = {}
    for k in col_to_values:
        for v in col_to_values[k]:
            col_desc_and_value_to_value_desc[(col_to_desc[k], v)] = safe_translate((k, v), trans_dict)
    f = open("data/Folkstable/col_desc_and_value_to_value_desc.json", "w")
    for k in col_to_values:
        f.write('"'+col_to_desc[k]+'":{\n')
        for v in col_to_values[k]:
            f.write(f'"{v}":"{safe_translate((k, v), trans_dict)}",\n')
        f.write("}\n")
    f.close()


def age_bucketize(x):
    if x < 18:
        return "<18"
    if x < 25:
        return "18-24"
    if x < 35:
        return "25-34"
    if x < 45:
        return "35-44"
    if x < 55:
        return "45-54"
    if x < 65:
        return "56-64"
    if x >= 65:
        return ">65"


def marhyp_bucketize(x):
    years_since = 2018-x
    if years_since < 1:
        return "<1"
    if years_since < 6:
        return "1-5"
    if years_since < 10:
        return "6-10"
    if years_since >= 10:
        return ">10"


def wkhp_bucketize(x):
    if x < 10:
        return "<10"
    if x < 41:
        return "10-40"
    if x >= 41:
        return ">40"


def ACS_bucketize_csv():
    fields = {'AGEP': (age_bucketize, "age_disc"),
              'MARHYP': (marhyp_bucketize, "years_since_married_disc"),
              'WKHP': (wkhp_bucketize, "wkhp_disc")}
    df = pd.read_csv("data/Folkstable/SevenStates/Seven_States_grouped.csv", index_col=0)
    for f in fields:
        func, new_name = fields[f]
        df[new_name] = df[f].apply(func)
    print(df[['AGEP', 'age_disc']].head())
    print(df[['WKHP', 'wkhp_disc']].head())
    print(df[['MARHYP', 'years_since_married_disc']].head())
    df = df.drop(['AGEP', 'MARHYP', 'WKHP', 'CITWP'], axis=1)
    df.to_csv("data/Folkstable/SevenStates/Seven_States_grouped_disc.csv")


def flight_day_bucketize(x):
    if x <= 10:
        return "1-10"
    if x <= 20:
        return "11-20"
    if x > 20:
        return "21-31"


def flight_distance_bucketize(x):
    if x <= 500:
        return "<500"
    if x<=1000:
        return "500-1000"
    if x <= 1500:
        return "1000-1500"
    if x <= 2000:
        return "1500-2000"
    if x > 2000:
        return ">2000"


def flight_time_to_hour(x):
    if x < 100:
        return "00"
    if x >= 100:
        return str(int(x))[:-2]


def flights_bucketize_csv():
    fields = {'DAY': (flight_day_bucketize, "day_of_month"),
              'DISTANCE': (flight_distance_bucketize, "distance_disc"),
              'SCHEDULED_DEPARTURE': (flight_time_to_hour, "scheduled_departure_hour"),
              'DEPARTURE_TIME': (flight_time_to_hour, "departure_hour"),
              }
    df = pd.read_csv("data/flights/flights_with_airports.csv", index_col=0)
    for f in fields:
        func, new_name = fields[f]
        df[new_name] = df[f].apply(func)
        print(df[[f, new_name]].head())
    include = ['MONTH', 'day_of_month', 'DAY_OF_WEEK', 'AIRLINE', 'ORIGIN_AIRPORT_CODE', 'DEST_AIRPORT_CODE',
               'scheduled_departure_hour', 'departure_hour', 'distance_disc', 'DIVERTED', 'ORIGIN_AIRPORT',
               'ORIGIN_CITY', 'ORIGIN_STATE', 'ORIGIN_COUNTRY', 'DEST_AIRPORT', 'DEST_CITY', 'DEST_STATE',
               'DEST_COUNTRY']
    df.to_csv("data/flights/flights_with_airports_disc.csv")

def clean_unicode(x):
    if type(x) != str:
        return x
    return x.replace('\xa0', ' ')

def flights_dicts():
    df = pd.read_csv("data/flights/flights_with_airports_disc.csv", index_col=0,
                     dtype={'ORIGIN_AIRPORT_CODE': str, 'DEST_AIRPORT_CODE': str, 'ORIGIN_AIRPORT': str,
                            'ORIGIN_CITY': str, 'ORIGIN_STATE': str, 'ORIGIN_COUNTRY': str, 'DEST_AIRPORT': str,
                            'DEST_CITY': str, 'DEST_STATE': str, 'DEST_COUNTRY': str})
    include = ['MONTH', 'day_of_month', 'DAY_OF_WEEK', 'AIRLINE', 'ORIGIN_AIRPORT_CODE', 'DEST_AIRPORT_CODE',
               'scheduled_departure_hour', 'departure_hour', 'distance_disc', 'DIVERTED', 'ORIGIN_AIRPORT',
               'ORIGIN_CITY', 'ORIGIN_STATE', 'DEST_AIRPORT', 'DEST_CITY', 'DEST_STATE']
    trans_dict = make_translation_for_flights(include)
    cols_order_by_desc = sorted(include, key=trans_dict.get)

    f = open("data/flights/col_to_desc_dict.json", "w")
    f.write("{")
    for i, col in enumerate(cols_order_by_desc):
        f.write(f'"{col}":"{trans_dict[col]}"')
        if i < len(cols_order_by_desc)-1:
            f.write(", ")
    f.write("}")
    f.close()

    col_to_values = {}
    for k in include:
        col_to_values[k] = sorted([v for v in df[k].unique() if not pd.isna(v)])

    # convert numpy ints to basic ints for json serialization
    for k in col_to_values:
        vs = col_to_values[k]
        if type(vs[0]) == np.int64:
            col_to_values[k] = [int(v) for v in vs]

    with open("data/flights/col_to_values.json", "w") as outfile:
        json.dump(col_to_values, outfile)

    col_desc_to_values = {}
    for k in col_to_values:
        col_desc_to_values[trans_dict[k]] = col_to_values[k]

    with open("data/flights/col_desc_to_values.json", "w") as outfile:
        json.dump(col_desc_to_values, outfile)

    col_desc_and_value_to_value_desc = {}
    for k in col_to_values:
        for v in col_to_values[k]:
            col_desc_and_value_to_value_desc[(trans_dict[k], v)] = safe_translate((k, v), trans_dict)
    f = open("data/flights/col_desc_and_value_to_value_desc.json", "w")
    for k in col_to_values:
        f.write('"'+trans_dict[k]+'"{\n')
        for v in col_to_values[k]:
            f.write(f'"{v}":"{safe_translate((k, v), trans_dict)}"\n')
        f.write("}\n")
    f.close()


def h_and_m_dicts():
    df = pd.read_csv("data/hm/merged.csv", index_col=0)
    include = ['product_type_name', 'product_group_name', 'graphical_appearance_name', 'colour_group_name',
               'perceived_colour_value_name', 'perceived_colour_master_name', 'department_no', 'department_name',
               'index_name', 'index_group_name', 'section_name', 'garment_group_name', 'sales_channel_id', 'FN',
               'Active', 'club_member_status', 'fashion_news_frequency', 'day_of_month']
    trans_dict = make_translation_for_hm(include)
    cols_order_by_desc = sorted(include, key=trans_dict.get)

    f = open("data/hm/col_to_desc_dict.json", "w")
    f.write("{")
    for i, col in enumerate(cols_order_by_desc):
        f.write(f'"{col}":"{trans_dict[col]}"')
        if i < len(cols_order_by_desc)-1:
            f.write(", ")
    f.write("}")
    f.close()

    col_to_values = {}
    for k in include:
        col_to_values[k] = sorted([v for v in df[k].unique() if not pd.isna(v)])

    # convert numpy ints to basic ints for json serialization
    for k in col_to_values:
        vs = col_to_values[k]
        if type(vs[0]) == np.int64:
            col_to_values[k] = [int(v) for v in vs]

    with open("data/hm/col_to_values.json", "w") as outfile:
        json.dump(col_to_values, outfile)

    col_desc_to_values = {}
    for k in col_to_values:
        col_desc_to_values[trans_dict[k]] = col_to_values[k]

    with open("data/hm/col_desc_to_values.json", "w") as outfile:
        json.dump(col_desc_to_values, outfile)

    col_desc_and_value_to_value_desc = {}
    for k in col_to_values:
        for v in col_to_values[k]:
            col_desc_and_value_to_value_desc[(trans_dict[k], v)] = safe_translate((k, v), trans_dict)
    f = open("data/hm/col_desc_and_value_to_value_desc.json", "w")
    for k in col_to_values:
        f.write('"'+trans_dict[k]+'"{\n')
        for v in col_to_values[k]:
            f.write(f'"{v}":"{safe_translate((k, v), trans_dict)}"\n')
        f.write("}\n")
    f.close()


def SO_years_bucketize(x):
    if x <= 1:
        return "<1"
    if x <= 5:
        return "1-5"
    if x <= 10:
        return "5-10"
    if x <= 20:
        return "10-20"
    if x > 20:
        return ">20"


def SO_bucketize_csv():
    fields = {'YearsCode': (SO_years_bucketize, "YearsCode_disc"),
              'YearsCodePro': (SO_years_bucketize, "YearsCode_Pro_disc"),
              'WorkExp': (SO_years_bucketize, "WorkExp_disc")
              }
    df = pd.read_csv("data/SO/temp_df_for_sql.csv")
    for f in fields:
        func, new_name = fields[f]
        df[new_name] = df[f].apply(func)
        print(df[[f, new_name]].head())
    df.to_csv("data/SO/SO_disc.csv")


def SO_dicts():
    df = pd.read_csv("data/SO/SO_disc.csv", index_col=0)
    include = ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'EdLevel', 'LearnCode', 'LearnCodeOnline', 'LearnCodeCoursesCert', 'DevType', 'OrgSize', 'PurchaseInfluence', 'BuyNewTool', 'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith', 'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith', 'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith', 'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith', 'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSysProfessional use', 'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction', 'OfficeStackAsyncHaveWorkedWith', 'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith', 'OfficeStackSyncWantToWorkWith', 'Blockchain', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth', 'ICorPM', 'TimeSearching', 'YearsCode_disc', 'YearsCode_Pro_disc', 'WorkExp_disc']
    trans_dict = create_column_dictionary_for_SO(include)
    cols_order_by_desc = sorted(include, key=trans_dict.get)

    f = open("data/SO/col_to_desc_dict.json", "w")
    f.write("{")
    for i, col in enumerate(cols_order_by_desc):
        f.write(f'"{col}":"{trans_dict[col]}"')
        if i < len(cols_order_by_desc)-1:
            f.write(", ")
    f.write("}")
    f.close()

    col_to_values = {}
    for k in include:
        col_to_values[k] = sorted([v for v in df[k].unique() if not pd.isna(v)])

    # convert numpy ints to basic ints for json serialization
    for k in col_to_values:
        vs = col_to_values[k]
        if type(vs[0]) == np.int64:
            col_to_values[k] = [int(v) for v in vs]

    with open("data/SO/col_to_values.json", "w") as outfile:
        json.dump(col_to_values, outfile)

    col_desc_to_values = {}
    for k in col_to_values:
        col_desc_to_values[trans_dict[k]] = col_to_values[k]

    with open("data/SO/col_desc_to_values.json", "w") as outfile:
        json.dump(col_desc_to_values, outfile)

    col_desc_and_value_to_value_desc = {}
    for k in col_to_values:
        for v in col_to_values[k]:
            col_desc_and_value_to_value_desc[(trans_dict[k], v)] = safe_translate((k, v), trans_dict)
    f = open("data/SO/col_desc_and_value_to_value_desc.json", "w")
    for k in col_to_values:
        f.write('"'+trans_dict[k]+'":{\n')
        for v in col_to_values[k]:
            f.write(f'"{v}":"{safe_translate((k, v), trans_dict)}",\n')
        f.write("}\n")
    f.close()




def df_to_sql_DB(df, db_name):
    # This should only be run once. (Per DB)
    engine = connect_sql_db(db_name)
    df.to_sql("my_table", engine)


if __name__ == '__main__':
    # print("Creating discretized fields into CSV file")
    # ACS_bucketize_csv()
    # print("Reading new CSV")
    # df = pd.read_csv("data/Folkstable/SevenStates/Seven_States_grouped_disc.csv")
    # print("Uploading to database ACS7_disc. This may take a while.")
    # df_to_sql_DB(df, "ACS7_disc")

    # flights_bucketize_csv()
    # print("Reading new CSV")
    # df = pd.read_csv("data/flights/flights_with_airports_disc.csv", index_col=0)
    # print("Uploading to database flights_disc. This may take a while.")
    # df_to_sql_DB(df, "flights_disc")

    # SO_bucketize_csv()
    print("Reading new CSV")
    df = pd.read_csv("data/SO/SO_disc.csv", index_col=0)
    print("Uploading to database SO_disc. This may take a while.")
    df_to_sql_DB(df, "SO_disc")

