import "./App.css";
import Header from "./components/Header";
import HomePage from "./pages/HomePage";
import MapEvents from "./pages/MapEvents";
import Events from "./pages/Events";
import { Route, Routes } from "react-router-dom";
import { useEffect, useRef, useState } from "react";
import Smog from "./pages/Smog";

function App() {
  const eventsContent = useRef(null);
  let [allEvents, setAllEvents] = useState([]);
  useEffect(() => {
    getEvents();
  }, []);

  let getEvents = async () => {
    let response = await fetch("http://127.0.0.1:8000/get_events/");
    let data = await response.json();
    const todayDate = new Date();
    let dataSortedByDate = data
      .filter((event) => {
        // removes events which already ended
        return (
          event.occurrence.filter((ocurr) => {
            return new Date(ocurr.to.split("T")) > todayDate;
          }).length > 0
        );
      })
      .sort((a, b) => {
        // sorts by start date
        let aCurrentDates = a.occurrence.filter((ocurr) => {
          return new Date(ocurr.to.split("T")) > todayDate;
        });
        let bCurrentDates = b.occurrence.filter(
          (ocurr) => new Date(ocurr.to.split("T")) > todayDate
        );
        let aFirstDate = new Date(aCurrentDates[0].to.split("T"));
        let bFirstDate = new Date(bCurrentDates[0].to.split("T"));
        return aFirstDate.getTime() - bFirstDate.getTime();
      });
    setAllEvents(dataSortedByDate);
  };
  return (
    <div className="App">
      <Header />
      <div className="container">
        <div className="content" ref={eventsContent}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route
              path="/events"
              element={
                <Events eventsContent={eventsContent} allEvents={allEvents} />
              }
            />
            <Route path="/map" element={<MapEvents allEvents={allEvents} />} />
            <Route path="/smog" element={<Smog />} />
          </Routes>
        </div>
      </div>
    </div>
  );
}

export default App;
