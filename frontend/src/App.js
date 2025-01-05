import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, useLocation } from "react-router-dom";
import AuthForm from "./pages/Auth.js";
import Dashboard from "./pages/Dashboard.js";
import Transaction from "./pages/Transaction.js";
import Header from "./pages/Header.js";
import SideNav from "./pages/SideNav.js";
import './pages/Auth.css';
import './pages/Dashboard.css';
import './pages/DashboardForm.css';
import './pages/SideNav.css';
function App() {
  return (
    <Router>
      <MainApp />
    </Router>
  );
}

function MainApp() {
  const location = useLocation();
  const [isSideNavOpen, setIsSideNavOpen] = useState(false);

  // Conditionally render the Header only if not on the login page
  const shouldShowHeader = location.pathname !== "/";
  const toggleSideNav = () => {
    setIsSideNavOpen(!isSideNavOpen);
  };

  return (
    <>
      {location.pathname !== "/" && (
        <SideNav isOpen={isSideNavOpen} toggleNav={toggleSideNav} />
      )}
      
      {shouldShowHeader && <Header toggleSideNav={toggleSideNav} />}
      <Routes>
        <Route path="/" element={<AuthForm />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/transactions" element={<Transaction />} />
      </Routes>
    </>
  );
}

export default App;
