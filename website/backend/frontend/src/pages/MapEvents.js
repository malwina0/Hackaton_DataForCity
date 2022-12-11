import React, { useEffect, useMemo, useRef, useState } from "react";
import MapPopupInfo from "../components/map/MapPopupInfo";
import {
  MapContainer,
  Marker,
  Popup,
  TileLayer,
  useMapEvents,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import "leaflet.markercluster/dist/MarkerCluster.css";
import "leaflet.markercluster/dist/MarkerCluster.Default.css";
import "./MapEvents.css";
import L from "leaflet";
import MapSubHeader from "../components/map/MapSubHeader";
import EventListItem from "../components/events/EventListItem";
import Pagination from "../components/events/pagination/Pagination";
import MarkerClusterGroup from "../components/MarkerClusterGroup";

function MapEvents(props) {
  let [chosenLocation, setChosenLocation] = useState(null);
  let [mapDisplayEvents, setMapDisplayEvents] = useState([]);
  let [allProperEvents, setAllProperEvents] = useState([]);
  let [displayRadius, setDisplayRadius] = useState(100);
  const markerRef = useRef(null);
  const popupRef = useRef(null);
  const mapRef = useRef(null);

  let PageSize = 5;
  const [currentPage, setCurrentPage] = useState(1);

  const currentTableData = useMemo(() => {
    const firstPageIndex = (currentPage - 1) * PageSize;
    const lastPageIndex = firstPageIndex + PageSize;
    let onlyEvents = [];
    mapDisplayEvents.forEach(function (item) {
      onlyEvents.push(item.event);
    });
    return onlyEvents.slice(firstPageIndex, lastPageIndex);
  }, [currentPage, mapDisplayEvents]);

  const icon = L.icon({
    iconUrl: "/images/marker-icon.png",
    iconSize: [23, 35],
  });

  const icon_pin = L.icon({
    iconUrl: "/images/icons8-map-pin-48.png",
    iconSize: [48, 48],
    iconAnchor: [24, 48],
  });

  const allEvents = props.allEvents;

  useEffect(() => {
    let extractProperEvents = () => {
      let properEvents = [];
      allEvents.forEach((event) => {
        if (event.map?.features[0]) {
          if (event.map.features[0].geometry?.coordinates) {
            properEvents.push({
              event: event,
              coordinates: event.map.features[0].geometry.coordinates,
            });
          }
        }
      });
      return properEvents;
    };

    let initialDisplayEvents = extractProperEvents();
    setAllProperEvents(initialDisplayEvents);
    setMapDisplayEvents(initialDisplayEvents);
  }, [allEvents]);

  useEffect(() => {
    function getEventsInRadius(radius) {
      let pin_localizaton = L.latLng(markerRef.current.getLatLng());
      return allProperEvents.filter((event) => {
        let event_localization = L.latLng([
          event.coordinates[1],
          event.coordinates[0],
        ]);
        return event_localization.distanceTo(pin_localizaton) < radius * 1000;
      });
    }
    setCurrentPage(1);
    if (markerRef.current) {
      setMapDisplayEvents(getEventsInRadius(displayRadius));
    }
  }, [chosenLocation, displayRadius, allProperEvents]);

  const HandleMapClicks = () => {
    const eventHandlers = useMemo(
      () => ({
        dragend() {
          const marker = markerRef.current;
          if (marker != null) {
            setChosenLocation([marker.getLatLng().lat, marker.getLatLng().lng]);
          }
          if (mapRef.current._popup?.isOpen()) {
            mapRef.current._popup.close();
          }
        },
      }),
      []
    );
    useMapEvents({
      click: (e) => {
        // console.log(mapRef.current._popup);
        if (popupRef.current?.isOpen()) {
          popupRef.current.close();
        } else if (mapRef.current._popup?.isOpen()) {
          mapRef.current._popup.close();
        } else {
          setChosenLocation([e.latlng.lat, e.latlng.lng]);
        }
      },
    });
    return chosenLocation ? (
      <Marker
        key={chosenLocation[0]}
        position={chosenLocation}
        eventHandlers={eventHandlers}
        draggable={true}
        icon={icon_pin}
        ref={markerRef}
      >
        <Popup
          position={chosenLocation}
          closeOnClick={false}
          offset={[0, -25]}
          ref={popupRef}
        >
          <div>
            Wybrana lokalizacja: <br />
            {chosenLocation[0]}, {chosenLocation[1]}
          </div>
        </Popup>
      </Marker>
    ) : null;
  };

  return (
    <div>
      <div className="event-header">
        <h1>Mapa wydarzeń w Warszawie</h1>
      </div>
      <MapSubHeader setDisplayRadius={setDisplayRadius} />
      <MapContainer
        className="markercluster-map"
        ref={mapRef}
        center={[52.229808, 21.011833]}
        zoom={12}
        maxZoom={18}
      >
        <HandleMapClicks />
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        />
        <MarkerClusterGroup>
          {mapDisplayEvents &&
            mapDisplayEvents.map((event) => (
              <Marker
                key={event.event.id}
                position={[event.coordinates[1], event.coordinates[0]]}
                icon={icon}
              >
                <Popup closeOnClick={false}>
                  <MapPopupInfo event={event.event} />
                </Popup>
              </Marker>
            ))}
        </MarkerClusterGroup>
      </MapContainer>

      {displayRadius <= 10 && markerRef.current ? (
        mapDisplayEvents && mapDisplayEvents.length > 0 ? (
          <div>
            <Pagination
              className="pagination-bar"
              currentPage={currentPage}
              totalCount={mapDisplayEvents.length}
              pageSize={PageSize}
              onPageChange={(page) => {
                setCurrentPage(page);
              }}
            />
            {currentTableData.map((event, index) => (
              <EventListItem key={index} event={event} />
            ))}
            <Pagination
              className="pagination-bar"
              currentPage={currentPage}
              totalCount={mapDisplayEvents.length}
              pageSize={PageSize}
              onPageChange={(page) => {
                setCurrentPage(page);
              }}
            />
            <div>
              <br />
            </div>
          </div>
        ) : (
          <h3 className="no-events">
            Żadne z wydarzeń nie znajduje się w promieniu {displayRadius}km od
            wybranego punktu
          </h3>
        )
      ) : null}
    </div>
  );
}

export default MapEvents;
