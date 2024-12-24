import React from "react";

import HoverData from "./hoverData";
import HeaderDisplay from "./headerDisplay";
import About from "./about";
const TableDisplayHeader: React.FC<any> = ({
  hoveredData,
  predicateText,
  sortingOptions,
  setSortingOptions,
}) => {
  return (
    <div>
      {hoveredData === null ? null : (
        <HoverData data={hoveredData} predicate={predicateText} />
      )}
      <About />

      <HeaderDisplay
        sortingOptions={sortingOptions}
        setSortingOptions={setSortingOptions}
      ></HeaderDisplay>

      <div
        style={{ marginTop: "25px", width: "80vw" }}
        className="seperation-Line"
      ></div>
    </div>
  );
};
export default TableDisplayHeader;
