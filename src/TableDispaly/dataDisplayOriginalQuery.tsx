import React, { useContext, useEffect } from "react";

import Predicate from "./predicate";

import { MyContext } from "../App";

import DataHeader from "./dataHeader";

const DataDisplayOriginalQuery: React.FC = () => {
  const context = useContext(MyContext);
  const { originalQueryData, collapse } = context!;
  console.log("Original Query Data:", originalQueryData);

  // Define the translation object with the specified type
  return (
    <div
      className="container"
      style={{
        backgroundColor: "#B0C4DE",
        width: "80vw !important",
      }}
    >
      <div
        className={`DataDisplay-row ${collapse ? "collapsed" : "expanded"}`}
        key={`DataDisplay-Original`}
        style={{ width: "120vw !important", backgroundColor: "#B0C4DE" }}
      >
        <div className={`font-size `} id="DataDisplay-predicate">
          <Predicate
            showIcon={false}
            func={() => {}}
            folded={false}
            predicate={
              <div style={{ fontSize: "24px" }}>
                how does the claim hold in the database?
              </div>
            }
          ></Predicate>
        </div>
        <DataHeader
          dataValues={{
            N1: originalQueryData[0],
            N2: originalQueryData[1],
            mean1: originalQueryData[2],
            mean2: originalQueryData[3],
          }}
          index={0}
          aggregateFunction={""}
        />
        <DataHeader
          dataValues={{
            N1: originalQueryData[0],
            N2: originalQueryData[1],
            mean1: originalQueryData[2],
            mean2: originalQueryData[3],
          }}
          index={1}
          aggregateFunction={""}
        />

        <div
          id="DataDisplay-chart"
          style={{
            backgroundColor: "#B0C4DE",
            width: collapse ? "350px" : "300px",
          }}
        >
          <div id="DataDisplay-chart_size"></div>
        </div>

        <div
          className="font-size"
          id="DataDisplay-time"
          style={{ backgroundColor: "#B0C4DE" }}
        >
          <div></div>
        </div>
      </div>
    </div>
  );
};

export default DataDisplayOriginalQuery;
