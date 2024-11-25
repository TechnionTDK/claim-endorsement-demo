import { ACS7dict, groupByOptions } from "../utils/dataDump";

export async function retrieveOriginalQuery() {
  const sleep = (ms: number) =>
    new Promise((resolve) => setTimeout(resolve, ms));

  try {
    const response = await fetch("./src/assets/demo_test_ORIGINAL.json");
    const text = await response.json();
    console.log(text);
    const agg = (Object.values(text.agg) as number[]).map((value: number) =>
      parseFloat(value.toFixed(3))
    );
    const count = (Object.values(text.count) as number[]).map(
      (value: number) => value
    );
    //jsonData = JSON.parse(text); // Replace single quotes with double quotes

    if (agg.length == 0 || count.length == 0) {
      await sleep(1000);
      return [0, 0, 0, 0];
    } else {
      return [count[0], count[1], agg[0], agg[1]];
    }
  } catch (error) {
    await sleep(1000);
    console.error("Error fetching the file:", error);
    return [0, 0, 0, 0];
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
