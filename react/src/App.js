import React, { useState } from "react";
import "./App.css";

function App() {
  const [isLogin, setIsLogin] = useState(true);

  // Toggle between login and register
  const toggleForm = () => {
    setIsLogin(!isLogin);
  };

  return (
    <div className="App">
      <h1 id="Title">SCAM Banking</h1>
      <div className="container">
        <h2 id="form-title">{isLogin ? "Login" : "Register"}</h2>

        {/* Login Form */}
        {isLogin && (
          <form id="auth-form" method="POST" action="http://localhost:5000/auth/login">
            <input type="email" id="email" name="email" placeholder="Email" required />
            <input type="password" id="password" name="password" placeholder="Password" required />
            <button type="submit">Login</button>
          </form>
        )}

        {/* Register Form */}
        {!isLogin && (
          <form id="register-form" method="POST" action="http://localhost:5000/auth/register">
            <input type="email" id="email" name="email" placeholder="Email" required />
            <input type="text" id="name" name="name" placeholder="Full Name" required />
            <input type="password" id="register-password" name="password" placeholder="Password" required />
            <input type="date" id="dob" name="dob" placeholder="Date of Birth" required />
            <input type="text" id="address" name="address" placeholder="Address" required />
            <button type="submit">Register</button>
          </form>
        )}

        {/* Toggle Button */}
        <div className="toggle" onClick={toggleForm}>
          {isLogin ? "Don't have an account? Register" : "Already have an account? Login"}
        </div>
      </div>
    </div>
  );
}

export default App;
