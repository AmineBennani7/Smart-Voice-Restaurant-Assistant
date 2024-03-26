import React, { useState } from 'react';
import LoginForm from '../Pages/LoginPage'; 
import '../Components/Styles/LoginSignup.css';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: formData.username,
          password: formData.password
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if(data.access_token) {
        localStorage.setItem("token", data.access_token);
        localStorage.setItem("username", formData.username); 
        navigate(`/dashboard/${formData.username}`);
      } else {
        alert("Error al introducir el usuario o la contraseña");      }

    } catch (error) {
      alert("Error al introducir el usuario o la contraseña");
    }
  };

  return <LoginForm handleChange={handleChange} handleSubmit={handleSubmit} formData={formData} />;
};

export default Login;