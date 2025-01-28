import React, { useContext } from "react";
import { DataHeaderProps } from "../utils/interfaces";
import { MyContext } from "../App";
import { parseNumber } from "../utils/utilFunctions";

const DataHeader: React.FC<DataHeaderProps> = ({
  dataValues,
  index,
  aggregateFunction,
}) => {
  const context = useContext(MyContext);
  const { selectedDatabase } = context!;

  const calcMean = (): number => {
    var parsedMean = 0;
    var mean = "";
    if (index == 0) {
      mean = dataValues.mean1;
    } else {
      mean = dataValues.mean2;
    }
    parsedMean = parseNumber(mean) as number;
    if (selectedDatabase == "HM") {
      return parsedMean;
    } else {
      return parsedMean;
    }
  };
  const calcAmount = (): number => {
    var amount = 0;
    if (index == 0) {
      amount = dataValues.N1;
    } else {
      amount = dataValues.N2;
    }
    return amount;
  };
  const amount = calcAmount();
  const mean = calcMean();

  const condition =
    aggregateFunction === "Count" || selectedDatabase == "Flights";

  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: `1fr ${!condition ? "1fr" : ""}`,
        gridTemplateRows: "auto",
      }}
    >
      {!condition ? (
        <div id="DataDisplay-attr" style={{ fontSize: 30 }}>
          {mean}
        </div>
      ) : null}
      <div id="DataDisplay-value" style={{ fontSize: 30 }}>
        {amount}
      </div>
    </div>
  );
};

export default DataHeader;
