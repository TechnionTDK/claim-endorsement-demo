import { useContext } from "react";
import * as React from "react";

import { MyContext } from "../App";
import { Sidebar, Menu } from "react-pro-sidebar";

import Phase1 from "./phase1";
import Phase2 from "./phase2";
import Phase3 from "./phase3";

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
          <Phase1
            selectedDatabase={selectedDatabase}
            selectInitial={selectInitial}
          />

          <Phase2 />

          <Phase3 clearData={clearData} />
        </Menu>
      </Sidebar>
    </div>
  );
};

export default MySideBar;
