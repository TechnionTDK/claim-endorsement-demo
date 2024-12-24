import React, { useContext } from "react";
import { Button } from "react-bootstrap";

import { MyContext } from "../App";
import { GetLLMText } from "../utils/utilFunctions";

interface ExplainaitionProps {
  dataValues: any;
}
const Explanation: React.FC<ExplainaitionProps> = ({ dataValues }) => {
  const context = useContext(MyContext);
  let loadName = `${dataValues.attribute1}${dataValues.attribute2}${dataValues.value1}${dataValues.value2}`;
  const [showExplaination, setShowExplanation] = React.useState(true);
  const {
    selectedGroupBy,
    loadingStates,
    setLoadingStates,
    selectedDatabase,
    selectedCompare1,
    selectedCompare2,
    aggregateFunction,
    SetExplanation,
  } = context!;
  const GetLLM = async () => {
    const sleep = (ms: number) =>
      new Promise((resolve) => setTimeout(resolve, ms));
    try {
      var LLMText = { result: "an error has occurred, try again" };
      var modelName = "flash";
      var errorOccurred = true;
      while (errorOccurred) {
        errorOccurred = false;
        LLMText = await GetLLMText(
          dataValues,
          selectedDatabase,
          selectedGroupBy,
          selectedCompare1,
          selectedCompare2,
          aggregateFunction,
          `gemini-1.5-${modelName}`
        );
        if (LLMText.result == "an error has occurred, try again") {
          modelName = "flash-8b";
          errorOccurred = true;
          await sleep(1000);
        }
      }
      console.log("got here");

      SetExplanation(dataValues.index, LLMText.result, modelName);
      setLoadingStates((old) => [
        ...old.filter((item) => item.name != loadName),
      ]);
    } catch (error) {
      alert(`Error fetching data:${error}`);
    }
  };

  if (dataValues.explanation.explanation == "") {
    return (
      <Button
        variant="outline-secondary"
        id="custom-outline-secondary"
        size="sm"
        style={{ marginTop: "10px", width: "8rem" }}
        disabled={loadingStates.some((item) => loadName == item.name)}
        onClick={(event) => {
          event.stopPropagation(); // Prevent the click event from bubbling up to the parent div

          dataValues.loadingExplantion = true;

          setLoadingStates((old) => [
            ...old,
            {
              name: loadName,
              value: true,
            },
          ]);

          GetLLM();
        }}
      >
        {loadingStates.some((item) => loadName == item.name)
          ? "Loading..."
          : "Explanation"}
      </Button>
    );
  } else {
    return (
      <div style={{ position: "relative" }}>
        <Button
          variant="outline-secondary"
          id="custom-outline-secondary"
          size="sm"
          style={{
            marginTop: "10px",
            width: "5rem",
            fontSize: "14px",
          }}
          onClick={(event) => {
            event.stopPropagation();
            setShowExplanation(!showExplaination);
          }}
        >
          {" "}
          {showExplaination ? `X` : `Show`}
        </Button>
        {showExplaination ? (
          <div className="explanation-info-popup" style={{}}>
            <div
              style={{
                textShadow: `
              -1px -1px 0 #000,  
              1px -1px 0 #000,
              -1px 1px 0 #000,
              1px 1px 0 #000`,
                fontSize: "20px",
              }}
            >
              {dataValues.explanation.explanation}
            </div>
            <div
              style={{
                textAlign: "center",
                position: "absolute",
                fontWeight: "bold",
                bottom: "10px",
                right: "10px",
                fontSize: "8px",
                textShadow: `
                -1px -1px 0 #000,  
                1px -1px 0 #000,
                -1px 1px 0 #000,
                1px 1px 0 #000`,
              }}
            >
              Generated using Google's Gemini {dataValues.explanation.modelName}{" "}
              <br />
            </div>
          </div>
        ) : (
          <div></div>
        )}
      </div>
    );
  }
};

export default Explanation;
