import React, { useContext } from "react";
import { MyContext } from "../App";
import { AttrHeaderProps } from "../utils/interfaces";

const AttrHeader: React.FC<AttrHeaderProps> = ({
  title,
  attribute1Name,
  attribute2Name,
  aggregateFunction,
}) => {
  const context = useContext(MyContext);
  const { selectedDatabase } = context!;
  const condition =
    aggregateFunction === "Count" || selectedDatabase == "Flights";

  return (
    <div>
      <div className="font-size attrHeader_title">{title}</div>
      <div
        id="firstattr"
        style={{
          display: "grid",
          gridTemplateColumns: `1fr ${condition ? "" : "1fr"}`, // Three equal columns
          gridTemplateRows: "auto", // Rows will adjust based on content
        }}
      >
        <div className="font-size" id="attr1_div">
          {attribute1Name}
        </div>
        {condition ? null : (
          <div className="font-size" id="value1_div">
            {attribute2Name}
          </div>
        )}
      </div>
    </div>
  );
};

export default AttrHeader;
