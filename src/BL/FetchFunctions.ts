import { ACS7dict, groupByOptions } from "../utils/dataDump";

export async function retrieveOriginalQuery(
  var1: string,
  var2: string,
  tempSelectedDatabase: string,
  tempSelectedGroupBy: number
) {
  let groupbyTextValue =
    groupByOptions[tempSelectedDatabase][tempSelectedGroupBy];
  console.log(tempSelectedDatabase);

  const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));
  var isUpdated = false;

  console.log(groupbyTextValue);

  while (!isUpdated) {
    try {
      const response = await fetch("./src/assets/demo_test_ORIGINAL.txt");
      const text = await response.text();
      const cleanedText = text.replace(/[{}]/g, "");
      const cleanedText2 = cleanedText.replace(/[']/g, "");
      var splittedText = cleanedText2.split(":");
      splittedText = [
        splittedText[0],
        ...splittedText[1].split(","),
        splittedText[2],
      ];
      console.log(splittedText);
      var rVar1 = splittedText[0];
      var rVar2 = splittedText[2];
      if (tempSelectedDatabase != "Stack Overflow") {
        rVar1 =
          ACS7dict[groupbyTextValue[tempSelectedGroupBy]][
            parseInt(splittedText[0])
          ];
        rVar2 =
          ACS7dict[groupbyTextValue[tempSelectedGroupBy]][
            parseInt(splittedText[2])
          ];
      }
      //jsonData = JSON.parse(text); // Replace single quotes with double quotes

      console.log(var1);
      console.log(rVar1);
      console.log(var2);
      console.log(rVar2);

      if (var1 == rVar1 && var2 == rVar2) {
        console.log("FOUND IT");

        isUpdated = true;
      } else {
        await sleep(100);
      }
    } catch (error) {
      await sleep(100);
      console.error("Error fetching the file:", error);
    }
  }
}
export async function StopCalculationWrapper(filepath: number) {
  try {
    console.log("this is the filepath");
    console.log(filepath);

    await fetch(`http://localhost:3005/project/?pathname=${filepath}`, {
      method: "DELETE",
    });
  } catch (error) {
    alert("Error in fetching data");
    throw new Error("Error in fetching data");
  }
}
export async function StartCalculationWrapper(
  db: string,
  agg: string,
  grp: string,
  g1: string,
  g2: string
) {
  try {
    if (agg == "Avg") {
      agg = "avg";
    }
    await fetch(
      `http://localhost:3005/project/?dbname=${db}&aggtype=${agg}&grpattr=${grp}&g1=${g1}&g2=${g2}`
    );
  } catch (error) {
    alert("Error in fetching data");
    throw new Error("Error in fetching data");
  }
}
export async function GetData(index: number, dbIndex: number) {
  const response = await fetch(
    `http://localhost:3005/project/send-data?prev=${index}&dbIndex=${dbIndex}`
  );
  const data = await response.json();
  if (data.noData) {
    console.log("here");

    alert(
      "This query resulted in no results, please try another one hdfjkdshfjkdshjfkdsh"
    );
    return null;
  }
  if (data.isEmpty || data.data.isEmpty) {
    return null;
  }
  console.log(data.data);

  return { dataUnit: data.data, grouped: data.grouped };
}
export async function FetchLLMData(
  db: string,
  predicate: string,
  group1: string,
  group1data: string,
  group1value: string,
  group1datavalue: string,
  group2: string,
  group2data: string,
  group2value: string,
  group2datavalue: string,
  functiont: string,
  g1LeftName: string,
  g2LeftName: string,
  modelName: string
) {
  const response = await fetch(
    `http://localhost:3005/project/LLM/?databaseName=${db}&predicate=${predicate}&g1=${group1}&g1Data=${group1data}&g1Value=${group1value}&g1ValueData=${group1datavalue}&g2=${group2}&g2Data=${group2data}&g2Value=${group2value}&g2ValueData=${group2datavalue}&function=${functiont} &g1LeftName=${g1LeftName}&g2LeftName=${g2LeftName}&modelName=${modelName}`
  );
  const data = await response.json();

  return data;
}
