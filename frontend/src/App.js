import React from "react";
import AuthForm from "./pages/Auth.js";
import Dashboard from "./pages/Dashboard.js";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import './pages/Auth.css'; 
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AuthForm />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}
export default App;
