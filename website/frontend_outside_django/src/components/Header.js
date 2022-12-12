import React from "react";
import { Link } from "react-router-dom";
import classes from "./Header.module.css";

const Header = () => {
  return (
    <header className={classes.site_header}>
      <ul className={classes.header_list}>
        <li>
          <Link to="/">Strona główna</Link>
        </li>
        <li>
          <Link to="/events">Wydarzenia</Link>
        </li>
        <li>
          <Link to="/map">Mapa</Link>
        </li>
        <li>
          <Link to="/smog">Smog</Link>
        </li>
      </ul>
    </header>
  );
};

export default Header;
