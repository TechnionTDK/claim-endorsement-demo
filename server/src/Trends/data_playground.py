import pandas as pd


def is_rising(list_of_numbers):
    for i in range(len(list_of_numbers)-1):
        if list_of_numbers[i] > list_of_numbers[i+1]:
            return False
    return True

#### stack overflow ####

agg = 'mean'
df = pd.read_csv("data/SO/temp_df_for_sql.csv", index_col=0)
edlevel_to_number = {'Primary/elementary school': 1, 'Secondary school': 2, 'Bachelor’s degree': 3,
                     'Master’s degree': 4, 'Other doctoral degree (Ph.D., Ed.D., etc.)': 5}
df['edlevelnumeric'] = df['EdLevel'].apply(edlevel_to_number.get)
df.groupby('edlevelnumeric')['ConvertedCompYearly'].apply(agg)

