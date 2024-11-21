import React, { useContext } from "react";
import { DataHeaderProps } from "../utils/interfaces";
import { MyContext } from "../App";
import { parseNumber } from "../utils/utilFunctions";

const DataHeader: React.FC<DataHeaderProps> = ({
  dataValues,
  index,
  aggregateFunction,
}) => {
  const amount = index == 0 ? dataValues.N1 : dataValues.N2;
  const mean = index == 0 ? dataValues.mean1 : dataValues.mean2;
  const context = useContext(MyContext);
  const { selectedDatabase } = context!;
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
          {parseNumber(mean)}
        </div>
      ) : null}
      <div id="DataDisplay-value" style={{ fontSize: 30 }}>
        {amount}
      </div>
    </div>
  );
};

export default DataHeader;
