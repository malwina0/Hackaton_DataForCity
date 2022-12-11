import React from "react";
import "./HomePage.css";
import "../App.css";
function HomePage(props) {
  return (
    <div className="homepage-container">
      <h1 className="event-header">Strona główna</h1>
      <div className="homepage">
        <h2>Ta strona została stworzona w ramach Hackatonu Data For City.</h2>
        <h2>Wydarzenia</h2>
        <div>
          {" "}
          W zakładce Wydarzenia znajduje się lista wydarzeń w Warszawie,
          domyślnie posortowanych rosnąco względem daty. Można filtrować je
          zgodnie z własnymi potrzebami: wybierając dzielnicę, kategorię, zakres
          dat oraz szukać po słowach kluczowych. <br />
        </div>
        <h2>Mapa</h2>
        <div>
          W sekcji Mapa wydarzenia są zaznaczone na mapie. Można na niej
          zaznaczyć pinezką punkt oraz promień, w którego odległości chcemy
          wyświetlić wydarzenia. Wówczas zostaną one także wylistowane pod mapą.{" "}
          <br />
        </div>
        <h2>Smog</h2>
        <div>
          W zakładce Smog znajduje się prognoza poziomu smogu na kolejne 3 dni z
          wskazaniem, czy spełnia normy WHO.
        </div>
        <h4>Autorzy</h4>
        <div className="authors">
          Damian Bagiński, Jędrzej Sokołowski, Malwina Wojewoda
        </div>
      </div>
    </div>
  );
}

export default HomePage;
