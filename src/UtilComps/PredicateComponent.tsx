import React from "react";

interface PredicateComponentProps {
  attribute1: string;
  value1: string;
  attribute2: string;
  value2: string;
}
const PredicateComponent: React.FC<PredicateComponentProps> = ({
  attribute1,
  value1,
  attribute2,
  value2,
}) => {
  const a1 = attribute1;
  const v1 = value1;
  const a2 = attribute2;
  const v2 = value2;

  // Define the translation object with the specified type

  if (attribute2 == "N/A" || value2 == "N/A") {
    return (
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gridTemplateRows: "auto auto",
        }}
      >
        <div
          style={{
            borderRight: "3px solid #b8b8b8",
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            fontSize: "30px !important",
          }}
        >
          {a1}
        </div>
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
          }}
        >
          {v1}
        </div>
      </div>
    );
  }
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: "1fr 1fr",
        gridTemplateRows: "auto auto",
      }}
    >
      <div
        style={{
          borderRight: "3px solid #b8b8b8",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
        }}
      >
        {a1}
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
        }}
      >
        {v1}
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          borderTop: "3px solid #b8b8b8",
          borderRight: "3px solid #b8b8b8",
        }}
      >
        {a2}
      </div>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          borderTop: "3px solid #b8b8b8",
        }}
      >
        {v2}
      </div>
    </div>
  );
};

export default PredicateComponent;
