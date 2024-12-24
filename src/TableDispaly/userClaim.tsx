import { useContext } from "react";
import { MyContext } from "../App";

import { getTextValues } from "../utils/utilFunctions";

const UserClaim: React.FC = () => {
  const context = useContext(MyContext);
  const {
    selectedDatabase,
    selectedGroupBy,
    selectedCompare1,
    selectedCompare2,
    aggregateFunction,
  } = context!;
  const { aggregate, title, groupBy, compare1, compare2 } = getTextValues(
    aggregateFunction,
    selectedDatabase,
    selectedGroupBy,
    selectedCompare1,
    selectedCompare2
  );

  const getClaimText = () => {
    return (
      <div className="query-Div-About " style={{ fontSize: 26 }}>
        Claim: <strong>{aggregate}</strong> {title}
        {" of"} <strong>"{compare2}"</strong> {"is larger than that of "}
        <strong>"{compare1}"</strong> {"grouped by"}{" "}
        <strong>"{groupBy}"</strong>
      </div>
    );
  };

  return (
    <div>
      <div className="main-Div-About">{getClaimText()}</div>
    </div>
  );
};

export default UserClaim;
