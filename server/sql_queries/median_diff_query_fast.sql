WITH filtered AS (
    SELECT "{column}",
           PERCENTILE_CONT(0.5) WITHIN GROUP (
               ORDER BY CASE WHEN "{grp_attr}"='{value1}' OR "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) AS total_median,
           PERCENTILE_CONT(0.5) WITHIN GROUP (
               ORDER BY CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) AS median1,
           COUNT(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) as N1,
           PERCENTILE_CONT(0.5) WITHIN GROUP (
               ORDER BY CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) AS median2,
           COUNT(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END) as N2
    FROM {table_name}
    GROUP BY "{column}"
    HAVING PERCENTILE_CONT(0.5) WITHIN GROUP (
               ORDER BY CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END) <
           PERCENTILE_CONT(0.5) WITHIN GROUP (
               ORDER BY CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)
),
inter_table AS (SELECT "{column}","{target_attr}","{grp_attr}",total_median
                FROM {table_name} INNER JOIN filtered USING ("{column}")
),
observed AS (
    SELECT "{column}",
    COUNT(CASE WHEN "{grp_attr}"='{value1}' AND "{target_attr}">total_median THEN "{target_attr}"
                      ELSE NULL END) AS v1_over,
    COUNT(CASE WHEN "{grp_attr}"='{value2}' AND "{target_attr}">total_median THEN "{target_attr}"
                      ELSE NULL END) AS v2_over,
    COUNT(CASE WHEN "{grp_attr}"='{value1}' AND "{target_attr}"<=total_median THEN "{target_attr}"
                      ELSE NULL END) AS v1_under,
    COUNT(CASE WHEN "{grp_attr}"='{value2}' AND "{target_attr}"<=total_median THEN "{target_attr}"
                      ELSE NULL END) AS v2_under
    FROM inter_table
    GROUP BY "{column}"
)
SELECT *
FROM observed NATURAL INNER JOIN filtered
WHERE v1_over+v1_under>={min_group_size} AND v2_over+v2_under>={min_group_size};


-- contingency AS (SELECT "{column}",v1_over,v2_over,v1_under,v2_under,
--         v1_over+v2_over AS over,
--         v1_under+v2_under AS under,
--         v1_over+v1_under AS v1,
--         v2_over+v2_under AS v2,
--         CAST(v1_over+v2_over+v1_under+v2_under AS float) AS total
-- FROM observed
-- WHERE v1_over+v1_under>={min_group_size} AND v2_over+v2_under>={min_group_size}
-- ),
-- expected AS (SELECT "{column}",v1_over,v2_over,v1_under,v2_under,over,under,v1,v2,total,
--             over*v1/total AS e1_over,
--             under*v1/total AS e1_under,
--             over*v2/total AS e2_over,
--             under*v2/total AS e2_under
--             FROM contingency
-- )
-- SELECT "{column}",median1,count1,median2,count2,
--             POWER(ABS(v1_over-e1_over)-0.5,2)/e1_over+
--             POWER(ABS(v1_under-e1_under)-0.5,2)/e1_under+
--             POWER(ABS(v2_over-e2_over)-0.5,2)/e2_over+
--             POWER(ABS(v2_under-e2_under)-0.5,2)/e2_under AS chi_squared_stat
--         FROM expected NATURAL INNER JOIN filtered;
