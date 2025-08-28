import React, { useContext } from "react";
import { HeaderDisplayProps } from "../utils/interfaces";
import { MyContext } from "../App";
import { getTextValues, changeSortingFunction } from "../utils/utilFunctions";
import AttrHeader from "./attrHeader";
import { aggregateFunctions, compareTitle } from "../utils/dataDump";
import SortBar from "../sortbar/SortBar";
const HeaderDisplay: React.FC<HeaderDisplayProps> = ({
  setSortingOptions,
  sortingOptions,
}) => {
  const context = useContext(MyContext);
  const {
    aggregateFunction,
    selectedDatabase,
    selectedGroupBy,
    selectedCompare1,
    selectedCompare2,
    collapse,
  } = context!;
  const changeSort = (index: number) => {
    setSortingOptions((old) => {
      return changeSortingFunction(index, old);
    });
  };
  return (
    <div id="data_div">
      <div id="setup_div" className={collapse ? "collapsed" : "expanded"}>
        <div className="font-size" id="predicate_div">
          Predicate
        </div>
        <AttrHeader
          title={
            getTextValues(
              aggregateFunction,
              selectedDatabase,
              selectedGroupBy,
              selectedCompare1,
              selectedCompare2
            ).compare2
          }
          attribute1Name={`${aggregateFunctions[aggregateFunction]} ${compareTitle[selectedDatabase]}`}
          attribute2Name="Amount"
          aggregateFunction={aggregateFunctions[aggregateFunction]}
        />
        <AttrHeader
          title={
            getTextValues(
              aggregateFunction,
              selectedDatabase,
              selectedGroupBy,
              selectedCompare1,
              selectedCompare2
            ).compare1
          }
          attribute1Name={`${aggregateFunctions[aggregateFunction]} ${compareTitle[selectedDatabase]}`}
          attribute2Name="Amount"
          aggregateFunction={aggregateFunctions[aggregateFunction]}
        />
        <div id="data_divs">
          <SortBar sortingOptions={sortingOptions} sortFunction={changeSort} />
        </div>

        <div className="font-size" id="time_div">
          Time
        </div>
      </div>
    </div>
  );
};

export default HeaderDisplay;
