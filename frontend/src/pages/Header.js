import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
const Header = ({ onToggleAddCardForm, onToggleRemoveCardForm, toggleSideNav }) => {
  const location = useLocation()
  const isOnTransactionPage = location.pathname === "/transactions";
  const navigate = useNavigate()

  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate("/")
  }


  return (
    <header> 
      <ul>
        <li>  
          <button onClick={toggleSideNav} className="MenuButton">☰</button>
          <Link to="/dashboard"> Home </Link>
          <Link to="/transactions">Transactions</Link>
          {!isOnTransactionPage && (
            <div>
              <button onClick={onToggleAddCardForm} className="addButton"> Add Card </button>
              <button onClick={onToggleRemoveCardForm} className="removeButton"> Remove Card </button>
            </div>
          )}
          <button onClick={handleLogout} className="logoutButton"> Logout </button>
        </li>
      </ul>
    </header> 
  );
};

export default Header;
