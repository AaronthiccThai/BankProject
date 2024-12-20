import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const AuthForm = () => {
  const [isLogin, setIsLogin] = useState(true); // Track whether the user is logging in or registering
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    name: "",
    dob: "",
    address: ""
  });

  const toggleForm = () => setIsLogin(!isLogin);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };
  const navigate = useNavigate(); // Hook for navigation

  const handleSubmit = async (e) => {
    e.preventDefault();
    const url = isLogin
      ? "http://localhost:5000/auth/login"
      : "http://localhost:5000/auth/register";

    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });

      const data = await response.json();
      if (response.ok) {
        alert(data.message);
        navigate("/dashboard")
        if (!isLogin) setIsLogin(true); // Switch to login after successful registration
      } else {
        alert(data.message);
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred. Please try again.");
    }
  };

  return (
    <div className="auth-form-container">
      <h2>{isLogin ? "Login" : "Register"}</h2>
      <form onSubmit={handleSubmit}>
        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required/>
        <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required/>
        {!isLogin && (
          <>
            <input type="text" name="name" placeholder="Full Name" value={formData.name} onChange={handleChange} required/>
            <input type="date" name="dob" value={formData.dob} onChange={handleChange} required/>
            <input type="text" name="address" placeholder="Address" value={formData.address} onChange={handleChange} required/>
          </>
        )}
        <button type="submit">{isLogin ? "Login" : "Register"}</button>
      </form>
      <p onClick={toggleForm} className="toggle-form">
        {isLogin
          ? "Don't have an account? Register"
          : "Already have an account? Login"}
      </p>
    </div>
  );
};

export default AuthForm;
