import React from "react";
import "./EventListItem.css";
import {
  PrepareDate,
  PrepareAddress,
  PrepareText,
  PrepareImage,
} from "../DataPrepareFunctions";

function EventListItem({ event }) {
  function Categories({ event }) {
    if (event.category) {
      return (
        <div className="categories">
          <h3>
            {event?.category.length === 1 ? "Kategoria: " : "Kategorie: "}
          </h3>
          <br />
          {event?.category.map((cat) => (
            <p key={event.id.toString().concat(cat.id.toString())}>
              {cat.name}
            </p>
          ))}
        </div>
      );
    }
  }

  return (
    <a href={event.url}>
      <div className="event-list-item">
        <div className="row">
          <div className="column left">
            <h3>{event.title}</h3>
            <Categories event={event} />
            <PrepareText event={event} />
          </div>
          <div className="column middle">
            <h3>Kiedy?</h3>
            <PrepareDate event={event} />
            <h3>Gdzie?</h3>
            <PrepareAddress event={event} />
          </div>
          <div className="column right">
            <PrepareImage event={event} />
          </div>
        </div>
      </div>
    </a>
  );
}

export default EventListItem;
