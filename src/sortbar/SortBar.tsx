import React from "react";
import SortIcon from "./sortIcon";
interface SortBarProps {
  sortingOptions: number[];
  sortFunction: (sortid: number) => void;
}

const SortBar: React.FC<SortBarProps> = ({ sortingOptions, sortFunction }) => {
  return (
    <div>
      <div className="font-size attrHeader_title">{"Naturalness Measures"}</div>
      <div
        id="sort-div"
        style={{
          display: "grid",
          marginLeft: "60px",
          marginRight: "45px",

          gridTemplateColumns: " 1fr 1fr 1fr 1fr 1fr",
          gap: "00px",
        }}
      >
        <div>
          <SortIcon
            sorting={sortingOptions[0] == 0 ? sortingOptions[1] : 0}
            color="#2f7d31"
            onClickSort={() => {
              sortFunction(0);
            }}
          />
        </div>
        <div>
          <SortIcon
            sorting={sortingOptions[0] == 1 ? sortingOptions[1] : 0}
            color="#9c27b0"
            onClickSort={() => {
              sortFunction(1);
            }}
          />
        </div>
        <div>
          <SortIcon
            sorting={sortingOptions[0] == 2 ? sortingOptions[1] : 0}
            color="#ed6d03"
            onClickSort={() => {
              sortFunction(2);
            }}
          />
        </div>
        <div>
          <SortIcon
            sorting={sortingOptions[0] == 3 ? sortingOptions[1] : 0}
            color="#d3302f"
            onClickSort={() => {
              sortFunction(3);
            }}
          />
        </div>
        <div>
          <SortIcon
            sorting={sortingOptions[0] == 4 ? sortingOptions[1] : 0}
            color="#0088d1"
            onClickSort={() => {
              sortFunction(4);
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default SortBar;
