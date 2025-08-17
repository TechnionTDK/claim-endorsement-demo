import pandas as pd
from claim_endorse_demo import db_name_to_config
from ClaimEndorseFunctions import df_to_sql_DB
if __name__ == "__main__":
    for dataset_name in db_name_to_config:
        db_name = db_name_to_config[dataset_name]["database_name"]
        if db_name not in ['SO_disc']:
            continue
        df_path = db_name_to_config[dataset_name]["dataframe_path"]
        df = pd.read_csv(df_path, index_col=0)
        print(f"Uploading {db_name} to postgres DB")
        df_to_sql_DB(df, db_name)