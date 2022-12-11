import React, { useEffect, useState } from "react";
import "./EventFilters.css";
import classes from "./EventFilters.module.css";
import DatePicker, { registerLocale } from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import pl from "date-fns/locale/pl";
registerLocale("pl", pl);

function EventFilters(props) {
  let setFilters = props.setFilters;
  let maxDate = props.maxDate;
  let allEvents = props.allEvents;
  let setQuery = props.setQuery;

  const [startDate, setStartDate] = useState(new Date());
  const [endDate, setEndDate] = useState(new Date());
  const [isShown, setIsShown] = useState(false);
  const [catList, setCatList] = useState([]);
  const [districtList, setDistrictList] = useState([]);

  useEffect(() => {
    setEndDate(maxDate);
  }, [maxDate]);

  useEffect(() => {
    const handleFilterSubmit = (e) => {
      setFilters(() => [catList, [startDate, endDate], districtList]);
    };
    handleFilterSubmit();
  }, [catList, startDate, endDate, districtList]);

  const handleShowClick = (e) => {
    setIsShown((current) => !current);
    if (e.target.textContent === "Pokaż filtry") {
      e.target.textContent = "Schowaj filtry";
    } else {
      e.target.textContent = "Pokaż filtry";
    }
  };

  const handleCategoryClick = (e) => {
    const value = e.target.innerHTML;
    let index = catList.indexOf(value);
    if (index === -1) {
      setCatList((catList) => [...catList, value]);
      e.target.classList.toggle("clicked");
    } else {
      setCatList(catList.filter((item) => item !== value));
      e.target.classList.toggle("clicked");
    }
  };

  const handleDistrictClick = (e) => {
    const value = e.target.innerHTML;
    let index = districtList.indexOf(value);
    if (index === -1) {
      setDistrictList((districtList) => [...districtList, value]);
      e.target.classList.toggle("clicked");
    } else {
      setDistrictList(districtList.filter((item) => item !== value));
      e.target.classList.toggle("clicked");
    }
  };

  let allCategories = new Set();
  let allDistricts = new Set();

  allEvents.forEach(function (event) {
    event.category?.forEach(function (cat) {
      allCategories.add(cat.name);
    });
    if (event.localization) {
      allDistricts.add(event.localization[0].name);
    } else {
    }
  });

  allCategories = Array.from(allCategories).sort();
  allDistricts = Array.from(allDistricts).sort();

  const CatButtons = (cat, index) => {
    return (
      <button key={index} onClick={handleCategoryClick}>
        {cat}
      </button>
    );
  };

  const DistrictButtons = (district, index) => {
    return (
      <button key={index} onClick={handleDistrictClick}>
        {district}
      </button>
    );
  };

  return (
    <div className="filters_container">
      <button className="show-filters" onClick={handleShowClick}>
        Pokaż filtry
      </button>
      <input
        className="search_input"
        placeholder="Szukaj wydarzenia"
        onChange={(event) => setQuery(event.target.value)}
      />
      <div className={isShown ? null : classes.notvisible}>
        <div className="filters">
          <div className="filter_categories">
            <h3>Kategorie:</h3>
            {allCategories.map(CatButtons)}
          </div>
          <p className="filter_info">
            Wyświetlone zostaną wydarzenia zawierające wszystkie z zaznaczonych
            kategorii
          </p>
          <div className="filter_categories">
            <h3>Lokalizacje:</h3>
            {allDistricts.map(DistrictButtons)}
          </div>
          <p className="filter_info">
            Wyświetlone zostaną wszystkie wydarzenia odbywające się w
            zaznaczonych lokalizacjach
          </p>
          <div className="dates">
            <h3>Data:</h3>
            <div className="dates-inner">
              <h4>Od:</h4>
              <DatePicker
                popperPlacement="bottom"
                locale="pl"
                dateFormat="dd/MM/yyyy"
                selected={startDate}
                onChange={(date) => setStartDate(date)}
              />
              <h4>Do:</h4>
              <DatePicker
                popperPlacement="bottom"
                locale="pl"
                dateFormat="dd/MM/yyyy"
                selected={endDate}
                onChange={(date) => setEndDate(date)}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default EventFilters;
