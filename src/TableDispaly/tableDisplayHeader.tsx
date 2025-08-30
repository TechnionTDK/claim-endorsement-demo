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
  const { collapse, dataArrayLength, loading } = context!;
  const getTextForData = () => {
    if (loading) {
      return (
        <div
          style={{ textAlign: "left", marginLeft: "10px", marginTop: "10px" }}
        >
          <b>{dataArrayLength} </b> results have been fetched so far.
        </div>
      );
    } else {
      return (
        <div
          style={{ textAlign: "left", marginLeft: "10px", marginTop: "10px" }}
        >
          <b>{dataArrayLength} </b> results found.
        </div>
      );
    }
  };
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
      {dataArrayLength > 0 && getTextForData()}
      {/*style={{ marginTop: "25px", width: "80vw" }}*/}
      <div
        style={
          collapse
            ? { marginTop: "15px", width: "80vw" }
            : { marginTop: "15px", width: "64vw" }
        }
        className="seperation-Line"
      ></div>
    </div>
  );
};
export default TableDisplayHeader;
