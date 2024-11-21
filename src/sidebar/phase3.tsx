import { Button } from "react-bootstrap";
import { useContext } from "react";
import MySlider from "./SliderComponent";
import { Phase3Props } from "../utils/interfaces";
import { MyContext } from "../App";
import PopupComponent from "../UtilComps/popupComponent";
import ClipLoader from "react-spinners/ClipLoader";
import { popupTexts } from "../utils/dataDump";

const Phase3: React.FC<Phase3Props> = ({ clearData }) => {
  const context = useContext(MyContext);
  const {
    loading,
    clearIntervalWrapper,
    setIntervalData,
    intervalData,
    startCalculation,
    stopCalculation,
    isChangeable,
    groupDataBool,
    setGroupDataBool,
  } = context!;
  return (
    <div id="Phase3">
      <PopupComponent
        isTitle={true}
        titleName="Scoring Weights"
        text={"Adjust weights for naturalness measures."}
        className="phase3"
        idName="infoPopupPhase3"
      ></PopupComponent>

      <div>
        <MySlider />

        <div className="buttons-Div-phase3">
          <Button
            disabled={!isChangeable}
            className="font-size"
            style={{ minWidth: "100px" }}
            onClick={async () => {
              clearData(0);
              await stopCalculation();
              await startCalculation();
            }}
          >
            {loading && (
              <ClipLoader
                size={20}
                loading={true}
                speedMultiplier={0.7}
                color="white"
              ></ClipLoader>
            )}
            {!loading && "Start Fetching"}
          </Button>

          <Button
            className="font-size"
            variant="danger"
            style={{ minWidth: "100px" }}
            onClick={async () => {
              if (intervalData === 0) return;
              console.log("-------------------------------------------------");

              await stopCalculation();
              clearIntervalWrapper();
            }}
          >
            Stop Fetching
          </Button>
        </div>
        <div style={{ marginTop: "10px" }}></div>
        <Button
          disabled={!isChangeable}
          variant="warning"
          onClick={() => setGroupDataBool(!groupDataBool)}
        >
          change display{groupDataBool ? "(compact)" : "(full)"}
        </Button>
      </div>
    </div>
  );
};

export default Phase3;
