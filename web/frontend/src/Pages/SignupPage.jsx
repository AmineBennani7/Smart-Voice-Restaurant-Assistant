import React, { useState } from 'react';
import '../Components/LoginSignup.css';
import ajustes from '../Assets/ajustes.png';
import password from '../Assets/password.png';
import usuario from '../Assets/usuario.png';
import telefono from '../Assets/ring-phone.png';
import correo from '../Assets/correo-electronico.png';
import { validateFormData, validateEmail, phoneNumberPattern } from '../utils/signupValidator';

import { Link } from 'react-router-dom';

const Signup = () => {
  const [formData, setFormData] = useState({
    fullname: '',
    lastname: '',
    username: '',
    email: '',
    password: '',
    phoneNumber: ''
  });

  // Función para manejar cambios en los campos de entrada
  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  // Conexión con flask api para resgistrarse
  const handleSubmit = async (e) => {
    e.preventDefault();
    // Validar los campos del formulario
    if (!validateFormData(formData)) { 

      return;
    }
    try {
      const response = await fetch('http://localhost:5000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      console.log(data); // Verificar la respuesta del servidor
    } catch (error) {
      console.error('Error al enviar el formulario:', error);
    }
  };

  

  return (
    <div className='container'>
      <div className="header">
        <div className="text">Crear cuenta</div>
        <div className="underline"></div>
      </div>
     
        <form onSubmit={handleSubmit}> {/* Agregar el controlador de eventos onSubmit */}
        <div className="inputs">
          <div className="input">
            <img src={usuario} alt="" style={{ width: '30px', height: '30px' }} />
            <input type="text" name="fullname" placeholder="Nombre" value={formData.fullname} onChange={handleChange} />
          </div>
          <div className="input">
            <img src={usuario} alt="" style={{ width: '30px', height: '30px' }} />
            <input type="text" name="lastname" placeholder="Apellido" value={formData.lastname} onChange={handleChange} />
          </div>
          <div className="input">
            <img src={usuario} alt="" style={{ width: '30px', height: '30px' }} />
            <input type="text" name="username" placeholder="Usuario" value={formData.username} onChange={handleChange} />
          </div>
          <div className="input">
            <img src={correo} alt="" style={{ width: '30px', height: '30px' }} />
            <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} />
          </div>
          <div className="input">
            <img src={password} alt="" style={{ width: '30px', height: '30px' }} />
            <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} />
          </div>
          <div className="input">
            <img src={telefono} alt="" style={{ width: '30px', height: '30px' }} />
            <input type="text" name="phoneNumber" placeholder="Número de Teléfono" value={formData.phoneNumber} onChange={handleChange} />
          </div>
        </div>
        <div className="submit-container">
        <button type="submit" className="submit">Crear cuenta</button>
        </div>
      </form>
      <div className="forgot-password">
       ¿Ya posees tu cuenta? <Link to="/">Iniciar sesión</Link>
      </div>
    </div>
  );
}

export default Signup;
