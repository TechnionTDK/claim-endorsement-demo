SELECT width_bucket("{column}", {low} ,{high}, {bucket_count}) as bucket,
COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN 1 ELSE NULL END) as count1,
COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN 1 ELSE NULL END) as count2
FROM {table_name}
GROUP BY bucket
HAVING COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN 1 ELSE NULL END) <
       COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN 1 ELSE NULL END);