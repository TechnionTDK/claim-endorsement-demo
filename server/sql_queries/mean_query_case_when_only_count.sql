SELECT {selecting_string},
       AVG(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) as mean1,
       COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) as count1,
       AVG(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) as mean2,
       COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) as count2
FROM {table_name} GROUP BY {grouping_string}
HAVING AVG(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END)<
       AVG(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)
   AND COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END)>{min_group_size}
   AND COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)>{min_group_size};