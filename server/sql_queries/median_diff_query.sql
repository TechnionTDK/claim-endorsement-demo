WITH median AS (SELECT "{column}",PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "{target_attr}") AS total_median
                FROM {table_name} WHERE "{target_attr}" IS NOT NULL AND "{grp_attr}"='{value1}' OR "{grp_attr}"='{value2}'
                GROUP BY "{column}"
),
inter_table AS (SELECT "{column}","{target_attr}","{grp_attr}",total_median
            FROM {table_name} INNER JOIN median USING ("{column}")
),
v1_over AS (SELECT "{column}",COUNT(*) AS v1_over
            FROM inter_table
            WHERE "{grp_attr}"='{value1}' AND "{target_attr}">total_median
            GROUP BY "{column}"
),
v2_over AS (SELECT "{column}",COUNT(*) AS v2_over
            FROM inter_table
            WHERE "{grp_attr}"='{value2}' AND "{target_attr}">total_median
            GROUP BY "{column}"
),
v1_under AS (SELECT "{column}",COUNT(*) AS v1_under
            FROM inter_table
            WHERE "{grp_attr}"='{value1}' AND "{target_attr}"<=total_median
            GROUP BY "{column}"
),
v2_under AS (SELECT "{column}",COUNT(*) AS v2_under
            FROM inter_table
            WHERE "{grp_attr}"='{value2}' AND "{target_attr}"<=total_median
            GROUP BY "{column}"
),
observed AS (SELECT "{column}",v1_over,v2_over,v1_under,v2_under,
        v1_over+v2_over AS over,
        v1_under+v2_under AS under,
        v1_over+v1_under AS v1,
        v2_over+v2_under AS v2,
        CAST(v1_over+v2_over+v1_under+v2_under AS float) AS total
FROM v1_over NATURAL INNER JOIN v2_over NATURAL INNER JOIN v1_under NATURAL INNER JOIN v2_under
WHERE v1_over+v1_under>={min_group_size} AND v2_over+v2_under>={min_group_size}
),
expected AS (SELECT "{column}",v1_over,v2_over,v1_under,v2_under,over,under,v1,v2,total,
            over*v1/total AS e1_over,
            under*v1/total AS e1_under,
            over*v2/total AS e2_over,
            under*v2/total AS e2_under
            FROM observed

),
median1 AS (SELECT "{column}",PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "{target_attr}") AS median1, COUNT(*) AS count1
                FROM {table_name} WHERE "{target_attr}" IS NOT NULL AND "{grp_attr}"='{value1}'
                GROUP BY "{column}"
),
median2 AS (SELECT "{column}",PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY "{target_attr}") AS median2, COUNT(*) AS count2
                FROM {table_name} WHERE "{target_attr}" IS NOT NULL AND "{grp_attr}"='{value2}'
                GROUP BY "{column}"
)
SELECT "{column}",median1,count1,median2,count2,
            POWER(ABS(v1_over-e1_over)-0.5,2)/e1_over+
            POWER(ABS(v1_under-e1_under)-0.5,2)/e1_under+
            POWER(ABS(v2_over-e2_over)-0.5,2)/e2_over+
            POWER(ABS(v2_under-e2_under)-0.5,2)/e2_under AS chi_squared_stat
        FROM expected NATURAL INNER JOIN median1 NATURAL INNER JOIN median2
        WHERE median1<median2;
