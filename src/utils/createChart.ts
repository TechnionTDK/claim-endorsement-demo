const createDataCompact = (
  databaseData: any,
  aggFunction: string,
  database: string
) => {
  console.log(
    "this is the aggregation function, look at it and love it. PRAISE BE"
  );
  console.log(aggFunction);

  let value = databaseData.grouped.map((data: any) => {
    var mean1 = data.best.mean1;
    var mean2 = data.best.mean2;
    console.log(data);

    if (aggFunction == "Median") {
      mean1 = data.best.median1;
      mean2 = data.best.median2;
    }
    return {
      N1: data.best.N1,
      N2: data.best.N2,
      mean1: mean1,
      mean2: mean2,
      attribute1: data.best.Attr1_str,
      attribute2: data.best.Attr2_str,
      value1: data.best.Value1,
      value2: data.best.Value2,
      datasets: [...createDataset(data.best, aggFunction, database)],
      fullList: createDataFull(data.fullList, aggFunction, database),
      time: data.best.Time,
      explanation: { modelName: "", explanation: "" },
      unfolded: false,
      groupunfold: false,
      loadingExplaintion: false,
    };
  });

  return value;
};
const createDataFull = (
  databaseData: any,
  aggFunction: string,
  database: string
) => {
  let value = databaseData.map((data: any) => {
    var mean1 = data.mean1;
    var mean2 = data.mean2;
    if (aggFunction == "Median") {
      mean1 = data.median1;
      mean2 = data.median2;
    }
    return {
      N1: data.N1,
      N2: data.N2,
      mean1: mean1,
      mean2: mean2,
      attribute1: data.Attr1_str,
      attribute2: data.Attr2_str,
      value1: data.Value1_str,
      value2: data.Value2_str,
      datasets: [...createDataset(data, aggFunction, database)],
      time: data.Time,

      explanation: { modelName: "", explanation: "" },
      unfolded: false,
      groupunfold: false,
      loadingExplantion: false,
    };
  });

  return value;
};

const createDataset = (
  databseValues: any,
  aggFunction: string,
  database: string
) => {
  const dataset = [
    {
      label: "Cosine Similarity",
      data: Math.max(databseValues["Cosine Similarity"], 0),
      backgroundColor: "#2f7d31",
    },
  ];
  if (aggFunction == "Count") {
    dataset.push({
      label: "AggDiff",
      data: Math.max(databseValues["AggDiff"], 0),
      backgroundColor: "#9c27b0",
    });
  } else {
    dataset.push({
      label: "Inverted pvalue",
      data: Math.max(databseValues["Inverted pvalue"], 0),
      backgroundColor: "#9c27b0",
    });
  }
  dataset.push(
    {
      label: "Normalized Anova F Stat",
      data: Math.max(databseValues["Normalized Anova F Stat"], 0),
      backgroundColor: "#ed6d03",
    },
    {
      label: "Normalized MI",
      data: Math.max(0, databseValues["Normalized_MI"]),
      backgroundColor: "#d3302f",
    },
    {
      label: "Coverage",
      data: Math.max(0, databseValues["Coverage"]),
      backgroundColor: "#0088d1",
    }
  );

  return dataset;
};
export const createData = (
  databaseData: any,
  aggFunction: string,
  database: string,
  isCompact = false
) => {
  if (isCompact) {
    return createDataCompact(databaseData, aggFunction, database);
  } else {
    return createDataFull(databaseData, aggFunction, database);
  }
};
