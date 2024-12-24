import { useContext } from "react";
import * as React from "react";

import { MyContext } from "../App";
import { Sidebar, Menu } from "react-pro-sidebar";
import DatabasePhase from "./databasePhase";
import ClaimPhase from "./claimPhase";
import WeightsPhase from "./weightsPhase";

const MySideBar: React.FC = () => {
  const selectInitial = (e: any) => {
    setSelectedDatabase(e.target.value);
  };
  const context = useContext(MyContext);
  const { selectedDatabase, setSelectedDatabase, clearData } = context!;

  return (
    <div style={{ paddingRight: "10px" }}>
      <div id="MySideBar-main_div"></div>

      <Sidebar id="SideBar-Content">
        <div id="SideBar-top_divider"></div>

        <Menu id="SideBar-Menu">
          <DatabasePhase
            selectedDatabase={selectedDatabase}
            selectInitial={selectInitial}
          />

          <ClaimPhase />

          <WeightsPhase clearData={clearData} />
        </Menu>
      </Sidebar>
    </div>
  );
};

export default MySideBar;
