import { FetchLLMData } from "../BL/FetchFunctions";
import {
  aggregateFunctions,
  compareTitle,
  compareValues,
  groupByOptions,
  translationDict,
  valuesDict,
} from "./dataDump";
import { Data, DataType } from "./interfaces";

export function displayFixed(number: number): string {
  if (number < 0.01) {
    return "<0.01";
  } else {
    return number.toFixed(3);
  }
}
export function TranslatePath(databaseName: string) {
  switch (databaseName) {
    case "Stack Overflow":
      return 0;

    case "Flights":
      return 1;

    case "US Census":
      return 2;

    default:
      return 0;
  }
}
export function TranslateForURL(
  tempSelectedDatabase: string,
  tempAggregateFunction: number,
  tempSelectedGroupBy: number,
  tempSelectedCompare1: number,
  tempSelectedCompare2: number
) {
  console.log(tempSelectedDatabase);
  console.log("use this^");
  let groupbyTextValue =
    groupByOptions[tempSelectedDatabase][tempSelectedGroupBy];
  console.log("tempSelectedDatabase is ");
  console.log(tempSelectedDatabase);

  let db = translationDict[tempSelectedDatabase][tempSelectedDatabase];

  console.log("2y4723647823647823647892364892364928748237489327492 ");
  console.log(translationDict);
  console.log(tempSelectedDatabase);

  console.log(db);
  console.log("2y4723647823647823647892364892364928748237489327492 ");

  let agg = aggregateFunctions[tempAggregateFunction];
  let grp = translationDict[tempSelectedDatabase][groupbyTextValue];
  let g1 =
    compareValues[tempSelectedDatabase][groupbyTextValue][tempSelectedCompare1];
  let g2 =
    compareValues[tempSelectedDatabase][groupbyTextValue][tempSelectedCompare2];
  let argtype = "int";
  if (db == "ACS7" || db == "FLIGHTS" || db == "diabetes" || db == "zillow") {
    console.log(tempSelectedDatabase);
    console.log(translationDict[tempSelectedDatabase]);
    console.log(groupbyTextValue);
    console.log(
      "*************************************************************************"
    );
    console.log(agg);
    console.log(grp);
    console.log(valuesDict[groupbyTextValue][g1]);
    console.log(g1);
    console.log(g2);

    console.log(valuesDict[groupbyTextValue]);
    console.log(valuesDict[groupbyTextValue][g2]);
    g1 = valuesDict[groupbyTextValue][g1];
    g2 = valuesDict[groupbyTextValue][g2];
  }
  return { db, agg, grp, g1, g2, argtype };
}
export function getTextValues(
  aggregateFunction: number,
  selectedDatabase: string,
  selectedGroupBy: number,
  selectedCompare1: number,
  selectedCompare2: number
) {
  const aggregate = aggregateFunctions[aggregateFunction];
  const title = compareTitle[selectedDatabase];

  const compares =
    compareValues[selectedDatabase][
      groupByOptions[selectedDatabase][selectedGroupBy]
    ];

  const compare1 = compares[selectedCompare1];
  const compare2 = compares[selectedCompare2];
  const groupBy = groupByOptions[selectedDatabase][selectedGroupBy];
  return { aggregate, title, groupBy, compare1, compare2 };
}

export async function GetLLMText(
  dataValues: any,
  selectedDatabase: string,
  selectedGroupBy: number,
  selectedCompare1: number,
  selectedCompare2: number,
  aggregateFunction: number,
  modelName: string
) {
  console.log("has started");
  let a = groupByOptions[selectedDatabase][selectedGroupBy];
  let b =
    compareValues[selectedDatabase][
      groupByOptions[selectedDatabase][selectedGroupBy]
    ][selectedCompare1];
  let c =
    compareValues[selectedDatabase][
      groupByOptions[selectedDatabase][selectedGroupBy]
    ][selectedCompare2];
  let functiont = aggregateFunctions[aggregateFunction];
  let db = selectedDatabase;

  let predicate = "";
  let fixedAttribute1 =
    dataValues.attribute1 == "Trans" ? "Transexual" : dataValues.attribute1;
  let fixedAttribute2 =
    dataValues.attribute2 == "Trans" ? "Transexual" : dataValues.attribute2;

  if (dataValues.attribute2 == "N/A") {
    predicate = `${fixedAttribute1}=${dataValues.value1}`;
  } else {
    predicate = `${fixedAttribute1}=${dataValues.value1} and ${fixedAttribute2}=${dataValues.value2}`;
  }
  let g1Data = "N/A";
  let g2Data = "N/A";
  if (selectedDatabase != "Flights" && functiont != "Count") {
    g1Data = dataValues.mean1.toFixed(3);
    g2Data = dataValues.mean2.toFixed(3);
  }
  let g1ValueData = dataValues.N1;
  let g2ValueData = dataValues.N2;

  let g1LeftName = `${a}-${b} `;
  let g1Left = `"${a}-${b} `;
  let g2LeftName = `${a}-${c} `;
  let g2Left = `"${a}-${c} `;
  let g1 = g1Left + `${functiont} ${compareTitle[db]}` + `": ${g1Data}`;
  let g2 = g2Left + `${functiont} ${compareTitle[db]}` + `": ${g2Data}`;
  let g1Value = g1Left + 'count"' + `: ${dataValues.N1}`;
  let g2Value = g2Left + 'count"' + `: ${dataValues.N2}`;
  console.log("sending...");
  console.log(g1Value);
  console.log(g2Value);
  console.log(
    db,
    predicate,
    g1,
    g1Data,
    g1Value,
    g1ValueData,
    g2,
    g2Data,
    g2Value,
    g2ValueData
  );

  const data = await FetchLLMData(
    db,
    predicate,

    g1Data,
    g1ValueData,

    g2Data,
    g2ValueData,
    functiont,
    g1LeftName,
    g2LeftName,
    modelName
  );
  console.log("this is the one that changes");

  console.log(dataValues.index);
  console.log(dataValues);

  return data;
}
export function parseNumber(number: string) {
  var parsed = parseFloat(number);
  if (Number.isInteger(parsed)) {
    return parsed;
  } else {
    return parsed.toFixed(3);
  }
}
export function changeSortingFunction(index: number, old: number[]) {
  const newSort = [...old];

  if (index == newSort[0]) {
    switch (newSort[1]) {
      case 0:
        newSort[1] = 1;
        break;
      case 1:
        newSort[1] = -1;
        break;
      case -1:
        newSort[1] = 0;
        break;

      default:
        break;
    }
    return newSort;
  }
  newSort[0] = index;
  newSort[1] = 1;
  return newSort;
}
export function checksortFunction(
  normRef: React.MutableRefObject<DataType[]>,
  sortingOptions: number[]
) {
  return (data1: Data, data2: Data) => {
    let normalizedValues = normRef.current.map((value) => value.value);
    let data1Normalized = data1.datasets.map(
      (dataset, index) => (dataset.data * normalizedValues[index]) / 100
    );

    let data2Normalized = data2.datasets.map(
      (dataset, index) => (dataset.data * normalizedValues[index]) / 100
    );
    if (sortingOptions[1] != 0) {
      if (sortingOptions[1] != -1) {
        return (
          data2Normalized[sortingOptions[0]] -
          data1Normalized[sortingOptions[0]]
        );
      } else {
        return (
          data1Normalized[sortingOptions[0]] -
          data2Normalized[sortingOptions[0]]
        );
      }
    }
    return (
      data2Normalized.reduce((acc, cv) => acc + cv, 0) -
      data1Normalized.reduce((acc, cv) => acc + cv, 0)
    );
  };
}
