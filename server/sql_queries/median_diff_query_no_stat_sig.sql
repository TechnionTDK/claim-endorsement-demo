WITH discretized AS (
    SELECT {selecting_string},
           "{grp_attr}",
           "{target_attr}"
    FROM {table_name}
    )
SELECT {grouping_string},
       PERCENTILE_CONT(0.5) WITHIN GROUP (
           ORDER BY CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) AS median1,
       COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) as N1,
       PERCENTILE_CONT(0.5) WITHIN GROUP (
           ORDER BY CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) AS median2,
       COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) as N2
FROM discretized
GROUP BY {grouping_string}
HAVING PERCENTILE_CONT(0.5) WITHIN GROUP (
           ORDER BY CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) <
       PERCENTILE_CONT(0.5) WITHIN GROUP (
           ORDER BY CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)
AND COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END)>={min_group_size}
AND COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)>={min_group_size};
