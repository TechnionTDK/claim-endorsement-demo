import { useContext } from "react";
import Slider from "@mui/material/Slider";

import * as React from "react";

import { MyContext } from "../App";

import {
  aggregateFunctions,
  parameters,
  parametersAltered,
} from "../utils/dataDump";

const MySlider: React.FC<{}> = () => {
  const context = useContext(MyContext);
  const { normalizedData, setNormalizedData, aggregateFunction } = context!;
  let usedParameters;
  if (aggregateFunctions[aggregateFunction] == "Count") {
    usedParameters = parametersAltered;
  } else {
    usedParameters = parameters;
  }
  const handleChange = (event: any, newValue: number | number[]) => {
    let name = event.target.name;
    setNormalizedData((oldValues) => {
      return oldValues.map((value, _index) => {
        if (value.name === name) {
          return { ...value, value: newValue as number };
        }
        return value;
      });
    });
  };

  return (
    <div id="Slider_Margin">
      <div className="font-size">{usedParameters[0]}</div>
      <Slider
        style={{ margin: "0px", padding: "0px" }}
        color="success"
        aria-label={normalizedData[0].name}
        name={normalizedData[0].name}
        value={normalizedData[0].value}
        onChange={handleChange}
      />

      <div className="font-size">{usedParameters[1]}</div>
      <Slider
        style={{ margin: "0px", padding: "0px" }}
        color="secondary"
        aria-label={normalizedData[1].name}
        name={normalizedData[1].name}
        value={normalizedData[1].value}
        onChange={handleChange}
      />
      <div className="font-size">{usedParameters[2]}</div>
      <Slider
        style={{ margin: "0px", padding: "0px" }}
        color="warning"
        aria-label={normalizedData[2].name}
        name={normalizedData[2].name}
        value={normalizedData[2].value}
        onChange={handleChange}
      />
      <div className="font-size">{usedParameters[3]}</div>
      <Slider
        style={{ margin: "0px", padding: "0px" }}
        color="error"
        aria-label={normalizedData[3].name}
        name={normalizedData[3].name}
        value={normalizedData[3].value}
        onChange={handleChange}
      />
      <div className="font-size">{usedParameters[4]}</div>
      <Slider
        style={{ margin: "0px", paddingBottom: "0.5vh" }}
        color="info"
        aria-label={normalizedData[4].name}
        name={normalizedData[4].name}
        value={normalizedData[4].value}
        onChange={handleChange}
      />
    </div>
  );
};
export default MySlider;
