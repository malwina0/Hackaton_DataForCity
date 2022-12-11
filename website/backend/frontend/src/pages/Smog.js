import React from "react";
import SmogPredictions from "../components/smog/SmogPredictions";

function Smog(props) {
  return (
    <div>
      <div className="event-header">
        <h1>Przewidywane poziomy smogu</h1>
      </div>
      <h3 className="smog">
        Planujesz wyjście na nadchodzące wydarzenie w Warszawie? Weź pod uwagę
        przewidywane poziomy smogu w ciągu najbliższych dni.
      </h3>
      <SmogPredictions />
      <h3 className="smog">
        Normy stężeń pyłu zawieszonego zalecane przez Światową Organizację
        Zdrowia (WHO):
      </h3>
      <h3 className="smog">
        <ul>
          <li>norma średniego dziennego stężenia pyłu PM10: 50 µg/m3</li>
          <li>norma średniego rocznego stężenia pyłu PM10: 20 µg/m3</li>
        </ul>
      </h3>
    </div>
  );
}

export default Smog;
