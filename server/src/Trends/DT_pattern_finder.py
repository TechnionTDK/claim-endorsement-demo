from sklearn import tree
from sklearn.tree import plot_tree
import pandas as pd
import matplotlib.pyplot as plt


class DecisionTreePatternFinder(object):
    def __init__(self, df, conf, max_depth=3):
        # The subset of the dataframe columns that should be one-hot encoded should be a list (conf["string_cols"]).
        # The subset of the dataframe to consider in the tree training should be a list conf["include"].
        # row ids to remove should be a list: conf["ids_to_remove"].
        self.df = df.copy()
        self.conf = conf
        self.max_depth = max_depth
        self.tree = None
        self.cols = None

    def find_prominent_attributes(self):
        self.df['remove'] = 0
        self.df.loc[self.conf["ids_to_remove"], 'remove'] = 1

        df_nona = self.df.dropna(subset=[self.conf['outcome_attr'], self.conf['gb_attr']])
        df_nona = df_nona[self.conf["include"] + ["remove"]]

        string_cols = [x for x in self.conf["string_cols"] if x in self.conf['include']]
        df_encoded = pd.get_dummies(df_nona, columns=string_cols, prefix_sep="$")

        X = df_encoded[[col for col in df_encoded.columns if col != "remove"]]
        self.cols = X.columns
        Y = df_encoded["remove"]
        clf = tree.DecisionTreeClassifier(max_depth=self.max_depth)
        clf = clf.fit(X, Y)
        self.tree = clf  # for inspection
        # plt.figure()
        # plot_tree(clf)
        # plt.savefig(self.conf['output_path'].split('.')[0]+'_tree.pdf', format='pdf', bbox_inches="tight")
        features_used = [X.columns[feat] for feat in clf.tree_.feature if feat >= 0]
        orig_feats = []
        for attr in features_used:
            if attr not in self.conf["include"]:
                orig_feats.append(attr.split("$")[0])
            else:
                orig_feats.append(attr)
        return orig_feats




############### draft #####################
# df, conf = read_SO_and_conf()
# ids_to_remove = [61044, 72941, 202, 62027, 70523, 18923, 62224, 66496, 47934, 27426, 20250, 30824, 40790, 1799, 10331, 1889, 39216, 61968, 31042, 51600, 11639, 20938, 50406, 14795, 21415, 21480, 37697, 47086, 62235, 53498, 66811, 67034, 67855, 8344, 16127, 39444, 20165, 309, 1741, 5233]
#
# df['remove'] = 0
# df.loc[ids_to_remove, 'remove'] = 1
#
# df_nona = df.dropna(subset=[conf['outcome_attr'], conf['gb_attr']])
# df_nona = df_nona[conf["include"] + ["remove"]]
#
#
#
# string_cols = ['MainBranch', 'Employment', 'RemoteWork', 'CodingActivities', 'LearnCode', 'OrgSize',
#                'LearnCodeOnline', 'LearnCodeCoursesCert', 'DevType', 'PurchaseInfluence', 'BuyNewTool',
#                'Country', 'LanguageHaveWorkedWith', 'LanguageWantToWorkWith', 'DatabaseHaveWorkedWith',
#                'DatabaseWantToWorkWith', 'PlatformHaveWorkedWith', 'PlatformWantToWorkWith',
#                'WebframeHaveWorkedWith', 'WebframeWantToWorkWith', 'MiscTechHaveWorkedWith',
#                'MiscTechWantToWorkWith', 'ToolsTechHaveWorkedWith', 'ToolsTechWantToWorkWith',
#                'NEWCollabToolsHaveWorkedWith', 'NEWCollabToolsWantToWorkWith', 'OpSysProfessional use',
#                'OpSysPersonal use', 'VersionControlSystem', 'VCInteraction', 'OfficeStackAsyncHaveWorkedWith',
#                'OfficeStackAsyncWantToWorkWith', 'OfficeStackSyncHaveWorkedWith', 'OfficeStackSyncWantToWorkWith',
#                'Blockchain', 'Age', 'Gender', 'Trans', 'Sexuality', 'Ethnicity', 'Accessibility', 'MentalHealth',
#                'ICorPM', 'TimeSearching']
# categorical_to_numeric_encoding = ['OrgSize', 'Age', 'PurchaseInfluence']
# #encoder.fit(df_nona, df_nona['remove'])
# #encoder.fit(df[include], Y)
# string_cols = [x for x in string_cols if x in conf['include']]
# #encoder = OrdinalEncoder(encoding_method='ordered', variables=string_cols, ignore_format=True,
# #                                 missing_values='ignore')
# #encoder.fit(df_nona[include], Y)
# # X = encoder.transform(df_nona[include])
# df_encoded = pd.get_dummies(df_nona, columns=string_cols)
# # df_encoded = df_encoded.drop(string_cols)
# X = df_encoded[[col for col in df_encoded.columns if col != "remove"]]
# Y = df_encoded["remove"]
# clf = tree.DecisionTreeClassifier(max_depth=3)
# clf = clf.fit(X, Y)
# # plot_tree(clf)
# features_used = [X.columns[feat] for feat in clf.tree_.feature if feat >= 0]
