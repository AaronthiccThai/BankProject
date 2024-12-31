import React from "react";
import { Link, useLocation } from "react-router-dom";
const Header = ({ onToggleAddCardForm, onToggleRemoveCardForm  }) => {
  const location = useLocation()
  const isOnTransactionPage = location.pathname === "/transactions";
  return (
    <ul>
      <li>  
        <Link to="/dashboard"> Home </Link>
        <Link to="/transactions">Transactions</Link>
        {!isOnTransactionPage && (
          <div>
            <button onClick={onToggleAddCardForm} className="addButton"> Add Card </button>
            <button onClick={onToggleRemoveCardForm} className="removeButton"> Remove Card </button>
          </div>
        )}        
      </li>
    </ul>
  );
};

export default Header;
