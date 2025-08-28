import React, { useContext, useEffect, useState } from "react";
import { Form } from "react-bootstrap";
import { Phase2Props } from "../utils/interfaces";

import {
  groupByOptions,
  compareValues,
  aggregateFunctions,
  popupTexts,
} from "../utils/dataDump";
import PopupComponent from "../UtilComps/popupComponent";
import { MyContext } from "../App";
import { compareTitle } from "../utils/dataDump";
import Select from "react-select";
import Examples from "../TableDispaly/examples";
const ClaimPhase: React.FC<Phase2Props> = ({}) => {
  const [display, setDisplay] = useState("");
  const context = useContext(MyContext);

  const {
    isChangeable,
    selectedDatabase,

    selectedGroupBy,
    setSelectedGroupBy,

    selectedCompare1,
    setSelectedCompare1,
    selectedCompare2,
    setSelectedCompare2,

    aggregateFunction,
    setAggregateFunction,
  } = context!;
  useEffect(() => {
    setDisplay(groupByOptions[selectedDatabase][selectedGroupBy]);
  }, []);
  useEffect(() => {
    setDisplay(groupByOptions[selectedDatabase][selectedGroupBy]);
  }, [selectedDatabase, selectedGroupBy, selectedCompare1, selectedCompare2]);

  const sty = {
    control: (styles: any) => ({
      ...styles,
      height: "2vw",
      fontSize: "1vw",
      textAlign: "left",
    }),

    singleValue: (provided: any) => ({
      ...provided,
      fontSize: "1vw", // Change this to your desired font size
    }),
    option: (provided: any) => ({
      ...provided,
      fontSize: "1vw", // Change this to your desired font size
      wordBreak: "break-word", // Break words to fit within the container
      hyphens: "auto", // Add hyphens where appropriate
    }),
  };
  const myprint = () => {
    /*console.log(compareValues);
    console.log(selectedDatabase);
    console.log(groupByOptions);
    console.log(groupByOptions[selectedDatabase]);
    console.log(selectedGroupBy);
    console.log(groupByOptions[selectedDatabase][selectedGroupBy]);
    console.log(compareValues[selectedDatabase]);
    console.log(selectedCompare2);

    console.log(
      compareValues[selectedDatabase][
        groupByOptions[selectedDatabase][selectedGroupBy]
      ][selectedCompare2]
    );*/
    return true;
  };
  return (
    <div id="Phase2">
      <PopupComponent
        isTitle={true}
        titleName="Claim"
        text={"Construct the claim to endorse in the database."}
        className="phase2"
        idName="infoPopupPhase2"
      ></PopupComponent>
      <Examples />
      <div>
        <div className="font-size">Group By:</div>
        <Select
          value={{
            value: groupByOptions[selectedDatabase][selectedGroupBy],
            label: groupByOptions[selectedDatabase][selectedGroupBy],
          }}
          styles={sty}
          id="groupby"
          isDisabled={!isChangeable}
          options={groupByOptions[selectedDatabase].map((option, index) => ({
            value: option,
            label: option,
            index: index,
          }))}
          onChange={(e: any) => {
            console.log("this is  e.value:");
            console.log(e.value);

            setSelectedGroupBy(
              groupByOptions[selectedDatabase].indexOf(e.value)
            );
          }}
        ></Select>

        <div className="font-size">Compare:</div>

        <div
          style={{
            display: "grid",
            width: "100%",

            gridTemplateColumns: "1fr 1fr ",
          }}
        >
          <div
            style={{
              display: "flex",
              justifyContent: "center",
            }}
          >
            <Form.Select
              disabled={!isChangeable}
              style={{ height: "2.1vw", fontSize: "1vw", width: "100%" }}
              id="aggregateFunction"
              value={aggregateFunctions[aggregateFunction]}
              onChange={(e) =>
                setAggregateFunction(aggregateFunctions.indexOf(e.target.value))
              }
            >
              {aggregateFunctions.map((option, index) => (
                <option key={index} value={option}>
                  {option}
                </option>
              ))}
            </Form.Select>
          </div>
          <div
            style={{
              fontSize: "0.8vw",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              marginLeft: "5px",
            }}
            className="font-size"
          >
            <Form.Select
              disabled={!isChangeable}
              style={{ height: "2.1vw", fontSize: "1vw", width: "100%" }}
              id="groupattr"
              value={compareTitle[selectedDatabase]}
              onChange={(e) => {}}
            >
              <option
                key={`${compareTitle[selectedDatabase]} of`}
                value={`${compareTitle[selectedDatabase]} of`}
              >
                {`${compareTitle[selectedDatabase]} of`}
              </option>
            </Form.Select>
          </div>
        </div>
        <div style={{ height: "10px" }}></div>
        {myprint() && <div></div>}
        <div className="compare-Div-phase2">
          <div className="half">
            <Select
              styles={sty}
              id="compare2"
              value={{
                value:
                  compareValues[selectedDatabase][
                    groupByOptions[selectedDatabase][selectedGroupBy]
                  ][selectedCompare2],
                label:
                  compareValues[selectedDatabase][
                    groupByOptions[selectedDatabase][selectedGroupBy]
                  ][selectedCompare2],
              }}
              isDisabled={!isChangeable}
              options={compareValues[selectedDatabase][
                groupByOptions[selectedDatabase][selectedGroupBy]
              ]
                .filter(
                  (data) =>
                    compareValues[selectedDatabase][
                      groupByOptions[selectedDatabase][selectedGroupBy]
                    ][selectedCompare1] !== data
                )
                .map((option, index) => ({
                  value: option,
                  label: option,
                  index: index,
                }))}
              onChange={(e: any) => {
                let searchValue = e.value;

                setSelectedCompare2(
                  compareValues[selectedDatabase][
                    groupByOptions[selectedDatabase][selectedGroupBy]
                  ].indexOf(searchValue)
                );
              }}
            ></Select>
          </div>

          <div className="font-size" style={{ justifyContent: "center" }}>
            &gt;
          </div>
          <div className="half">
            <Select
              styles={sty}
              id="compare1"
              value={{
                value:
                  compareValues[selectedDatabase][
                    groupByOptions[selectedDatabase][selectedGroupBy]
                  ][selectedCompare1],
                label:
                  compareValues[selectedDatabase][
                    groupByOptions[selectedDatabase][selectedGroupBy]
                  ][selectedCompare1],
              }}
              isDisabled={!isChangeable}
              options={compareValues[selectedDatabase][
                groupByOptions[selectedDatabase][selectedGroupBy]
              ].map((option, index) => ({
                value: option,
                label: option,
                index: index,
              }))}
              onChange={(e: any) => {
                setSelectedCompare1((_old) => {
                  let searchValue = e.value;

                  let newIndex =
                    compareValues[selectedDatabase][
                      groupByOptions[selectedDatabase][selectedGroupBy]
                    ].indexOf(searchValue);
                  console.log(newIndex);
                  if (newIndex === selectedCompare2) {
                    if (newIndex === 0) {
                      setSelectedCompare2(1);
                    } else {
                      setSelectedCompare2(0);
                    }
                  }
                  return newIndex;
                });
              }}
            ></Select>
          </div>
        </div>

        <br />
      </div>
      <div className="seperator-Div"></div>
      <div className="seperation-Line"></div>
    </div>
  );
};

export default ClaimPhase;
