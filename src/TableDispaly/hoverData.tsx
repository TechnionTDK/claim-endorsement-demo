import React, { useContext } from "react";
import { HoverDataProps } from "../utils/interfaces";
import { displayFixed } from "../utils/utilFunctions";
import { MyContext } from "../App";
import {
  aggregateFunctions,
  parametersAltered,
  parameters,
} from "../utils/dataDump";
const HoverData: React.FC<HoverDataProps> = ({ data, predicate }) => {
  // Implement your component logic here
  const context = useContext(MyContext);
  const { aggregateFunction, maxDiff } = context!;
  if (data === null) return null;
  let usedParameters;
  if (aggregateFunctions[aggregateFunction] == "Count") {
    usedParameters = parametersAltered;
  } else {
    usedParameters = parameters;
  }

  const displaySS = displayFixed(data[0].data);
  const displayStS =
    aggregateFunctions[aggregateFunction] == "Count"
      ? displayFixed(data[1].data / maxDiff)
      : displayFixed(data[1].data);
  const displayAoV = displayFixed(data[2].data);
  const displayMI = displayFixed(data[3].data);
  const displayCov = displayFixed(data[4].data);
  return (
    <div className="main-Div-HoverData">
      <div>{predicate}</div>
      <p></p>
      <div>
        {usedParameters[0]} {displaySS}
      </div>
      <div>
        {usedParameters[1]}
        {displayStS}
      </div>
      <div>
        {usedParameters[2]} {displayAoV}
      </div>
      <div>
        {usedParameters[3]} {displayMI}
      </div>
      <div>
        {usedParameters[4]} {displayCov}
      </div>
    </div>
  );
};

export default HoverData;
