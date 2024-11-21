import pandas as pd
from scipy.stats import ttest_rel
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

datasets = ['flights', 'SO', 'ACS']


def check_following_instructions(df):
    answer_names = [col for col in df.columns if col.startswith("s")]
    not_follow = []
    for dataset_name in datasets:
        subset = df[df['dataset'] == dataset_name]
        for a in answer_names:
            vs = subset[a].values
            if 1 not in vs or 5 not in vs:
                print(f"{a} did not follow the instructions - missing 1 or 5.")
                not_follow.append((a, dataset_name))
    return not_follow


def split_multi_value_methods(df):
    new_rows = []
    for i, r in df.iterrows():
        methods = [m.strip() for m in r['method'].split(",")]
        if len(methods) > 1:
            for m in methods:
                new_row = r.copy()
                new_row['method'] = m
                new_rows.append(new_row)
        else:
            new_rows.append(r)
    return pd.DataFrame(new_rows)


def count5(iterable):
    return len([x for x in iterable if x == 5])


def analyze_results(df):
    score_cols = [col for col in df.columns if col not in ['dataset', 'method']]
    df['sum_scores'] = df[score_cols].sum(axis=1)
    df['avg_scores'] = df[score_cols].mean(axis=1)
    df['count_5'] = df[score_cols].apply(count5, axis=1)


def stat_sig(df, method1, method2, dataset=None):
    """df should be after split_multi_value_methods"""
    score_cols = [col for col in df.columns if len(col) == 24]
    if dataset is not None:
        a = df[(df["method"] == method1) & (df["dataset"] == dataset)][score_cols].values
        b = df[(df["method"] == method2) & (df["dataset"] == dataset)][score_cols].values
    else:
        a = df[(df["method"] == method1)][score_cols].values.flatten()
        b = df[(df["method"] == method2)][score_cols].values.flatten()
        if len(a) != len(b):
            a = df[(df["method"] == method1) & (df["dataset"] != "flights")][score_cols].values.flatten()
            b = df[(df["method"] == method2) & (df["dataset"] != "flights")][score_cols].values.flatten()
    # if (a == b).all():
    #    return "same data"
    #return ttest_rel(a, b, axis=0, nan_policy='propagate', alternative='two-sided')
    diffs = a - b
    n = len(diffs)
    tstat = np.mean(diffs) / (np.std(diffs) / np.sqrt(n))
    #print(tstat)
    return 2*sp.stats.t.sf(np.abs(tstat), n-1)


def method_to_choice_type(method_str):
    if "gen" in method_str:
        return "gen"
    if "max" in method_str:
        return "max"
    if "median" in method_str:
        return "median"


def ratings_chart(which_value='Average rating'):
    # Create DataFrame from provided data
    data = {
        "type": ['avg nat', 'avg nat', 'coverage', 'coverage', 'coverage', 'stat sig', 'stat sig', 'stat sig', 'anova', 'anova', 'anova', 'emb sim', 'emb sim', 'emb sim', 'mi', 'mi', 'mi', 'hypdb', 'hypdb'],
        "Method": ['max avg nat + gf', 'max avg nat', 'max coverage + gf', 'max coverage', 'median coverage', 'max stat sig + gf', 'max stat sig', 'median stat sig', 'max anova + gf', 'max anova', 'median anova', 'max emb sim + gf', 'max emb sim', 'median emb sim', 'max mi + gf', 'max mi', 'median mi', 'max hypdb + gf', 'max hypdb'],
        "Average rating": [3.54, 3.07, 2.94, 3.35, 2.29, 3.38, 3.20, 2.51, 3.28, 3.15, 2.04, 3.14, 2.91, 2.44, 2.80, 2.91, 2.19, 2.54, 2.76],
        "Times ranked top": [27, 20, 15, 38, 8, 21, 35, 13, 18, 23, 7, 21, 21, 7, 9, 19, 9, 0, 12],
    }

    df = pd.DataFrame(data)

    # Create color and texture mapping for each type
    color_mapping = {
        "anova": ('#FF6961', "//"),
        "avg nat": ("#FFD1DC", "\\\\"),
        "coverage": ("#FADA5E", "xx"),
        "emb sim": ("#BDDA57", "||"),
        "hypdb": ("#87ceeb", "--"),
        "mi": ("#B57EDC", "++"),
        "stat sig": ("white", "**")
    }
    texture_mapping = {'max': "++", 'median': "--", "gen": "xx"}

    # Plotting
    fig, ax = plt.subplots(figsize=(12, 8))

    # Bar positions
    bar_positions = range(len(df))

    # Bar colors and textures
    bar_colors = [color_mapping[t][0] for t in df['type']]
    bar_textures = [texture_mapping[method_to_choice_type(m)] for m in df['Method']]

    # Plot bars with textures
    for i, (color, texture) in enumerate(zip(bar_colors, bar_textures)):
        ax.barh(bar_positions[i], df[which_value][i], color=color,  # hatch=texture,
                linewidth=1, edgecolor='black',
                label=df['type'][i] if i == df['type'].tolist().index(df['type'][i]) else "")

    # Adding labels and title
    #ax.set_ylabel('Method')
    ax.set_xlabel(which_value, fontsize=14)
    #ax.set_title('Average rating by Method and Type')
    ax.set_yticks(bar_positions)
    ax.set_yticklabels(df['Method'])

    # Remove duplicate legends
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys())
    if which_value == 'Average rating':
        plt.xlim(1, 3.8)
    plt.tight_layout()
    plt.savefig(f"data/user study/rating_{which_value}.pdf", format="pdf")
    plt.show()


