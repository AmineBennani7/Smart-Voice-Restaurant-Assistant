import React, { useState } from 'react';
import LoginForm from '../Pages/LoginPage'; 
import '../Components/Styles/LoginSignup.css';
import { useNavigate } from 'react-router-dom';





const Login = () => {
    const [formData, setFormData] = useState({
      email: '',
      password: ''
    });

const navigate = useNavigate();

  
  
      // Función para manejar cambios en los campos de entrada
  
    const handleChange = (e) => {
      setFormData({
        ...formData,
        [e.target.name]: e.target.value
      });
    };
  
    //Conexión con el backend (FLASK API)
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
        const data = await response.json();
        console.log(data);
        if(data) { // if you got response, navigate to /dashboard
            navigate("/dashboard"); // redirects to dashboard
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    return <LoginForm handleChange={handleChange} handleSubmit={handleSubmit} formData={formData} />;
};


export default Login;
