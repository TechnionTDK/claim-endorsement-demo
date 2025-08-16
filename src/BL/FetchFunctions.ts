import { compareTitle } from "../utils/dataDump";

let filepaths = [
  "SO",
  "flights",
  "Folkstable/SevenStates",
  "hm",
  "diabetes2",
  "zillow",
];
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
    //console.error("Error fetching the file:", error);
    return [0, 0, 0, 0];
  }
}
export async function StopCalculationWrapper(filepath: number) {
  try {
    console.log("this is the filepath");
    console.log(filepath);

    await fetch(
      `http://localhost:3005/claimendorsement/?pathname=${filepaths[filepath]}`,
      {
        method: "DELETE",
      }
    );
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
    console.log(
      `http://localhost:3005/claimendorsement/?dbname=${encodeURIComponent(
        db
      )}&aggtype=${encodeURIComponent(agg)}&grpattr=${encodeURIComponent(
        grp
      )}&g1=${encodeURIComponent(g1)}&g2=${encodeURIComponent(g2)}`
    );

    await fetch(
      `http://localhost:3005/claimendorsement/?dbname=${encodeURIComponent(
        db
      )}&aggtype=${encodeURIComponent(agg)}&grpattr=${encodeURIComponent(
        grp
      )}&g1=${encodeURIComponent(g1)}&g2=${encodeURIComponent(g2)}`
    );
  } catch (error) {
    alert("Error in fetching data");
    throw new Error("Error in fetching data");
  }
}
export async function GetData(index: number, dbIndex: number) {
  const response = await fetch(
    `http://localhost:3005/claimendorsement/send-data?prev=${index}&dbName=${filepaths[dbIndex]}`
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
  group1data: string,
  g1Amount: string,
  group2data: string,
  g2Amount: string,
  functiont: string,
  g1Name: string,
  g2Name: string,
  modelName: string
) {
  const senddata = {
    compareValue: compareTitle[db],
    databaseName: db,
    predicate: predicate,

    g1Name: g1Name,
    g2Name: g2Name,

    g1CompareValue: group1data,
    g2CompareValue: group2data,

    g1Amount: g1Amount,
    g2Amount: g2Amount,

    function: functiont,
    modelName: modelName,
  };
  console.log(senddata);

  const response = await fetch("http://localhost:3005/claimendorsement/LLM/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(senddata),
  });
  const data = await response.json();

  return data;
}
