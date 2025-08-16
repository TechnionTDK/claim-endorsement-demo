import pandas as pd
from QueryRunner import *

def df_to_sql_DB(df, db_name):
    # This should only be run once. (Per DB)
    engine = connect_sql_db(db_name)
    df.to_sql("my_table", engine)

print("reading csv")
df = pd.read_csv('../data/diabetes2/diabetes_prediction_dataset_binned_age.csv', index_col=0)
df = df.drop(['diabetes10', 'age_category_numeric_consecutive', 'age_category_numeric'], axis=1)
print("loading to DB")
df_to_sql_DB(df, "diabetes")
