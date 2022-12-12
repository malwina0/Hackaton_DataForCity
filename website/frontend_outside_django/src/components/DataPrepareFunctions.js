import React from "react";

export function PrepareAddress({ event }) {
  if (event.map) {
    let features = event.map.features[0];
    if (
      features &&
      features.properties &&
      Object.keys(features.properties).length > 1
    ) {
      let loc = features.properties;
      let address = loc.shortStreetName.concat(" ", loc.streetNumber);
      let district = loc.district;
      return (
        <div className="event-location">
          {address}
          <br />
          {district}
        </div>
      );
    }
  }
  if (event.address) {
    let address = event.address[0].street;
    let name = event.address[0].name?.toString();
    return (
      <div className="event-location">
        {address}
        <br />
        {name}
      </div>
    );
  }
  if (event.localization) {
    let district = event.localization[0].name;
    return <div className="event-location">{district}</div>;
  }
  return <div className="event-location">Brak danych</div>;
}

export function PrepareImage({ event }) {
  if (event.image) {
    let img = event.image;
    if (img.highlighted) {
      return (
        <img src={event?.image.highlighted.path} alt="Obrazek niedostępny" />
      );
    }
    if (img.small) {
      return <img src={event?.image.small.path} alt="Obrazek niedostępny" />;
    }
  } else {
    return <div className="missing_img">Brak obrazka</div>;
  }
}

export function PrepareText({ event }) {
  function extractContent(s) {
    let span = document.createElement("span");
    span.innerHTML = s;
    return span.textContent || span.innerText;
  }

  function trimText(text) {
    if (text.length > 750) {
      return text.substring(0, 750).concat(" ... ");
    } else return text;
  }
  if (event.lead) {
    return <p>{trimText(event.lead)}</p>;
  }
  if (event.text) {
    return <p>{trimText(extractContent(event.text))}</p>;
  }
}

export function PrepareDate({ event }) {
  if (event.occurrence.length > 1) {
    let times = [];
    event.occurrence
      .filter((ocurr) => new Date(ocurr.to.split("T")) > new Date())
      .forEach(function (ocurr) {
        let date_start = new Date(ocurr.from.split("T"));
        let date_end = new Date(ocurr.to.split("T"));
        if (date_start.toLocaleDateString() === date_end.toLocaleDateString()) {
          times.push([
            date_end.toLocaleDateString(),
            date_start
              .toLocaleTimeString()
              .substring(0, 5)
              .concat(" - ", date_end.toLocaleTimeString().substring(0, 5)),
          ]);
        } else {
          times.push([
            date_start
              .toLocaleDateString()
              .concat(" - ", date_end.toLocaleDateString()),
            date_start
              .toLocaleTimeString()
              .substring(0, 5)
              .concat(" - ", date_end.toLocaleTimeString().substring(0, 5)),
          ]);
        }
      });

    return (
      <div className="event-date">
        {times.map((ocurr, index) => (
          <React.Fragment key={index}>
            {ocurr[0]}
            <br />
            {ocurr[1]}
            <br />
          </React.Fragment>
        ))}
      </div>
    );
  } else {
    let date_start = new Date(event.occurrence[0].from.split("T"));
    let date_end = new Date(event.occurrence[0].to.split("T"));

    if (date_start.toLocaleDateString() === date_end.toLocaleDateString()) {
      return (
        <div className="event-date">
          {date_end.toLocaleDateString()}
          <br />
          {date_start
            .toLocaleTimeString()
            .substring(0, 5)
            .concat(" - ", date_end.toLocaleTimeString().substring(0, 5))}
        </div>
      );
    } else {
      return (
        <div className="event-date">
          {date_start
            .toLocaleDateString()
            .concat(" - ", date_end.toLocaleDateString())}
          <br />
          {date_start
            .toLocaleTimeString()
            .substring(0, 5)
            .concat(" - ", date_end.toLocaleTimeString().substring(0, 5))}
        </div>
      );
    }
  }
}
