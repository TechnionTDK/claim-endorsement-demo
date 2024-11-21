from sklearn import tree

class DecisionTreePatternFinder(object):
    def __init__(self, df, conf):
        # assumes the existence of a binary label field that has 1 for rows to remove.
        self.df = df
        self.conf = conf

    def train_and_find_patterns(self):
        # TODO encode to one-hot
        X = self.df[self.conf['include']].values()
        Y = self.df[self.conf['label']]
        clf = tree.DecisionTreeClassifier()
        clf = clf.fit(X, Y)

