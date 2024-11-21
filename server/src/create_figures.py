import os
import sys
import pickle
from config import *
from constants import *
from analyze_output import *

metric_to_legend_name = {DF_COSINE_SIMILARITY_STRING: 'EmbSim',
                         DF_INVERTED_PVALUE_STRING: 'Regression',
                         DF_NORMALIZED_ANOVA_F_STAT_STRING: 'ANOVA',
                         DF_NORMALIZED_MI_STRING: 'MI',
                         DF_COVERAGE_STRING: 'Coverage100',
                         DF_METRICS_AVERAGE: None}


def ACS_exp(metric_names, figure_desc):
    res_path_dict = {
        'Original Order': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_original_order_guided_reference.csv')],
        # for random order we also have runs 4 and 5 if we want to use them
        'Random Order': [os.path.join(OUTPUT_DIR, f'ACS7_numeric_mean_2atoms_F_gt_M_random_shuffle{i}_guided.csv') for i in range(1,4)], 
        '1%Sample': [os.path.join(OUTPUT_DIR, 'sampling', f'ACS7_numeric_mean_2atoms_F_gt_M_original_order_0.01sample_guided{i}.csv') for i in range(1,4)],
        '5%Sample': [os.path.join(OUTPUT_DIR, 'sampling', f'ACS7_numeric_mean_2atoms_F_gt_M_original_order_0.05sample_guided{i}.csv') for i in range(1,4)],
        '10%Sample': [os.path.join(OUTPUT_DIR, 'sampling', f'ACS7_numeric_mean_2atoms_F_gt_M_original_order_0.1sample_guided{i}.csv') for i in range(1,4)],
        #'5%Sample': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_original_order_10Ksample_guided.csv')],
                     # os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_original_order_10Ksample_guided2.csv')],
        # '50KSample': [os.path.join(OUTPUT_DIR,
        #                            'ACS7_numeric_mean_2atoms_F_gt_M_original_order_50Ksample_guided.csv')],
        # '100KSample': [os.path.join(OUTPUT_DIR,
        #                            'ACS7_numeric_mean_2atoms_F_gt_M_original_order_100Ksample_guided.csv')],
        'MI': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_MI_guided.csv')],
        'ANOVA': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_Anova_F_Stat_guided.csv')],
        'EmbSim': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_Cosine_Similarity_guided.csv')],
        'Regression': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_REGRESSION_guided.csv')],
        'Coverage100': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_NUM_LARGE_GROUPS_guided.csv')],
        'Serial Top k': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_ALL_TOP_K_SERIAL_guided1.csv')],
        'Merged Top k': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_ALL_TOP_K_MERGED_guided.csv')],
        'HypDB': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_HYPDB_guided1.csv')],
        'OREO★': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_OREO_guided.csv')]
    }
    #res_path_dict = {'HypDB': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_HYPDB_guided.csv')],}
    reference_file = os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_original_order_guided_reference.csv')
    if figure_desc == 'table_time_until_recall':
        for k, v in res_path_dict.items():
            print(f"{k}")
            for csv_path in v:
                metric_to_time = find_time_until_specific_score_recall(csv_path, reference_file, threshold=0.95)
                with open(os.path.join(OUTPUT_DIR, "time_to_recall.txt"), "a") as f:
                    f.write(f"{k}: {metric_to_time}")
        return
    stat_dict = None
    for metric_name in metric_names:
        # Sample size exp
        if figure_desc == 'sample_size':
            order = ['1%Sample', '5%Sample', '10%Sample']
            res_path_dict_sub = {k: v for k, v in res_path_dict.items() if k in order}
        # main graph
        elif figure_desc == 'main':
            order = ['Merged Top k', 'Serial Top k', '1%Sample',
                    #'Original Order', 
                    'Random Order', 'HypDB', 'OREO★']
            specific_nat_measure_baseline = metric_to_legend_name[metric_name]
            if specific_nat_measure_baseline is not None:
                order.append(specific_nat_measure_baseline)
            res_path_dict_sub = {k: v for k, v in res_path_dict.items() if k in order}
        else:
            print(f"Unsupported figure: {figure_desc}")
            return
        stat_dict = combine_result_files(res_path_dict_sub, metric_name, reference_file, order,
                                         k=100, time_bin_size_in_seconds=60,
                                         max_time_limit_in_seconds=1200,
                                         output_prefix=f"ACS7_numeric_mean_2atoms_F_gt_M_{figure_desc}_{metric_name}",
                                         filter_by_reference=False, time_unit='minutes', prev_stat_dict=stat_dict, base_font_size=24)


