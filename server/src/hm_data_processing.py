from relbench.datasets import get_dataset
import pandas as pd
from utils import age_bucketize

dataset = get_dataset("rel-hm", download=True)
#dataset.val_timestamp, dataset.test_timestamp

db = dataset.get_db()
#dataset.min_timestamp, dataset.max_timestamp
a = db.table_dict['article'].df
c = db.table_dict['customer'].df
c['age_group'] = c['age'].apply(age_bucketize)
t = db.table_dict['transactions'].df
# a = pd.read_csv("data/hm/articles.csv", index_col=0)
# c = pd.read_csv("data/hm/customers.csv", index_col=0)
# t = pd.read_csv("data/hm/transactions.csv", index_col=0)

# Choose a subset of one month long
t2 = t[t["month"] == 11]


m = a.merge(t2, on='article_id').merge(c, on="customer_id")
#m['age_group'] = m['age'].apply(age_bucketize)
#q = m.groupby('age_group')['price'].agg('sum')

# average spent per day, grouped by
price_per_day = t2.groupby(['customer_id', 't_dat'])['price'].sum().reset_index()
m3 = price_per_day.merge(c, on='customer_id')
#m3['age_group'] = m3['age'].apply(age_bucketize)
m3.groupby('age_group')['price'].agg('mean')
