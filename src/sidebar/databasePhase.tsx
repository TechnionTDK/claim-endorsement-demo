import React, { useContext } from "react";
import { Form } from "react-bootstrap";
import { Phase1Props } from "../utils/interfaces.ts";
import PopupComponent from "../UtilComps/popupComponent.tsx";
const dataBaseOptions = ["Stack Overflow", "US Census", "Flights", "HM"];
import logo from "../assets/logo/Logo.png";

import { MyContext } from "../App.tsx";

const DatabasePhase: React.FC<Phase1Props> = () => {
  const context = useContext(MyContext);

  const { setSelectedDatabase, selectedDatabase, isChangeable } = context!;

  return (
    <div>
      <img
        src={logo}
        alt="Logo"
        style={{
          width: "250px",
          height: "auto",
          marginBottom: "2px",
        }}
      />

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
                fontSize: "15.5px",
                width: "10vw",
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
    </div>
  );
};

export default DatabasePhase;
