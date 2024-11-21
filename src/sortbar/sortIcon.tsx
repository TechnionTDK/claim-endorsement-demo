import React from "react";
import { faSort } from "@fortawesome/free-solid-svg-icons";
import { faSortUp } from "@fortawesome/free-solid-svg-icons";
import { faSortDown } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { SortIconProps } from "../utils/interfaces";

const SortIcon: React.FC<SortIconProps> = ({ sorting, color, onClickSort }) => {
  return (
    <div className="main-Div-SortIcon" onClick={onClickSort}>
      {
        sorting == 1 ? (
          <span>
            <FontAwesomeIcon icon={faSortUp} color={color} />
          </span> // Up arrow
        ) : sorting == -1 ? (
          <span>
            <span>
              <FontAwesomeIcon icon={faSortDown} color={color} />
            </span>
          </span>
        ) : (
          <span>
            <span>
              <FontAwesomeIcon icon={faSort} color={color} />
            </span>
          </span>
        )
        // Down arrow
      }
    </div>
  );
};

export default SortIcon;
