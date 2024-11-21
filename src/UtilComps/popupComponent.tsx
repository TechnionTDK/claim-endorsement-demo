import React, { useState } from "react";
import { PopupComponentProps } from "../utils/interfaces";
const PopupComponent: React.FC<PopupComponentProps> = ({
  text,
  className,
  idName,
  titleName,
  isTitle,
}) => {
  const [showInfo, setShowInfo] = useState(false);
  let hoverTimeout: number;

  const handleMouseEnter = () => {
    setShowInfo(true);
    hoverTimeout = setTimeout(() => {
      const popup = document.getElementById(idName);
      popup!.classList.toggle("show");
    }, 500);
  };

  const handleMouseLeave = () => {
    clearTimeout(hoverTimeout);
    const t1 = setTimeout(() => {
      const popup = document.getElementById(idName);
      popup!.classList.toggle("show");
    }, 200);
    const t2 = setTimeout(() => {
      setShowInfo(false);
    }, 800);

    return () => {
      clearTimeout(t1);
      clearTimeout(t2);
    };
  };

  return (
    <div className={`${className}-container`}>
      <p className={isTitle ? `${className}-title title-font` : "no-margin"}>
        {titleName}
      </p>
      <div
        className="more-info-icon"
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        ?
      </div>
      {showInfo && (
        <div id={idName} className={`info-popup-${className} info-popup`}>
          <p>{text}</p>
        </div>
      )}
    </div>
  );
};

export default PopupComponent;
