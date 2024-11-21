import pandas as pd

from ACS_Experimenting import bucketize_ACS_dataset
from ClaimEndorseFunctions import *

# first download the samples by: (from postgres)
# COPY (SELECT * FROM db_size_exp_<size>) TO '/var/lib/postgresql/ACS7_numeric_<size>sample1.csv' DELIMITER ',' CSV HEADER;

# Next, bucketize the samples
from analyze_output import analyze_oreo_output_file

for i in range(1, 11):
    p = f"/home/shunita/cherry/Cherry-picked-Generalizations/datasets/ACS7_numeric_{i}00Ksample1.csv"
    df = pd.read_csv(p, index_col=0)
    df = bucketize_ACS_dataset(df)
    df.to_csv(p)


# find the leading attributes in each sample result
# EXP_PATH = "/home/shunita/cherry/cherrypick/data/Folkstable/SevenStates/results/db_size_sensitivity4"
# ref_path = os.path.join(EXP_PATH, "ACS7_numeric_mean_2atoms_F_gt_M_original_order_guided_{i}00000_tuples.csv")
EXP_PATH = "/home/shunita/cherry/cherrypick/data/Folkstable/SevenStates/results/db_width_sensitivity1"
ref_path = os.path.join(EXP_PATH, "ACS7_numeric_mean_2atoms_F_gt_M_original_order_guided_{i}0cols_iter0.csv")
K=100
# d = {}
for i in range(7, 11):
    path = ref_path.format(i=i)
    res = pd.read_csv(path, index_col=0)
    res = res.sort_values(by='Metrics Average', ascending=False)
    top_attrs = set(list(res.head(K)['Attr1'].values) + list(res.head(K)['Attr2'].values))
    d[i] = top_attrs
print(d)

# Use these to run OREO on the matching sample.
# Finally, analyze the time until 95% recall in each metric.
# res_file_path = "/home/shunita/cherry/Cherry-picked-Generalizations/results/found_cas_ACS{i}00Ksample1_women_gt_men_attr_pairs.csv"
res_file_path = "/home/shunita/cherry/Cherry-picked-Generalizations/results/found_cas_ACS_{i}0col_sample1_women_gt_men_attr_pairs.csv"
for i in range(1, 7):
    df = analyze_oreo_output_file(res_file_path.format(i=i), ref_path.format(i=i), should_prune_by_generality=False)
    df.to_csv(os.path.join(EXP_PATH, f"ACS7_numeric_mean_2atoms_F_gt_M_OREO_guided_{i}00000_tuples.csv"))
