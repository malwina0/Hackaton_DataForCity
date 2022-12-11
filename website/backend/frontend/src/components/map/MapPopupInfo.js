import React from "react";
import {
  PrepareAddress,
  PrepareDate,
  PrepareImage,
} from "../DataPrepareFunctions";

function MapPopupInfo(props) {
  const event = props.event;
  return (
    <div>
      <h3>{event.title}</h3>
      {/*<div className="column popup_left">*/}
      <PrepareAddress event={event} />
      <PrepareDate event={event} />
      {/*</div>*/}
      {/*<div className="column popup_right">*/}
      <PrepareImage event={event} />
      {/*</div>*/}
    </div>
  );
}

export default MapPopupInfo;
