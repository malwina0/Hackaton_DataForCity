import React, { useState, useEffect } from "react";
import "./SmogPredictions.css";
import redCircle from "./images/icons8-red-circle-96.png";
import greenCircle from "./images/icons8-green-circle-96.png";
import orangeCircle from "./images/icons8-orange-circle-96.png";

function SmogPredictions(props) {
  let [predictions, setPredictions] = useState([]);
  useEffect(() => {
    getPredictions();
  }, []);

  let getPredictions = async () => {
    let response = await fetch("http://127.0.0.1:8000/get_smog/");
    let data = await response.json();
    setPredictions(data);
  };

  let icons = [greenCircle, orangeCircle, redCircle];
  let smogDescriptions = [
    "Stężenie smogu poniżej norm dziennych oraz rocznych",
    "Stężenie smogu mniejsze od normy dziennej ale większe od rocznej",
    "Stężenie smogu powyżej norm dziennych oraz rocznych",
  ];

  function singlePrediction(pred) {
    return (
      <div className="forecast-cell">
        <div className="prediction-wrapper">
          <div>{new Date(pred.date).toLocaleDateString("en-US")}</div>
          <div>
            <img
              className="prediction-icon"
              src={icons[pred.prediction]}
              alt="prediction_icon"
            />
          </div>
          <div>{smogDescriptions[pred.prediction]}</div>
        </div>
      </div>
    );
  }
  return (
    <div className="prediction-container">
      {predictions && predictions.map(singlePrediction)}
    </div>
  );
}

export default SmogPredictions;
