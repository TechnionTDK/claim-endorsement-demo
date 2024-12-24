import { useContext, useState } from "react";
import { MyContext } from "../App";
import { Form } from "react-bootstrap";
import { compareValues, groupByOptions } from "../utils/dataDump";

const dataBaseOptions2 = [
  "Masters earns more than Bachelors on avarage (Stack Overflow)",
  "Men earn more than Women on avarage (US Census)",
  "There are more delays on Saturdays than on Mondays (US Flights)",
];
const Examples: React.FC = () => {
  const context = useContext(MyContext);
  const { isChangeable, setExample } = context!;

  const [example, setExampleState] = useState("None");

  interface Example {
    name: string;
    groupBy: number;
    compare1: number;
    compare2: number;
    aggregateFunction: number;
  }

  const examples: { [key: string]: Example } = {
    "Masters earns more than Bachelors on avarage (Stack Overflow)": {
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
    "Men earn more than Women on avarage (US Census)": {
      name: "US Census",
      groupBy: groupByOptions["US Census"].indexOf("Sex"),
      compare1: 0,
      compare2: 1,
      aggregateFunction: 0,
    },
    "There are more delays on Saturdays than on Mondays (US Flights)": {
      name: "Flights",
      groupBy: groupByOptions["Flights"].indexOf("Day of Week"),
      compare1: 1,
      compare2: 6,
      aggregateFunction: 2,
    },
  };

  const selectExample = (e: any) => {
    if (e.target.value === "None") {
      setExampleState("None");
      return;
    }
    const dataName = e.target.value;
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
          marginTop: "1vw",
          display: "flex",

          flexDirection: "row",
          gap: "15px",
          alignItems: "center",
        }}
      >
        <div className="font-size">Examples</div>
        <Form.Select
          disabled={!isChangeable}
          style={{
            height: "1.8vw",
            fontSize: "0.6vw",
            width: "20vw",
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
