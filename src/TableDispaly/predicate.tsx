import React from "react";
import { PredicateProps } from "../utils/interfaces";
import { Button } from "react-bootstrap";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faChevronDown, faChevronUp } from "@fortawesome/free-solid-svg-icons";

const Predicate: React.FC<PredicateProps> = ({
  predicate,
  func,
  folded,
  showIcon,
}) => {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "row",
        justifyContent: "space-between",
        gap: "5px",
        alignItems: "center",
      }}
    >
      <div>
        {showIcon && (
          <div style={{ marginRight: "20px" }}>
            <Button
              size="sm"
              id={!folded ? "custom-outline-secondary" : "custom-secondary"}
              onClick={(event) => {
                func(event);
              }}
            >
              <FontAwesomeIcon icon={!folded ? faChevronDown : faChevronUp} />
            </Button>
          </div>
        )}
      </div>
      <div style={{ justifyContent: "center", flex: 1 }}>{predicate}</div>
    </div>
  );
};

export default Predicate;
