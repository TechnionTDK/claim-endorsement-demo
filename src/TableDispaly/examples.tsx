import { useContext, useState } from "react";
import { MyContext } from "../App";
import { Form } from "react-bootstrap";
import { compareValues, groupByOptions } from "../utils/dataDump";
import { HMCompareValues } from "../utils/HM/HMCompareValues";

const dataBaseOptions2 = [
  "(Stack Overflow) Masters earns more than Bachelors on avarage",
  "(Stack Overflow) Self learners with books more than standard education",
  "(Diabetes) People with no hypertension have more cases of diabetes",
  "(Diabetes) People who never smoked vs people who previously smoked",
  "(Zillow) Price of houses with 2 bedrooms is higher than 4 bedrooms",
  "(Zillow) Price of houses built in 2005-2009 is higher than 2000-2004",
  "(H&M) 40 year olds buy more than 25 year olds",
  "(US Census) Women earn more than Men on avarage",
  "(US Flights) There are more delays on Saturdays than on Mondays",
];
const Examples: React.FC = () => {
  const context = useContext(MyContext);
  const { isChangeable, setExample, collapse } = context!;

  const [example, setExampleState] = useState("None");

  interface Example {
    name: string;
    groupBy: number;
    compare1: number;
    compare2: number;
    aggregateFunction: number;
  }

  const examples: { [key: string]: Example } = {
    "(Zillow) Price of houses built in 2005-2009 is higher than 2000-2004": {
      name: "Zillow",
      groupBy: groupByOptions["Zillow"].indexOf("Year range built"),
      compare1:
        compareValues["Zillow"]["Year range built"].indexOf("2000-2004"),
      compare2:
        compareValues["Zillow"]["Year range built"].indexOf("2005-2009"),
      aggregateFunction: 1,
    },

    "(Zillow) Price of houses with 2 bedrooms is higher than 4 bedrooms": {
      name: "Zillow",
      groupBy: groupByOptions["Zillow"].indexOf("Number of bedrooms in home"),
      compare1:
        compareValues["Zillow"]["Number of bedrooms in home"].indexOf("4"),
      compare2:
        compareValues["Zillow"]["Number of bedrooms in home"].indexOf("2"),
      aggregateFunction: 0,
    },
    "(Stack Overflow) Self learners with books more than standard education": {
      name: "Stack Overflow",
      groupBy: groupByOptions["Stack Overflow"].indexOf("Learn Code"),
      compare1: compareValues["Stack Overflow"]["Learn Code"].indexOf(
        "School (i.e., University, College, etc)"
      ),
      compare2: compareValues["Stack Overflow"]["Learn Code"].indexOf(
        "Books / Physical media"
      ),
      aggregateFunction: 0,
    },
    "(Diabetes) People with no hypertension have more cases of diabetes": {
      name: "Diabetes",
      groupBy: groupByOptions["Diabetes"].indexOf("Hypertension"),
      compare1: compareValues["Diabetes"]["Hypertension"].indexOf("Have"),
      compare2:
        compareValues["Diabetes"]["Hypertension"].indexOf("Doesn't Have"),
      aggregateFunction: 0,
    },
    "(Diabetes) People who never smoked vs people who previously smoked": {
      name: "Diabetes",
      groupBy: groupByOptions["Diabetes"].indexOf("Smoking history"),
      compare1: compareValues["Diabetes"]["Smoking history"].indexOf("Former"),
      compare2: compareValues["Diabetes"]["Smoking history"].indexOf("Never"),
      aggregateFunction: 0,
    },
    "(Stack Overflow) Masters earns more than Bachelors on avarage": {
      name: "Stack Overflow",
      groupBy: groupByOptions["Stack Overflow"].indexOf("Education Level"),
      compare1:
        compareValues["Stack Overflow"]["Education Level"].indexOf(
          "Bachelor’s degree"
        ),
      compare2:
        compareValues["Stack Overflow"]["Education Level"].indexOf(
          "Master’s degree"
        ),
      aggregateFunction: 0,
    },
    "(US Census) Women earn more than Men on avarage": {
      name: "US Census",
      groupBy: groupByOptions["US Census"].indexOf("Sex"),
      compare1: 0,
      compare2: 1,
      aggregateFunction: 0,
    },
    "(US Flights) There are more delays on Saturdays than on Mondays": {
      name: "Flights",
      groupBy: groupByOptions["Flights"].indexOf("Day of Week"),
      compare1: 1,
      compare2: 6,
      aggregateFunction: 2,
    },
    "(H&M) 40 year olds buy more than 25 year olds": {
      name: "HM",
      groupBy: groupByOptions["HM"].indexOf("Age"),
      compare1: HMCompareValues.Age.indexOf("25"),
      compare2: HMCompareValues.Age.indexOf("40"),
      aggregateFunction: 2,
    },
  };

  const selectExample = (e: any) => {
    if (e.target.value === "None") {
      setExampleState("None");
      return;
    }

    const dataName = e.target.value;
    console.log(dataName);
    const { name, groupBy, compare1, compare2, aggregateFunction } =
      examples[dataName];
    setExampleState(dataName);
    console.log(name, groupBy, compare1, compare2, aggregateFunction);

    setExample(name, groupBy, compare1, compare2, aggregateFunction);
  };
  return (
    <div>
      <div
        style={{
          display: "flex",

          flexDirection: "column",
          gap: "5px",
          alignItems: "center",
        }}
      >
        <div className="font-size">Examples:</div>
        <Form.Select
          disabled={!isChangeable}
          style={{
            height: "2vw",
            fontSize: "1vw",
            width: collapse ? "14vw" : "30vw",
          }}
          value={example}
          onChange={(e) => selectExample(e)}
        >
          <option value="None">None</option>
          {dataBaseOptions2.map((option, index) => (
            <option key={index} value={option}>
              {option}
            </option>
          ))}
        </Form.Select>
      </div>
    </div>
  );
};

export default Examples;
