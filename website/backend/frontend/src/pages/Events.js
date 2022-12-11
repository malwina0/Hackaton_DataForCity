import React, { useState, useEffect, useMemo } from "react";
import Pagination from "../components/events/pagination/Pagination";
import EventListItem from "../components/events/EventListItem";
import EventFilters from "../components/events/EventFilters";

function Events(props) {
  let [filters, setFilters] = useState([[], [], []]);
  let [displayEvents, setDisplayEvents] = useState([]);
  let [maxDate, setMaxDate] = useState(new Date());
  let [query, setQuery] = useState("");

  const eventsContent = props.eventsContent;
  const allEvents = props.allEvents;

  let PageSize = 10;
  const [currentPage, setCurrentPage] = useState(1);

  const currentTableData = useMemo(() => {
    const firstPageIndex = (currentPage - 1) * PageSize;
    const lastPageIndex = firstPageIndex + PageSize;
    return displayEvents.slice(firstPageIndex, lastPageIndex);
  }, [currentPage, displayEvents]);

  useEffect(() => {
    setEventVariables();
  }, [allEvents]);

  function scrollTop() {
    eventsContent.current.scrollTo({ top: 0 });
  }

  useEffect(() => {
    function searchResults(query) {
      return allEvents.filter((event) => {
        if (query === "") {
          return event;
        } else {
          if (event.title) {
            if (event.title.toLowerCase().includes(query.toLowerCase())) {
              return event;
            }
          }
          if (event.lead) {
            if (event.lead.toLowerCase().includes(query.toLowerCase())) {
              return event;
            }
          }
          if (event.text) {
            if (event.text.toLowerCase().includes(query.toLowerCase())) {
              return event;
            }
          }
          return false;
        }
      });
    }

    function filtering(currentEvents, categories) {
      function singleFilter(currentCat) {
        return currentEvents.filter(function (event) {
          let tmp = [];
          event.category?.forEach(function (cat) {
            tmp.push(cat.name === currentCat);
          });
          return tmp.some((el) => el);
        });
      }

      categories.forEach(function (currentCat) {
        currentEvents = singleFilter(currentCat);
      });
      return currentEvents;
    }

    function dateFiltering(currentEvents, dates) {
      const date_start = dates[0];
      const date_end = dates[1];

      return currentEvents.filter(function (event) {
        let tmp = [];

        event.occurrence.forEach(function (ocurr) {
          // Check if event lasts multiple days, if so, compare only end date
          if (
            (new Date(ocurr.to.split("T")) - new Date(ocurr.from.split("T"))) /
              (1000 * 3600 * 24) >
            1
          ) {
            if (event.id === 323) {
              console.log({ date_start });
              console.log({ date_end });
              console.log("date from", new Date(ocurr.from.split("T")));
              console.log("date to", new Date(ocurr.to.split("T")));
              console.log(new Date(ocurr.to.split("T")) <= date_end);
            }
            tmp.push(
              new Date(ocurr.to.split("T")) <= date_end &&
                new Date(ocurr.to.split("T")) >= date_start
            );
          } else {
            tmp.push(
              date_start <= new Date(ocurr.from.split("T")) &&
                new Date(ocurr.to.split("T")) <= date_end
            );
          }
        });
        return tmp.some((el) => el);
      });
    }

    function districtFiltering(currentEvents, districts) {
      return currentEvents.filter(function (event) {
        if (event.localization) {
          return districts.some(
            (distr) => event.localization[0].name === distr
          );
        } else if (event.map && event.map.features && event.map.features[0]) {
          return districts.some(
            (distr) => event.map.features[0].properties.district === distr
          );
        } else {
          return false;
        }
      });
    }

    setCurrentPage(1);

    let currentEvents = searchResults(query);

    if (filters[0].length > 0) {
      currentEvents = filtering(currentEvents, filters[0]);
    }
    if (filters[1].length > 0) {
      currentEvents = dateFiltering(currentEvents, filters[1]);
    }
    if (filters[2].length > 0) {
      currentEvents = districtFiltering(currentEvents, filters[2]);
    }

    setDisplayEvents(currentEvents);
  }, [filters, query, allEvents]);

  let setEventVariables = () => {
    setDisplayEvents(allEvents);
    let max_date = new Date();
    allEvents.forEach(function (event) {
      let curDate = new Date(event.occurrence[0].to.split("T"));
      if (curDate > max_date) {
        max_date = curDate;
      }
    });
    setMaxDate(max_date);
  };

  return (
    <div>
      <div className="event-header">
        <h1>Wydarzenia w Warszawie </h1>
      </div>
      <EventFilters
        setFilters={setFilters}
        maxDate={maxDate}
        allEvents={allEvents}
        setQuery={setQuery}
      />{" "}
      <Pagination
        className="pagination-bar"
        currentPage={currentPage}
        totalCount={displayEvents.length}
        pageSize={PageSize}
        onPageChange={(page) => {
          setCurrentPage(page);
          scrollTop();
        }}
      />
      {displayEvents.length > 0 ? (
        <div>
          {currentTableData.map((event, index) => (
            <EventListItem key={index} event={event} />
          ))}
          <Pagination
            className="pagination-bar"
            currentPage={currentPage}
            totalCount={displayEvents.length}
            pageSize={PageSize}
            onPageChange={(page) => {
              setCurrentPage(page);
              scrollTop();
            }}
          />
          <div>
            <br />
          </div>
        </div>
      ) : (
        <h3 className="no-events">
          Żadne z wydarzeń nie spełnia podanych wymagań
        </h3>
      )}
    </div>
  );
}

export default Events;
