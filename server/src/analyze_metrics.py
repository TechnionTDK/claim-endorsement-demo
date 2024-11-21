import pandas as pd


def read_metrics_from_path(df_path):
    results = pd.read_csv(df_path)
    results['anova'] = results[['anova_f_stat', 'anova_p_value']].apply(lambda row: tuple(row.values), axis=1)
    # from a string representing a tuple to an actual tuple
    results['attr_tuple'] = results['attr_tuple'].apply(eval)
    results = results.set_index('attr_tuple')
    anova_dict = results['anova'].to_dict()
    mi_dict = results['mi'].to_dict()
    cosine_sim_dict = results['cosine_sim'].to_dict()
    min_value_count = results['min_value_count'].to_dict()
    max_group_size = results['max_group_size'].to_dict()
    return anova_dict, mi_dict, cosine_sim_dict, min_value_count, max_group_size


def make_anova_dataset():
    df = pd.read_csv(r"data\Folkstable\SevenStates\metrics_2atoms_PINCP.csv", index_col=0)
    anova_dict, mi_dict, cosine_sim_dict, min_value_count, max_group_size = read_metrics_from_path(r"data\Folkstable\SevenStates\metrics_2atoms_PINCP.csv")

    # make anova dataset: attr1, att2, (attr1 and attr2)
    anova_data = []
    for attr_tuple in anova_dict:
        if len(attr_tuple) == 1:
            continue
        # 2 attributes in the tuple
        attr1, attr2 = attr_tuple
        anova_data.append([attr1, anova_dict[(attr1,)][0], attr2, anova_dict[(attr2,)][0], anova_dict[attr_tuple]][0])
    anova_df = pd.DataFrame.from_records(anova_data, columns=['Attr1', 'Attr1_anova', 'Attr2', 'Attr2_anova', 'combined_anova'])
    anova_df.to_csv("data/Folkstable/SevenStates/anova_analysis.csv")


def test_monotonicity(anova_df):
    claim_holds = 0
    claim_doesnt_hold = 0
    for i, row1 in anova_df.iterrows():
        print(f"so far: holds: {claim_holds}, doesn't hold: {claim_doesnt_hold}")
        for j, row2 in anova_df.iterrows():
            if row1['Attr1_anova'] > row2['Attr1_anova'] and row1['Attr2_anova'] > row2 ['Attr2_anova']:
                if row1['combined_anova'] > row2['combined_anova']:
                    claim_holds += 1
                else:
                    claim_doesnt_hold += 1
    print(f"Claim holds: {claim_holds}, claim does not hold: {claim_doesnt_hold}")


def make_MI_dataset():
    # df = pd.read_csv(r"data\Folkstable\SevenStates\metrics_2atoms_PINCP.csv", index_col=0)
    anova_dict, mi_dict, cosine_sim_dict, min_value_count, max_group_size = read_metrics_from_path(r"data\Folkstable\SevenStates\metrics_2atoms_PINCP.csv")

    # make MI dataset: attr1, att2, (attr1 and attr2)
    MI_data = []
    for attr_tuple in mi_dict:
        if len(attr_tuple) == 1:
            continue
        # 2 attributes in the tuple
        attr1, attr2 = attr_tuple
        MI_data.append([attr1, mi_dict[(attr1,)], attr2, mi_dict[(attr2,)], mi_dict[attr_tuple]])
    mi_df = pd.DataFrame.from_records(MI_data, columns=['Attr1', 'Attr1_MI', 'Attr2', 'Attr2_MI', 'combined_MI'])
    mi_df.to_csv("data/Folkstable/SevenStates/mi_analysis.csv")


def test_monotonicity(mi_df):
    claim_holds = 0
    claim_doesnt_hold = 0
    for i, row1 in mi_df.iterrows():
        print(f"so far: holds: {claim_holds}, doesn't hold: {claim_doesnt_hold}")
        for j, row2 in mi_df.iterrows():
            if row1['Attr1_MI'] > row2['Attr1_MI'] and row1['Attr2_MI'] > row2 ['Attr2_MI']:
                if row1['combined_MI'] > row2['combined_MI']:
                    claim_holds += 1
                else:
                    print("############# Does not hold: ##########")
                    print(row1)
                    print(row2)
                    claim_doesnt_hold += 1
    print(f"Claim holds: {claim_holds}, claim does not hold: {claim_doesnt_hold}")