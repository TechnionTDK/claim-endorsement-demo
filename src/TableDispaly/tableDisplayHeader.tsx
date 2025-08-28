import React, { useContext } from "react";

import HoverData from "./hoverData";
import HeaderDisplay from "./headerDisplay";
import About from "./about";
import { MyContext } from "../App";
const TableDisplayHeader: React.FC<any> = ({
  hoveredData,
  predicateText,
  sortingOptions,
  setSortingOptions,
}) => {
  const context = useContext(MyContext);
  const { collapse } = context!;
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

      {/*style={{ marginTop: "25px", width: "80vw" }}*/}
      <div
        style={
          collapse
            ? { marginTop: "25px", width: "80vw" }
            : { marginTop: "25px", width: "64vw" }
        }
        className="seperation-Line"
      ></div>
    </div>
  );
};
export default TableDisplayHeader;
