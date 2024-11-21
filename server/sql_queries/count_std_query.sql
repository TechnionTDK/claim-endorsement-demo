SELECT STDDEV(count1)
FROM (SELECT {selecting_string}, COUNT(*) as count1
      FROM {table_name} GROUP BY {grouping_string}) as t;
