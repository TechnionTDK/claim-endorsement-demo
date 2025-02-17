import pandas as pd
from claim_endorse_demo import db_name_to_config
from ClaimEndorseFunctions import df_to_sql_DB
if __name__ == "__main__":
    for db_name in db_name_to_config:
        df_path = db_name_to_config[db_name]["dataframe_path"]
        df = pd.read_csv(df_path, index_col=0)
        print(f"Uploading {db_name} to postgres DB")
        df_to_sql_DB(df, db_name)