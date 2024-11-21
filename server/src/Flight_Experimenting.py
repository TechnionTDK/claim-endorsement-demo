import config
import pandas as pd
from ClaimEndorseFunctions import *
import time

trans_dict = {"id": "ID",
                    "year": "Year",
                    "month": "Month",
                    "day": "Day",
                    "dep_time": "Departure Time",
                    "sched_dep_time": "Sceduled Departure Time",
                    "dep_delay": "Departure Delay",
                    "arr_time": "Arrival Time",
                    "sched_arr_time": "Scheduled Arrival Time",
                    "arr_delay": "Arrival Delay",
                    "carrier": "Carrier",
                    "flight": "Flight",
                    "tailnum": "Tail Number",
                    "origin": "Origin",
                    "dest": "Destination",
                    "air_time": "Air Time",
                    "distance": "Distance",
                    "hour": "Hour",
                    "minute": "Minute",
                    "time_hour": "Time hour",
                    "name": "Name"}

exclude_list = ["id", "time_hour", "name",
                # "dep_time", "sched_dep_time", "arr_time", "sched_arr_time", "hour", "minute"
                "dep_delay" # this is the target attribute.
                ]

is_numeric = ["dep_delay", "arr_delay", "air_time", "distance"]

if __name__ == '__main__':
    start_time = time.time()
    df = pd.read_csv(config.DATAFRAME_PATH)
    
    #shuffle_and_save(df, exclude_list, is_numeric, trans_dict, start_time, iters=3)
    #run_random_shuffle_over_full_table(df, exclude_list, is_numeric, trans_dict, 3)

    ##################### main quality ################################
    #result_df = run_cherrypicking_with_config(df, exclude_list, is_numeric, trans_dict)

    ########### sample size experiment #####################
    #run_sample_guided_experiment([0.01, 0.05, 0.1], 3, df, exclude_list, is_numeric, trans_dict)

    ############## num tuples experiment #########################
    methods = ['random_shuffle:1', 'random_shuffle:2', 'random_shuffle:3', 'original_order', 'ALL_TOP_K_MERGED', '0.01sample', 'ALL_TOP_K_SERIAL']
    #sample_sizes = range(50000, 300001, 50000)
    #num_tuples_vs_time_for_full_run(sample_sizes, df, exclude_list, is_numeric, trans_dict, methods)
    
    ############## num columns experiment #########################
    col_sample_sizes = range(2, 19 ,2)
    num_columns_vs_time_for_full_run(col_sample_sizes, df, exclude_list, is_numeric, trans_dict, methods)