def test_for_noise_in_random_shuffle(metric_name):
    res_path_dict = {
        'Random Order1': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_random_shuffle_guided1.csv')],
        'Random Order2': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_random_shuffle_guided2.csv')],
        'Random Order3': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_random_shuffle_guided3.csv')],
        'Random Order4': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_random_shuffle_guided4.csv')],
        'Random Order5': [os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_random_shuffle_guided5.csv')],
    }
    reference_file = os.path.join(OUTPUT_DIR, 'ACS7_numeric_mean_2atoms_F_gt_M_original_order_guided_reference.csv')
    combine_result_files(res_path_dict, metric_name, reference_file, ['Random Order1','Random Order2','Random Order3', 'Random Order4'],
                         k=100, time_bin_size_in_seconds=60,
                         max_time_limit_in_seconds=1200, output_prefix=f"ACS7_numeric_mean_2atoms_F_gt_M_noise_test_{metric_name}",
                         filter_by_reference=False, time_unit='minutes')

def get_first_response_time(res_path_dict):
    for k in res_path_dict:
        times = []
        for filepath in res_path_dict[k]:
            df = pd.read_csv(filepath, index_col=0)
            times.append(df.Time.min())
        print(f"{k}: {np.mean(times)}")


def SO_exp(metric_names, figure_desc):
    #exp_string = 'F_gt_M'
    #agg = 'mean'
    exp_string = 'Bsc_gt_Msc'
    agg = 'median'
    res_path_dict = {
        'Original Order': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_original_order_guided_reference.csv')],
        'Random Order(3)': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_random_shuffle{i}_guided.csv') for i in range(1,4)],
        '1% Sample(3)': [os.path.join(OUTPUT_DIR, 'sampling', 
                                   f'stack_overflow_{agg}_2atoms_{exp_string}_original_order_0.01sample_guided{i}.csv') for i in range(1,4)],
        '5% Sample(3)': [os.path.join(OUTPUT_DIR, 'sampling',
                                   f'stack_overflow_{agg}_2atoms_{exp_string}_original_order_0.05sample_guided{i}.csv') for i in range(1,4)],
        '10% Sample(3)': [os.path.join(OUTPUT_DIR, 'sampling',
                                   f'stack_overflow_{agg}_2atoms_{exp_string}_original_order_0.1sample_guided{i}.csv') for i in range(1,4)],
        'MI': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_MI_guided.csv')],
        'ANOVA': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_Anova_F_Stat_guided.csv')],
        'EmbSim': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_Cosine_Similarity_guided.csv')],
        'Regression': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_REGRESSION_guided.csv')],
        'Coverage100': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_NUM_LARGE_GROUPS_guided.csv')],
        'Serial Top k': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_ALL_TOP_K_SERIAL_guided.csv')],
        'Merged Top k': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_ALL_TOP_K_MERGED_guided.csv')]
    }
    res_path_dict = {'HYPDB': [os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_HYPDB_guided.csv')]}
    reference_file = os.path.join(OUTPUT_DIR, f'stack_overflow_{agg}_2atoms_{exp_string}_original_order_guided_reference.csv')
    if figure_desc == 'table_time_until_recall':
        get_first_response_time(res_path_dict)
        for k, v in res_path_dict.items():
            print(f"{k}")
            for csv_path in v:
                metric_to_time = find_time_until_specific_score_recall(csv_path, reference_file, threshold=0.95)
                with open(os.path.join(OUTPUT_DIR, "time_to_recall.txt"), "a") as f:
                    f.write(f"{k}: {metric_to_time}")
        return
    stat_dict = None
    for metric_name in metric_names:
        # Sample size exp
        if figure_desc == 'sample_size':
            order = ['1% Sample(3)', '5% Sample(3)', '10% Sample(3)']
            res_path_dict_sub = {k: v for k, v in res_path_dict.items() if k in order}
        # Main methods
        elif figure_desc == 'main':
            # What if we only focused on this naturalness measure:
            #order = ['Merged Top k', 'Serial Top k', 'Original Order', '1KSample', 'Random Order']
            order = ['Merged Top k', 'Original Order', '1% Sample(3)', 'Random Order(3)']
            specific_nat_measure_baseline = metric_to_legend_name[metric_name]
            if specific_nat_measure_baseline is not None:
                order.append(specific_nat_measure_baseline)
            res_path_dict_sub = {k: v for k, v in res_path_dict.items() if k in order}
        else:
            print(f"Unsupported figure: {figure_desc}")
            return
        if figure_desc in ('main', 'sample_size'):
            stat_dict = combine_result_files(res_path_dict_sub, metric_name, reference_file, order,
                                             k=100, time_bin_size_in_seconds=20,
                                             max_time_limit_in_seconds=3 * 60,
                                             output_prefix=f"SO_{agg}_2atoms_{exp_string}_{figure_desc}_{metric_name}",
                                             filter_by_reference=False, time_unit='seconds', prev_stat_dict=stat_dict)


def flights_exp(metric_names, figure_desc):
    #exp_string = 'F_gt_M'
    #agg = 'mean'
    exp_string = 'DAY_OF_WEEK_6_gt_1'
    agg = 'count'
    db_str = 'flights_large'
    output_dir = 'data/flights/results/count_sat_gt_mon/'
    res_path_dict = {
        'Original Order': [os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_original_order_guided_reference.csv')],
        'Random Order(3)': [os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_random_shuffle{i}_guided.csv') for i in range(1,4)],
        '1% Sample(3)': [os.path.join(output_dir, #'sampling',
                                   f'{db_str}_{agg}_2atoms_{exp_string}_0.01sample{i}_guided.csv') for i in range(1,4)],
        '5% Sample(3)': [os.path.join(output_dir, #'sampling',
                                   f'{db_str}_{agg}_2atoms_{exp_string}_0.05sample{i}_guided.csv') for i in range(1,4)],
        '10% Sample(3)': [os.path.join(output_dir, #'sampling',
                                   f'{db_str}_{agg}_2atoms_{exp_string}_0.10sample{i}_guided.csv') for i in range(1,4)],
        #'MI': [os.path.join(OUTPUT_DIR, f'{db_str}_{agg}_2atoms_{exp_string}_MI_guided1.csv')],
        #'ANOVA': [os.path.join(OUTPUT_DIR, f'{db_str}_{agg}_2atoms_{exp_string}_Anova_F_Stat_guided1.csv')],
        #'EmbSim': [os.path.join(OUTPUT_DIR, f'{db_str}_{agg}_2atoms_{exp_string}_Cosine_Similarity_guided1.csv')],
        #'Regression': [os.path.join(OUTPUT_DIR, f'{db_str}_{agg}_2atoms_{exp_string}_REGRESSION_guided1.csv')],
        #'Coverage100': [os.path.join(OUTPUT_DIR, f'{db_str}_{agg}_2atoms_{exp_string}_NUM_LARGE_GROUPS_guided1.csv')],
        'Serial Top k': [os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_ALL_TOP_K_SERIAL_guided.csv')],
        'Merged Top k': [os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_ALL_TOP_K_MERGED_guided.csv')],
        'HYPDB': [os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_HYPDB_guided1.csv')],
        'OREO': [os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_OREO_guided.csv')]
        }
    res_path_dict = {'OREO': [os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_OREO_guided.csv')]}
    reference_file = os.path.join(output_dir, f'{db_str}_{agg}_2atoms_{exp_string}_original_order_guided_reference.csv')
    if figure_desc == 'table_time_until_recall':
        get_first_response_time(res_path_dict)
        for k, v in res_path_dict.items():
            print(f"{k}")
            for csv_path in v:
                metric_to_time = find_time_until_specific_score_recall(csv_path, reference_file, threshold=0.95)
                with open(os.path.join(output_dir, "time_to_recall.txt"), "a") as f:
                    f.write(f"{k}: {metric_to_time}")
        return
    stat_dict = None
    for metric_name in metric_names:
        # Sample size exp
        if figure_desc == 'sample_size':
            order = ['1% Sample(3)', '5% Sample(3)', '10% Sample(3)']
            res_path_dict_sub = {k: v for k, v in res_path_dict.items() if k in order}
        # Main methods
        elif figure_desc == 'main':
            # What if we only focused on this naturalness measure:
            #order = ['Merged Top k', 'Serial Top k', 'Original Order', '1KSample', 'Random Order']
            order = ['Merged Top k', 'Original Order', '1% Sample(3)', 'Random Order(3)']
            specific_nat_measure_baseline = metric_to_legend_name[metric_name]
            if specific_nat_measure_baseline is not None and specific_nat_measure_baseline in res_path_dict:
                order.append(specific_nat_measure_baseline)
            res_path_dict_sub = {k: v for k, v in res_path_dict.items() if k in order}
        else:
            print(f"Unsupported figure: {figure_desc}")
            return
        if figure_desc in ('main', 'sample_size'):
            stat_dict = combine_result_files(res_path_dict_sub, metric_name, reference_file, order,
                                             k=100, time_bin_size_in_seconds=30,
                                             max_time_limit_in_seconds=60*10,
                                             output_prefix=f"flights_{agg}_2atoms_{exp_string}_{figure_desc}_{metric_name}",
                                             filter_by_reference=False, time_unit='seconds', prev_stat_dict=stat_dict, base_font_size=26)


def analyze_scale_sensitivity(file_path_template, methods, sample_sizes, recall_metric, output_fname, xlabel, time_unit, pickle_path, num_atoms_changing=False):
    """
    :param file_path_template: should have places for "method_name" and "size"
    :param methods: method names to insert to the file path template
    :param sample_sizes: number of columns or tuples that were sampled
    :param recall_metric: metric to check when we get to 95% recall
    :param output_fname: where to write the output graph
    :return:
    """
    #file_path_template = "data/Folkstable/SevenStates/results/db_width_sensitivity{i}/ACS7_numeric_mean_2atoms_F_gt_M_{method_name}_guided_{num_cols}cols.csv"
    # xs - sample_sizes
    # ys = [s1, s2, ... for each method]
    method_to_series = {m: [] for m in methods}
    #pickle_path = os.path.join(OUTPUT_DIR, 'scale_sensitivity.pickle')
    if os.path.exists(pickle_path):
        print(f"loading from {pickle_path}")
        method_to_series = pickle.load(open(pickle_path, "rb"))
    else:
        for method in methods:
            for sample_size in sample_sizes:
                times_for_method_and_size = []
                for i in [""]:#range(1, 4): # 3 iterations
                    fname = file_path_template.format(method_name=method, size=sample_size, i=i)
                    ref = file_path_template.format(method_name='original_order', size=sample_size, i=i)
                    print(f"Working on: {fname}")
                    max_atoms = MAX_ATOMS
                    if num_atoms_changing:
                        max_atoms = sample_size
                    metric_to_time = find_time_until_specific_score_recall(fname, ref, threshold=0.95,
                                                                           score_name_subset=[recall_metric], k=100,
                                                                           max_atoms=max_atoms)
                    times_for_method_and_size.append(metric_to_time[recall_metric])
                print(f"{method} {sample_size} {times_for_method_and_size}")
                factor = 60 if time_unit == 'minutes' else 1
                method_to_series[method].append(np.mean(times_for_method_and_size)/factor)
        pickle.dump(method_to_series, open(pickle_path, "wb"))
    randomized_methods = {'random_shuffle': 'Random order',
                          'original_order_0.01sample': '1% sample guided',
                          '0.01sample': '1% sample guided'}
    for prefix in randomized_methods:
        rs_keys = [key for key in method_to_series.keys() if key.startswith(prefix)]
        if len(rs_keys) > 0:
            method_to_series[f'{randomized_methods[prefix]}({len(rs_keys)})'] = np.mean(
                [method_to_series[rs] for rs in rs_keys], axis=0)
            index_of_first_key = min([methods.index(rs_key) for rs_key in rs_keys])
            for rs_key in rs_keys:
                del (method_to_series[rs_key])
                methods.remove(rs_key)
            methods.insert(index_of_first_key, f'{randomized_methods[prefix]}({len(rs_keys)})')
            #methods.append(f'{randomized_methods[prefix]}({len(rs_keys)})')

    # rs_keys = [k for k in method_to_series.keys() if k.startswith('random_shuffle')]
    # if len(rs_keys) > 0:
    #     method_to_series[f'random_shuffle({len(rs_keys)})'] = np.mean([method_to_series[rs] for rs in rs_keys], axis=0)
    #     methods.append(f'random_shuffle({len(rs_keys)})')
    #     for rs_key in rs_keys:
    #         del(method_to_series[rs_key])
    #         methods.remove(rs_key)
    if num_atoms_changing:
        # for the legend:
        method_to_series['OREO★'] = [0]
        methods.append('OREO★')
        method_to_series['Full search'] = []
        for m in sample_sizes:
            file_path = file_path_template.format(method_name='ALL_TOP_K_MERGED', size=m, i="") 
            method_to_series['Full search'].append(pd.read_csv(file_path)['Time'].max())
        methods.append('Full search')
    #fig, ax = plt.subplots(figsize=(6, 6))
    fig, ax = plt.subplots()
    for i, m in enumerate(methods):
        legend_label = m
        if m == 'original_order_0.01sample' or m == '0.01sample':
            legend_label = '1% sample guided'
        elif m == 'ALL_TOP_K_SERIAL':
            legend_label = 'Serial Top k'
        elif m == 'ALL_TOP_K_MERGED':
            legend_label = 'Merged Top k'
        elif m == 'original_order':
            legend_label = 'Original order'
        addition = 0
        #if m == 'Full search':
        #    addition = 1
        xs = sample_sizes
        if legend_label == 'OREO★':
            xs = [0]
        ax.plot(xs, method_to_series[m], c=COLORS[i+addition],
                    #marker=MARKERS[i], 
                    #s=60,
                    marker='o',
                    linewidth=4,
                    linestyle=LINESTYLES[i],
                    label=legend_label)
    if sample_sizes[0] > 1000:
        xticks = sample_sizes[::2]
        xlabels = [f"{int(x/1000)}K" for x in xticks]
    else:
        xticks = sample_sizes
        xlabels = sample_sizes
    if num_atoms_changing:
        ax.set_xlim(0.8,5.2)
        ax.legend(fontsize=16)
    ax.set_xticks(xticks, labels=xlabels, fontsize=15)
    ax.tick_params(axis='both', labelsize=15)
    ax.set_xlabel(xlabel, fontsize=20)
    ax.set_ylabel(f'Time ({time_unit})', fontsize=20)
    #plt.rc('xtick', labelsize=20)
    #plt.rc('ytick', labelsize=20)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, output_fname), format="pdf")



def sensitivity_to_k(file_path_template, serial_k_path_template, sampling_file_path_template,
                     methods, ks, recall_metric, output_fname, xlabel,
                     time_unit, pickle_path):
    """
    :param file_path_template: should have places for "method_name" and "size"
    :param methods: method names to insert to the file path template
    :param sample_sizes: number of columns or tuples that were sampled
    :param recall_metric: metric to check when we get to 95% recall
    :param output_fname: where to write the output graph
    :return:
    """
    # file_path_template = "data/Folkstable/SevenStates/results/db_width_sensitivity/ACS7_numeric_mean_2atoms_F_gt_M_{method_name}_guided_{num_cols}cols.csv"
    # xs - sample_sizes
    # ys = [s1, s2, ... for each method]
    method_to_series = {m: [] for m in methods}
    # pickle_path = os.path.join(OUTPUT_DIR, 'scale_sensitivity.pickle')
    if os.path.exists(pickle_path):
        print(f"loading from {pickle_path}")
        method_to_series = pickle.load(open(pickle_path, "rb"))
    else:
        for method in methods:
            for k in ks:
                if method == 'ALL_TOP_K_SERIAL':
                    fname = serial_k_path_template.format(k=k)
                elif 'sample' in method:
                    fname = sampling_file_path_template.format(method_name=method)
                else:
                    fname = file_path_template.format(method_name=method)
                ref = file_path_template.format(method_name='original_order')
                print(f"Working on: {fname}")
                metric_to_time = find_time_until_specific_score_recall(fname, ref, threshold=0.95,
                                                                       score_name_subset=[recall_metric], k=k)
                factor = 60 if time_unit == 'minutes' else 1
                method_to_series[method].append(metric_to_time[recall_metric] / factor)
        pickle.dump(method_to_series, open(pickle_path, "wb"))
    randomized_methods = {'random_shuffle': 'Random order',
                          'original_order_0.01sample_guided': '1% sample guided',
                          '0.01sample': '1% sample guided'}
    for prefix in randomized_methods:
        rs_keys = [key for key in method_to_series.keys() if key.startswith(prefix)]
        if len(rs_keys) > 0:
            method_to_series[f'{randomized_methods[prefix]}({len(rs_keys)})'] = np.mean(
                [method_to_series[rs] for rs in rs_keys], axis=0)
            index_of_first_key = min([methods.index(rs_key) for rs_key in rs_keys])
            for rs_key in rs_keys:
                del (method_to_series[rs_key])
                methods.remove(rs_key)
            methods.insert(index_of_first_key, f'{randomized_methods[prefix]}({len(rs_keys)})')
    #w,h = plt.gcf().get_size_inches()
    #print(f"width, height: {w}, {h}")
    #plt.rcParams["figure.figsize"] = (9,4.8)
    #plt.rcParams["figure.figsize"] = (6,6)
    for i, m in enumerate(methods):
        legend_label = m
        # if m == 'original_order_0.01sample' or m == '0.01sample':
        #     legend_label = '1% sample guided'
        if m == 'ALL_TOP_K_SERIAL':
            legend_label = 'Serial Top k'
        elif m == 'ALL_TOP_K_MERGED':
            legend_label = 'Merged Top k'
        elif m == 'original_order':
            legend_label = 'Original order'
        plt.plot(ks, method_to_series[m], c=COLORS[i],
                    #marker=MARKERS[i],
                    marker='o',
                    #s=60,
                    linestyle=LINESTYLES[i],
                    linewidth=4,
                    label=legend_label)

    xticks = ks
    xlabels = ks

    plt.xticks(ticks=xticks, labels=xlabels, fontsize=15)
    plt.yticks(fontsize=15)
    #plt.legend(fontsize=14, loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlabel(xlabel, fontsize=20)
    plt.ylabel(f'Time ({time_unit})', fontsize=20)
    # plt.rc('xtick', labelsize=20)
    # plt.rc('ytick', labelsize=20)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, output_fname), format="pdf")


def sensitivity_to_num_atoms(file_path_template, m_values, time_unit):
    ys = []
    factor = 60 if time_unit == 'minutes' else 1
    max_times = []
    for m in m_values:
        file_path = file_path_template.format(m=m)
        time_until_recall = find_time_until_specific_score_recall(file_path, file_path, threshold=0.95, score_name_subset=[DF_METRICS_AVERAGE], k=100, max_atoms=m)
        ys.append(time_until_recall[DF_METRICS_AVERAGE]/factor)
        max_times.append(pd.read_csv(file_path)['Time'].max())
    plt.plot(m_values, ys, marker='o', linewidth=4, c=COLORS[0], label="Time to 95% avg. nat. recall")
    plt.plot(m_values, max_times, marker='o', linewidth=4, c=COLORS[1], label="Full search time")
    plt.xlabel("Max atoms", fontsize=20)
    plt.xticks(ticks=m_values, labels=m_values, fontsize=15)
    plt.ylabel(f'Time ({time_unit})', fontsize=20)
    plt.legend(fontsize=14)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "time_to_recall_vs_num_atoms.pdf"), format="pdf")


def analyze_random_query(file_path_template, methods):

    reference_file = file_path_template.format(method="original_order")
    metric_to_time = {}
    for method in methods:
        metric_to_time[method] = find_time_until_specific_score_recall(file_path_template.format(method=method),
                                                                       reference_file, threshold=0.95,
                                                                       score_name_subset=[DF_METRICS_AVERAGE])[DF_METRICS_AVERAGE]
    randomized_methods = {'random_shuffle': 'Random order',
                          '0.01sample': '1% sample guided'}
    for prefix in randomized_methods:
        keys = [k for k in metric_to_time if k.startswith(prefix)]
        avg_result = np.mean([metric_to_time[k] for k in keys])
        for k in keys:
            del metric_to_time[k]
        metric_to_time[f"{randomized_methods[prefix]}({len(keys)})"] = avg_result
    print(metric_to_time)



if __name__ == '__main__':
    metrics = [DF_COSINE_SIMILARITY_STRING, 
               DF_INVERTED_PVALUE_STRING, 
               DF_NORMALIZED_ANOVA_F_STAT_STRING,
               DF_NORMALIZED_MI_STRING, DF_COVERAGE_STRING, DF_METRICS_AVERAGE,
               ]
    #ACS_exp(metrics, "main")
    #sys.exit()
    # ACS_exp(metrics, "sample_size")
    #ACS_exp([], "table_time_until_recall")
    #sys.exit()
    #SO_exp(metrics, "sample_size")
    #SO_exp(metrics, "main")
    #SO_exp([], "table_time_until_recall")
    #sys.exit()
    #flights_exp(metrics, "sample_size")
    #flights_exp(metrics, "main")
    #flights_exp([], "table_time_until_recall")
    # test_for_noise_in_random_shuffle(DF_METRICS_AVERAGE)

    #analyze_random_query("data/Folkstable/SevenStates/results/random_queries/ACS7_numeric_mean_2atoms_MAR_3_gt_1_{method}_guided.csv",
    #                     #"data/SO/results/random_queries/stack_overflow_median_2atoms_Indian_gt_I don''t know_{method}_guided.csv",
    #                     methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL',
    #                              '0.01sample1', '0.01sample2', '0.01sample3',
    #                              'original_order',
    #                              'random_shuffle1', 'random_shuffle2', 'random_shuffle3'])

    # sensitivity_to_num_atoms(
    #     "data/SO/results/m_experiment/stack_overflow_median_{m}atoms_Bsc_gt_Msc_ALL_TOP_K_MERGED_guided1.csv",
    #     [1, 2, 3, 4, 5],
    #     "seconds")
    # sys.exit()

    #sensitivity_to_k(
    #   file_path_template=os.path.join(OUTPUT_DIR, f'{DATABASE_NAME}_{AGG_TYPE}_{MAX_ATOMS}atoms_{QUERY_DESC}_' + '{method_name}_guided.csv'),
    #   serial_k_path_template=os.path.join(OUTPUT_DIR, 'topk', f'{DATABASE_NAME}_{AGG_TYPE}_{MAX_ATOMS}atoms_{QUERY_DESC}'+'_ALL_TOP_K_SERIAL_K{k}_guided.csv'),
    #   sampling_file_path_template=os.path.join(OUTPUT_DIR, 'sampling', f'{DATABASE_NAME}_{AGG_TYPE}_{MAX_ATOMS}atoms_{QUERY_DESC}_original_order_'+'{method_name}.csv'),
    #   methods=['ALL_TOP_K_MERGED',
    #            'ALL_TOP_K_SERIAL',
    #            '0.01sample_guided1', '0.01sample_guided2', '0.01sample_guided3',
    #            #'original_order',
    #            'random_shuffle1', 'random_shuffle2', 'random_shuffle3',
    #            'HYPDB',
    #            'OREO'],
    #    #ks=[20, 40, 60, 80, 100, 120, 140, 160, 180, 200],
    #    ks=list(range(100,1001, 100)),
    #    recall_metric=DF_METRICS_AVERAGE,
    #    output_fname=f"{DATABASE_NAME}_{QUERY_DESC}_k_sensitivity_no_orig.pdf",
    #    xlabel="k value",
    #    time_unit="minutes",
    #    pickle_path=os.path.join(OUTPUT_DIR, 'k_sensitivity_ext.pickle'),
    #)
    #sys.exit()

    # sensitivity to num atoms
    analyze_scale_sensitivity(
         "data/SO/results/m_experiment{i}/stack_overflow_median_{size}atoms_Bsc_gt_Msc_{method_name}_guided.csv",
         methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL', '0.01sample1', '0.01sample2', '0.01sample3', 
                  #'original_order',
                  'random_shuffle1', 'random_shuffle2', 'random_shuffle3', 'HYPDB'],
         sample_sizes=range(1, 6),
         #    #sample_sizes=[10,20,30],
         recall_metric=DF_METRICS_AVERAGE,
         output_fname="SO_Bsc_gt_MSc_median_num_atoms.pdf",
         xlabel="Max atoms",
         time_unit="seconds",
         pickle_path=os.path.join(OUTPUT_DIR, 'num_atoms.pickle'), num_atoms_changing=True
    )
    sys.exit()
    #
    #
    #### sensitivity to width
    analyze_scale_sensitivity(
        "data/Folkstable/SevenStates/results/db_width_sensitivity{i}/ACS7_numeric_mean_2atoms_F_gt_M_{method_name}_guided_{size}cols_iter0.csv",
        methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL', '0.01sample1', '0.01sample2', '0.01sample3', 
                 #'original_order', 
                 'random_shuffle1', 'random_shuffle2', 'random_shuffle3', 'HYPDB'],
         sample_sizes=range(10, 101, 10),
         recall_metric=DF_METRICS_AVERAGE,
         output_fname="ACS_F_gt_M_DB_width_sensitivity_no_orig.pdf",
         xlabel="# columns",
         time_unit="minutes",
         pickle_path=os.path.join(OUTPUT_DIR, 'scale_sensitivity_width_plus_hdb.pickle')
    )
    sys.exit()
    ### sensitivity to size (# tuples)
    analyze_scale_sensitivity(
       "data/Folkstable/SevenStates/results/db_size_sensitivity{i}/ACS7_numeric_mean_2atoms_F_gt_M_{method_name}_guided_{size}_tuples.csv",
        methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL', '0.01sample1', '0.01sample2', '0.01sample3', 
            #'original_order', 
            'random_shuffle1', 'random_shuffle2', 'random_shuffle3', 'HYPDB'],#, 'OREO'],
        sample_sizes=range(100000, 1000001, 100000),
    #    #sample_sizes=range(100000, 600001, 100000),
        recall_metric=DF_METRICS_AVERAGE,
        output_fname="ACS_F_gt_M_DB_size_sensitivity_no_orig.pdf",
        xlabel="# tuples",
        time_unit="minutes",
        pickle_path=os.path.join(OUTPUT_DIR, 'scale_sensitivity_size_w_hypdb.pickle')
    )
    #sys.exit()

    # analyze_scale_sensitivity(
    #    "data/SO/results/db_width_sensitivity/stack_overflow_median_2atoms_Bsc_gr_Msc_{method_name}_guided_{size}cols_iter0.csv",
    #    methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL', '0.01sample', 'original_order', 'random_shuffle1', 'random_shuffle2', 'random_shuffle3'],
    #    sample_sizes=range(10, 50, 5),
    #    recall_metric=DF_METRICS_AVERAGE,
    #    output_fname="SO_Bsc_gr_Msc_DB_width_sensitivity.pdf",
    #    xlabel="DB width (# columns)",
    #    time_unit="seconds",
    #    pickle_path=os.path.join(OUTPUT_DIR, 'scale_sensitivity_width.pickle')
    # )
    #
    # analyze_scale_sensitivity(
    #    "data/SO/results/db_size_sensitivity/stack_overflow_median_2atoms_Bsc_gr_Msc_{method_name}_guided_{size}_tuples.csv",
    #    methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL', '0.01sample', 'original_order', 'random_shuffle1', 'random_shuffle2', 'random_shuffle3'],
    #    sample_sizes=range(10000, 50000, 5000),
    #    recall_metric=DF_METRICS_AVERAGE,
    #    output_fname="ACS_F_gt_M_DB_size_sensitivity.pdf",
    #    xlabel="DB size (# tuples)",
    #    time_unit="seconds",
    #    pickle_path=os.path.join(OUTPUT_DIR, 'scale_sensitivity_size.pickle')
    # )

    #analyze_scale_sensitivity(
    #     "data/flights/results/db_width_sensitivity/flights_large_mean_2atoms_AA_gt_UA_{method_name}_guided_{size}cols_iter0.csv",
    #     methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL', '0.01sample', 'original_order', 'random_shuffle1',
    #              'random_shuffle2', 'random_shuffle3'],
    #     sample_sizes=range(5, 41 ,5),
    #     recall_metric=DF_METRICS_AVERAGE,
    #     output_fname="flights_AA_gt_UA_DB_width_sensitivity.pdf",
    #     xlabel="DB width (# columns)",
    #     time_unit="seconds",
    #     pickle_path=os.path.join(OUTPUT_DIR, 'scale_sensitivity_width.pickle')
    #)

    #analyze_scale_sensitivity(
    #     "data/flights/results/db_size_sensitivity/flights_large_mean_2atoms_AA_gt_UA_{method_name}_guided_{size}_tuples.csv",
    #     methods=['ALL_TOP_K_MERGED', 'ALL_TOP_K_SERIAL', '0.01sample', 'original_order', 'random_shuffle1',
    #              'random_shuffle2', 'random_shuffle3'],
    #     sample_sizes=range(100000, 1000001, 100000),
    #     recall_metric=DF_METRICS_AVERAGE,
    #     output_fname="flights_AA_gt_UA_DB_size_sensitivity.pdf",
    #     xlabel="DB size (# tuples)",
    #     time_unit="seconds",
    #     pickle_path=os.path.join(OUTPUT_DIR, 'scale_sensitivity_size.pickle')
    #)
