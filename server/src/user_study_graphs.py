import matplotlib.pyplot as plt
import pandas as pd


def choose_randomly_from_middle(path_or_df, metric, blacklist=None, template=None, single_attr=False):
    if type(path_or_df) == str:
        df = pd.read_csv(path_or_df, index_col=0)
    else:
        df = path_or_df
    if blacklist is not None:
        df = df[~df['Attr1'].isin(blacklist) & ~df['Attr2'].isin(blacklist)]
    m = df[metric].median()
    print(f"{metric}: max: {df[metric].max()} min {df[metric].min()} median:{m}")
    rows = df[df[metric] <= m] #[['Attr1', 'Value1', 'Attr2', 'Value2', 'mean1', 'N1', 'mean2', 'N2', metric]]
    r = rows.sort_values(metric, ascending=False, axis=0).iloc[0]
    if template is None:
        print(r)
    else:
        if single_attr:
            print(template.format(count=r['N1']+r['N2'], count1=r['N1'], count2=r['N2'], attr1=r['Attr1'], value1=r['Value1']))
        else:
            print(template.format(count=r['N1']+r['N2'], attr1=r['Attr1_str'], value1=r['Value1_str'], attr2=r['Attr2_str'],
                                  value2=r['Value2_str'], mean1=int(r['mean1']), mean2=int(r['mean2'])))
        print(f"N1: {r['N1']}, N2: {r['N2']}")


def choose_randomly_from_each_metric():
    path = "data/Folkstable/SevenStates/results/compare to hypdb/ACS7_numeric_mean_2atoms_F_gt_M_ALL_TOP_K_SERIAL_guided1_with_external_scores.csv"
    # path = "data/SO/results/case studies/stack_overflow_mean_2atoms_Msc_gt_Bsc_ALL_TOP_K_MERGED_guided1_with_external_scores.csv"
    # path = "data/flights/results/flights_large_count_2atoms_DAY_OF_WEEK_6_gt_1_HYPDB_guided1_external_scores.csv"
    df = pd.read_csv(path, index_col=0)
    if path.startswith("data/flights"):
        print(f"read {len(df)}")
        df = df[df['Attr2'].isna()]
        print(f"read {len(df)}")
        df['Inverted pvalue'] = df['N2']-df['N1']
    for metric in ['Normalized Anova F Stat', 'Normalized_MI', 'Cosine Similarity', 'Coverage', 'Inverted pvalue']:
        choose_randomly_from_middle(
            df, metric,
            blacklist=['RELP', 'SPORDER'],
            # single_attr=True,
            # template="Among the {count} flights where {attr1}={value1}, there are more delays on Saturdays ({count2}) vs. Mondays ({count1}).",
            template="Among the {count} people who {attr1}={value1} & {attr2}={value2}, women have a higher income on average (${mean2}) than men (${mean1})."
            # template = "Among the {count} people who {attr1}={value1} & {attr2}={value2}, MSc graduates earn a higher salary on average (${mean2}) than BSc graduates (${mean1})."
        )



# # Data
# categories = ['BSc', 'MSc']
# g1, g2 = categories
# data = {
#     "statement id": [1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 27, 28, 29, 30, 31, 32],
#     "BSc value": [13450, 42302, 165692, 165692, 120599, 100013, 30474, 224574, 21946, 51651, 165769, 165769, 39194, 113545, 197018, 48749, 62759, 43585, 75211, 103820],
#     "MSc value": [54750, 82871, 167230, 167230, 133620, 145399, 45933, 255958.90, 45987, 52511.31, 182384, 182384, 56190, 134642, 312710, 98014, 231458, 213557, 160885, 180683],
#     "BSc count": [6, 226, 6497, 6497, 3126, 349, 12, 1005, 12, 1591, 900, 900, 106, 831, 148, 7, 23, 20, 46, 218],
#     "MSc count": [10, 54, 4201, 4201, 1399, 338, 28, 667, 28, 458, 542, 542, 68, 1041, 86, 15, 9, 7, 14, 90]
# }
# xlabel = "Average salary"
# unit = "people"
# database = "SO"

# categories = ["Men", "Women"]
# g1, g2 = categories
# data = {
#     "statement id": [13, 13, 14, 14, 15, 15, 16, 16, 17, 18, 19, 20, 17, 21, 33,34,35,36,37],
#     "Men value": [16720, 16720, 7201, 7201, 1017, 1017, 3436, 3436, 1656, 36789, 46610, 43222, 1656, 5649, 98318, 28784, 58543, 15191, 43437],
#     "Women value": [21507, 21507, 7325, 7325, 1044, 1044, 3474, 3474, 2768, 39288, 57222, 50323, 2768, 6155, 105045, 29476, 60086, 22105, 51467],
#     "Men count": ['24.8K', '24.8K', '71K', '71K', '14.5K', '14.5K', '3698', '3698', '545', '1360', '538', '672', '545', '49.8K', '73', '9608', '125', '91', '32'],
#     "Women count": ['24.2K', '24.2K', '58K', '58K', '13.9K', '13.9K', '3897', '3897', '385', '239', '44', '58', '385', '41.4K', '45', '284', '458', '83', '54']
# }
# xlabel = "Average income"
# unit = "people"
# database = "ACS"


categories = ["Monday", "Saturday"]
g1, g2 = categories
data = {
    "statement id": [22, 23, 24, 25, 26, 38, 39, 40, 41, 42],
    "Monday value": [30, 986, 8744, 41, 2573, 48, 10, 14, 14, 9],
    "Saturday value": [43, 1028, 9549, 51, 3753, 49, 13, 17, 16, 14],
}
for d in [g1, g2]:
    data[f'{d} count'] = data[f'{d} value']
xlabel = "# Delays over 10 minutes"
unit = "flights"
database = "flights"

# Create DataFrame
df = pd.DataFrame(data)

textsize = 14
for i, r in df.iterrows():
    # Create the bar chart
    fig, ax = plt.subplots()
    bars = ax.barh([0, 0.4], [r[f'{g1} value'], r[f'{g2} value']], height=0.15, tick_label=categories, zorder=3)

    # Add text labels to each bar
    counts = [f"{int(num)} {unit}" for num in [r[f'{g1} count'], r[f'{g2} count']]]
    for j, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width/2, bar.get_y() + bar.get_height() / 2, f'{counts[j]}', va='center', ha='center', color='white', fontweight='bold', fontsize=textsize)

    # Customize the chart
    ax.set_xlabel(xlabel, fontsize=textsize)
    ax.tick_params(axis='y', which='major', labelsize=textsize)
    ax.tick_params(axis='x', which='major', labelsize=textsize-2)
    ax.grid(axis='x', which='major', zorder=0)
    plt.tight_layout()
    plt.savefig(f'data/user study/{database}/{int(r["statement id"])}.png')
    plt.close(fig)
