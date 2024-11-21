import React, { useContext } from "react";
import { Form } from "react-bootstrap";
import { Phase1Props } from "../utils/interfaces";
import PopupComponent from "../UtilComps/popupComponent";
const dataBaseOptions = ["Stack Overflow", "US Census", "Flights"];
import { popupTexts } from "../utils/dataDump.ts";
import { MyContext } from "../App";
const Phase1: React.FC<Phase1Props> = () => {
  const context = useContext(MyContext);

  const { setSelectedDatabase, selectedDatabase, isChangeable } = context!;

  return (
    <div id="phase1">
      <PopupComponent
        isTitle={true}
        titleName="Database"
        text={"Select a database for your claim"}
        className="phase1"
        idName="infoPopupPhase1"
      ></PopupComponent>

      <div>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          <Form.Select
            disabled={!isChangeable}
            style={{
              height: "1.8vw",
              fontSize: "0.6vw",
              width: "8vw",
            }}
            value={selectedDatabase}
            onChange={(e) => setSelectedDatabase(e.target.value)}
          >
            {dataBaseOptions.map((option, index) => (
              <option key={index} value={option}>
                {option}
              </option>
            ))}
          </Form.Select>
        </div>

        <br />
      </div>

      <div className="seperation-Line"></div>
    </div>
  );
};

export default Phase1;
