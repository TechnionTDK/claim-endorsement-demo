from ClaimEndorseFunctions import *
from analyze_output import calculate_metrics_by_time_top_k_single_score, calculate_metrics_by_time_top_k_all_scores


def make_trans_dict_for_chicago():
    return {"IUCR": "Crime Reporting Code",
            "Primary Type": "Primary Crime Type"}



if __name__ == '__main__':
    # TODO: add an index column, and read the file with index_col=0
    df = pd.read_csv('data/chicago_crime/Chicago_Crimes_-_2001_to_Present.csv')
    is_numeric = []
    is_bucket = []
    exclude_list = ['ID', 'Case Number'] + \
                   [
                    'Block',
                    # 'Beat', 'District', 'Ward', 'Community Area',
                    'X Coordinate', 'Y Coordinate', 'Latitude', 'Longitude',
                    'Location', 'Historical Wards 2003-2015', 'Zip Codes', 'Community Areas', 'Wards',
                    'Boundaries - ZIP Codes', 'Census Tracts', 'Police Districts', 'Police Beats', 'Wards 2023-'
                   ]
    date_fields_dict = {'Date': '%m/%d/%Y %H:%M:%S %p', 'Updated On': '%m/%d/%Y %H:%M:%S %p'}

    # To load the table into the postgresql database:
    # created_df = create_filtered_csv(df, is_numeric, is_bucket, exclude_list, date_fields_dict, "data/chicago_crime/chicago_to_DB.csv",
    #                                    "data/chicago_crime/chicago_discretized_attributes.txt", create_db_flag=True)

    exclude_list += ['Date', 'Updated On']

    df[TARGET_ATTR] = 1
    attr_list = list(set(df.columns).difference(set(exclude_list + [TARGET_ATTR])))
    print(f"{len(attr_list)} attributes: {attr_list}")
    trans_dict = make_trans_dict_for_chicago()
    if RUN_ACTUAL_CP:
        res = run_cherrypicking_with_config(df, exclude_list, is_numeric=[], trans_dict=trans_dict)
    # if CREATE_FIGURES:
    #     result_path_list = [os.path.join(OUTPUT_DIR, "RESULT1.csv"),
    #                         os.path.join(OUTPUT_DIR, "RESULT2.csv"),
    #                         ]
    #     labels = ["Label1", "Label2"]
    #     calculate_metrics_by_time_top_k_single_score(result_path_list, labels, result_path_list[1],
    #                                                  DF_COSINE_SIMILARITY_STRING,
    #                                                  sorting_ascending=False, k=100,
    #                                                  time_bin_size_in_seconds=10, max_time_limit_in_seconds=15 * 60,
    #                                                  output_prefix="Chicago_count_district8_lt_24_sorted_cosine_sim")
    #     res_path = os.path.join(OUTPUT_DIR, "ACS_7states_mean_female_greater_than_male_sorted_by_approx_cosine_sim.csv")
    #     calculate_metrics_by_time_top_k_all_scores(res_path, res_path,
    #                                                k=100, time_bin_size_in_seconds=15, max_time_limit_in_seconds=300,
    #                                                output_prefix="ACS7_female_mean_gt_men_sorted_approx_cosine_sim_metrics")

