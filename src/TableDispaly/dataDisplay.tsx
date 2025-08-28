import React, { useContext } from "react";
import { Bar } from "react-chartjs-2";
import Predicate from "./predicate";
import { options } from "../utils/dataDump";
import { DataDisplayProps } from "../utils/interfaces";
import { MyContext } from "../App";

import { aggregateFunctions } from "../utils/dataDump";
import DataHeader from "./dataHeader";

import PredicateComponent from "../UtilComps/PredicateComponent";
import Explanation from "./Explanation";
const DataDisplay: React.FC<DataDisplayProps> = ({
  dataValues,
  setPredicateText,
  setHoveredData,
  index,
  highlightedIndex,
  setHighlightedIndex,
  father,
}) => {
  const context = useContext(MyContext);
  const { groupDataBool, aggregateFunction, unfoldData, collapse, maxDiff } =
    context!;
  // Define the translation object with the specified type

  const displayMoreFunc = (event: any) => {
    event.stopPropagation();
    unfoldData(dataValues.index);
    dataValues.groupunfold = !dataValues.groupunfold;
  };

  return (
    <div className="container">
      <div
        style={{
          backgroundColor:
            dataValues.index == highlightedIndex
              ? ""
              : index % 2 == 0
              ? "var(--light-background, #F4D3D0)"
              : "var(--alternate-background, #f8f4d5)", // Light mode background
        }}
        className={`DataDisplay-row ${
          highlightedIndex === dataValues.index ? "DataDisplay-highlight" : ""
        } ${!father ? "son" : ""} ${collapse ? "collapsed" : "expanded"}`}
        key={`DataDisplay-${dataValues.index}`}
        onMouseEnter={() => {
          //setHoveredData([...data.datasets]);
        }}
        onClick={(event) => {
          setPredicateText(
            <PredicateComponent
              attribute1={dataValues.attribute1}
              value1={dataValues.value1}
              attribute2={dataValues.attribute2}
              value2={dataValues.value2}
            ></PredicateComponent>
          );
          if (dataValues.index == highlightedIndex) {
            setHighlightedIndex("-1");
            setHoveredData(null);
            return;
          } else {
            setHighlightedIndex(dataValues.index);
            setHoveredData([...dataValues.datasets]);
          }
        }}
      >
        <div
          className={`font-size ${
            groupDataBool && father ? "" : "folded_display"
          }`}
          id="DataDisplay-predicate"
        >
          <Predicate
            showIcon={groupDataBool && father}
            func={displayMoreFunc}
            folded={dataValues.unfolded}
            predicate={
              <PredicateComponent
                attribute1={dataValues.attribute1}
                value1={dataValues.value1}
                attribute2={dataValues.attribute2}
                value2={dataValues.value2}
              ></PredicateComponent>
            }
          ></Predicate>
          <div
            style={{
              textAlign: "justify",
              marginTop: "20px",
              marginBottom: "20px",
            }}
          >
            <Explanation dataValues={dataValues}></Explanation>
          </div>
        </div>
        <DataHeader
          dataValues={dataValues}
          index={1}
          aggregateFunction={aggregateFunctions[aggregateFunction]}
        />
        <DataHeader
          dataValues={dataValues}
          index={0}
          aggregateFunction={aggregateFunctions[aggregateFunction]}
        />

        <div
          id="DataDisplay-chart"
          style={{ width: collapse ? "350px" : "300px" }}
        >
          <div
            id="DataDisplay-chart_size "
            style={{ width: collapse ? "335px" : "290px" }}
          >
            <Bar
              options={options}
              data={{
                labels: [""],
                datasets: [
                  ...dataValues.datasets.map((data: any) => {
                    let value = data.data;
                    if (data.label == "AggDiff") {
                      value = value / maxDiff;
                    }
                    return {
                      label: data.label,
                      data: [value],
                      backgroundColor: data.backgroundColor,
                    };
                  }),
                ],
              }}
            />
          </div>
        </div>

        <div id="DataDisplay-time" style={{ fontSize: "25px" }}>
          <div>
            {" "}
            {"<"}
            {parseFloat(dataValues.time + 1).toFixed(0)}s
          </div>
        </div>
      </div>
      {father ? <div className="recursiveDataDiv-border"></div> : <div></div>}
      <div id="recursiveDataDiv">
        {dataValues.unfolded &&
          dataValues.groupunfold &&
          dataValues.fullList &&
          dataValues.fullList.map((item: any, index2: number) => {
            return (
              <DataDisplay
                key={item.index}
                dataValues={item}
                index={index2}
                setPredicateText={setPredicateText}
                setHoveredData={setHoveredData}
                highlightedIndex={highlightedIndex}
                setHighlightedIndex={setHighlightedIndex}
                father={false}
              ></DataDisplay>
            );
          })}
      </div>
    </div>
  );
};

export default DataDisplay;
