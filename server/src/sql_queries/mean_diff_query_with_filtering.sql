WITH value_table AS (SELECT "{column}"
                     FROM {table_name} GROUP BY "{column}"
                     HAVING AVG(CASE WHEN "{grp_attr}"='{value1}' THEN "{target_attr}" ELSE NULL END)<
                            AVG(CASE WHEN "{grp_attr}"='{value2}' THEN "{target_attr}" ELSE NULL END)),
     subset_table AS (SELECT * FROM {table_name} WHERE "{column}" IN (SELECT * FROM value_table)),
     table1 AS (SELECT "{column}",AVG("{target_attr}") AS mean1,COUNT("{target_attr}") AS count1,STDDEV("{target_attr}") AS s1
        FROM subset_table
        WHERE "{grp_attr}"='{value1}'
        GROUP BY "{column}"
        HAVING COUNT("{target_attr}")>1
    ),
    table2 AS (SELECT "{column}", AVG("{target_attr}") AS mean2,COUNT("{target_attr}") AS count2,STDDEV("{target_attr}") AS s2
        FROM subset_table
        WHERE "{grp_attr}"='{value2}'
        GROUP BY "{column}"
        HAVING COUNT("{target_attr}")>1
    ),
    intermediate_table1 AS (SELECT "{column}", mean1,count1,s1,s1*s1/count1 AS intermediate1 FROM table1 WHERE s1>0),
    intermediate_table2 AS (SELECT "{column}", mean2,count2,s2,s2*s2/count2 AS intermediate2 FROM table2 WHERE s2>0),
	joined AS (SELECT * FROM intermediate_table1 INNER JOIN intermediate_table2 USING("{column}"))
    SELECT *, (mean1-mean2)/sqrt(intermediate1+intermediate2) AS T_stat, pow((intermediate1 +intermediate2),2)/(intermediate1*intermediate1/(count1-1) + intermediate2*intermediate2/(count2-1)) AS df
    FROM joined;