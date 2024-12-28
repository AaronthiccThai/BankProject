import React from "react";

const Header = ({ onToggleForm }) => {
  return (
    <ul>
      <li>
        <a href="#">Home</a>
        <a href="#">Transactions</a>
        <button onClick={onToggleForm}>Add Card</button>
      </li>
    </ul>
  );
};

export default Header;
