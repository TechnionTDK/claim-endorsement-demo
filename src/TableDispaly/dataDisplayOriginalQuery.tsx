import React, { useContext, useEffect } from "react";

import Predicate from "./predicate";

import { MyContext } from "../App";

import DataHeader from "./dataHeader";

import PredicateComponent from "../UtilComps/PredicateComponent";
import { Button } from "react-bootstrap";

const DataDisplayOriginalQuery: React.FC = () => {
  const context = useContext(MyContext);
  const { originalQueryData } = context!;
  // Define the translation object with the specified type
  return (
    <div className="container">
      <div className={`DataDisplay-row  `} key={`DataDisplay-Original`}>
        <div className={`font-size `} id="DataDisplay-predicate">
          <Predicate
            showIcon={false}
            func={() => {}}
            folded={false}
            predicate={<div>how does the claim hold in the database?</div>}
          ></Predicate>
        </div>
        <DataHeader
          dataValues={{
            N1: originalQueryData[0],
            N2: originalQueryData[1],
          }}
          index={0}
          aggregateFunction={"Count"}
        />
        <DataHeader
          dataValues={{
            N1: originalQueryData[0],
            N2: originalQueryData[1],
          }}
          index={1}
          aggregateFunction={"Count"}
        />

        <div id="DataDisplay-chart">
          <div id="DataDisplay-chart_size"></div>
        </div>

        <div className="font-size" id="DataDisplay-time">
          <div></div>
        </div>
      </div>
    </div>
  );
};

export default DataDisplayOriginalQuery;
