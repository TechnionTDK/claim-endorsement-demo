SELECT width_bucket("{column}", {low} ,{high}, {bucket_count}) as bucket,
SELECT {grouping_attrs},
       AVG(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) as mean1,
       COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) as count1,
       STDDEV (CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) as s1,
       AVG(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) as mean2,
       COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) as count2,
       STDDEV (CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) as s2
FROM {table_name} GROUP BY bucket
HAVING AVG(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END)<
       AVG(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)
   AND COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END)>1
   AND COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)>1;