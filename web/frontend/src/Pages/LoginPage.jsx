import React, { useState } from 'react';
import '../Components/LoginSignup.css';
import password from '../Assets/password.png';
import usuario from '../Assets/usuario.png';

import { Link } from 'react-router-dom';


const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });


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
      console.log(data); // Muestra la respuesta del backend en la consola
      // Aquí puedes manejar la respuesta del backend según sea necesario
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className='container'>
      <div className="header">
        <div className="text">Login</div>
        <div className="underline"></div>
      </div>
      <form className="inputs" onSubmit={handleSubmit}>
        <div className="input">
          <img src={usuario} alt="" style={{ width: '30px', height: '30px' }} />
          <input type="text" name="username" placeholder="Nombre de usuario" value={formData.username} onChange={handleChange} />
        </div>
        <div className="input">
          <img src={password} alt="" style={{ width: '30px', height: '30px' }} />
          <input type="password" name="password" placeholder="Contraseña" value={formData.password} onChange={handleChange} />
        </div>
        <div className="submit-container">
          <button type="submit" className="submit">Iniciar sesión</button>
        </div>
      </form>
      <div className="forgot-password">
        Contraseña olvidada ? <span>Pulse aquí !</span>
      </div>
      <div className="signup-link">
        Crea tu cuenta aquí: <Link to="/signup">Registrarse</Link>
      </div>
    </div>
  );
}

export default Login;
