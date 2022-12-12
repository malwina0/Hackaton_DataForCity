import React, { useRef } from "react";
import "./MapSubHeader.css";

function MapSubHeader(props) {
  const setDisplayRadius = props.setDisplayRadius;
  const radiusOptions = [1, 2, 3, 4, 5, 10];
  const radiusRef = useRef(null);

  const unclickButtons = () => {
    [...radiusRef.current.children].forEach((child) => {
      if (child.classList.contains("clicked")) {
        child.classList.toggle("clicked");
      }
    });
  };

  const handleRadiusClick = (e) => {
    const value = e.target.innerHTML;
    if (value === "Resetuj") {
      setDisplayRadius(100);
      unclickButtons();
    } else {
      setDisplayRadius(value.slice(0, -2));
      unclickButtons();
      e.target.classList.toggle("clicked");
    }
  };

  const RadiusButtons = (r, index) => {
    return (
      <button key={index} onClick={handleRadiusClick}>
        {r}km
      </button>
    );
  };
  return (
    <div>
      <div className="map">
        <h3>
          Kliknij dowolny punkt na mapie, aby wybrać lokalizację, w promieniu
          której wyświetlą się wydarzenia.
        </h3>
      </div>
      <div ref={radiusRef} className="radius-options">
        <h3>Wybierz promień:</h3>
        {radiusOptions.map(RadiusButtons)}
        <button key={7} onClick={handleRadiusClick}>
          Resetuj
        </button>
      </div>
    </div>
  );
}

export default MapSubHeader;