def combined_ratings_chart():
    # Create DataFrame from provided data
    data = {
        "type": ['avg nat', 'avg nat', 'coverage', 'coverage', 'coverage', 'stat sig', 'stat sig', 'stat sig',
                 'anova', 'anova', 'anova', 'emb sim', 'emb sim', 'emb sim', 'mi', 'mi', 'mi', 'hypdb', 'hypdb'],
        "method": ['max avg nat (gf)', 'max avg nat', 'max coverage (gf)', 'max coverage', 'median coverage',
                   'max stat sig (gf)', 'max stat sig', 'median stat sig', 'max anova (gf)', 'max anova',
                   'median anova', 'max emb sim (gf)', 'max emb sim', 'median emb sim', 'max mi (gf)', 'max mi',
                   'median mi', 'max hypdb (gf)', 'max hypdb'],
        "Average rating": [3.54, 3.07, 2.94, 3.35, 2.29, 3.38, 3.20, 2.51, 3.28, 3.15, 2.04, 3.14, 2.91, 2.44, 2.80,
                           2.91, 2.19, 2.54, 2.76],
        "Times ranked top": [27, 20, 15, 38, 8, 21, 35, 13, 18, 23, 7, 21, 21, 7, 9, 19, 9, 0, 12],
    }

    data = pd.DataFrame(data)

    # Create color and texture mapping for each type
    color_mapping = {
        "anova": ('#FF6961', "//"),
        "avg nat": ("#FFD1DC", "\\\\"),
        "coverage": ("#FADA5E", "xx"),
        "emb sim": ("#BDDA57", "||"),
        "hypdb": ("#87ceeb", "--"),
        "mi": ("#B57EDC", "++"),
        "stat sig": ("#FFA343", "**")
    }

    fig, axes = plt.subplots(figsize=(10, 6), ncols=2, sharey=True)

    bar_colors = [color_mapping[t][0] for t in data['type']]

    bars0 = axes[0].barh(data['method'], data['Average rating'], align='center', color=bar_colors, zorder=10, linewidth=0.75, edgecolor='black')
    axes[0].set_title('Avg Rating (out of 5)', fontsize=15, #pad=15,
                      color='black')
    bars1 = axes[1].barh(data['method'], data['Times ranked top'], align='center', color=bar_colors, zorder=10, linewidth=0.75, edgecolor='black')
    axes[1].set_title('Times ranked top (out of 150)', fontsize=15, #pad=15,
                      color='black')

    #for i, bars in enumerate([bars0, bars1]):
    for j, bar in enumerate(bars0):
        width = bar.get_width()
        axes[0].text(0.95*width, bar.get_y() + bar.get_height() / 5,
                     f'{bar.get_width()}', #va='center',  # ha='center'
                     color='black', #fontweight='bold',
                     fontsize=10, zorder=11)

    for j, bar in enumerate(bars1):
        width = bar.get_width()
        place = width
        if place == 0:
            place += 1
        else:
            place -= 3
        axes[1].text(place, bar.get_y() + bar.get_height() / 5,
                     f'{bar.get_width()}',
                     color='black',
                     fontsize=10, zorder=11)


    #axes[0].invert_xaxis()

    axes[0].set(yticks=range(len(data)), yticklabels=data['method'])
    #axes[0].yaxis.tick_left()
    axes[0].tick_params(axis='both', colors='white')  # tick color
    axes[1].tick_params(axis='both', colors='white')
    axes[0].set_xlim([3.8, 1])

    for chart_index in range(2):
        for label in (axes[chart_index].get_xticklabels() + axes[chart_index].get_yticklabels()):
            label.set(fontsize=14, color='black')

        axes[chart_index].grid(which='major', color="#d6d0d0")
        axes[chart_index].spines['top'].set_visible(False)
        axes[chart_index].spines['right'].set_visible(False)
        axes[chart_index].spines['bottom'].set_visible(False)
        axes[chart_index].spines['left'].set_visible(False)
    fig.tight_layout()
    plt.savefig("data/user study/user_study_combined.pdf", format="pdf")
