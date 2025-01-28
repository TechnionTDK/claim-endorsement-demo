import pandas as pd
from QueryRunner import *


def df_to_sql_DB(df, db_name):
    # This should only be run once. (Per DB)
    engine = connect_sql_db(db_name)
    df.to_sql("my_table", engine)

print("reading csv")
df = pd.read_csv('data/hm/merged.csv', index_col=0)
print("loading to DB")
df_to_sql_DB(df, "hm")
