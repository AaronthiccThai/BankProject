import React from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import AuthForm from "./pages/Auth.js";
import Dashboard from "./pages/Dashboard.js";
import Transaction from "./pages/Transaction.js";
import Header from "./pages/Header.js";
import './pages/Auth.css';
import './pages/Dashboard.css';
import './pages/DashboardForm.css';

function App() {
  return (
    <Router>
      <MainApp />
    </Router>
  );
}

function MainApp() {
  const location = useLocation();

  // Conditionally render the Header only if not on the login page
  const shouldShowHeader = location.pathname !== "/";

  return (
    <>
      {shouldShowHeader && (
        <Header
          onToggleAddCardForm={() => console.log("Add Card Form toggled")}
          onToggleRemoveCardForm={() => console.log("Remove Card Form toggled")}
        />
      )}
      <Routes>
        <Route path="/" element={<AuthForm />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/transactions" element={<Transaction />} />
      </Routes>
    </>
  );
}

export default App;
