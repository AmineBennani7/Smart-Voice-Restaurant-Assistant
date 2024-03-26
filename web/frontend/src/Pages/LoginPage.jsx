import React, { useState } from 'react';
import '../Components/Styles/LoginSignup.css';
import password from '../Assets/password.png';
import usuario from '../Assets/usuario.png';

import { Link } from 'react-router-dom';


const LoginForm = ({ handleChange, handleSubmit, formData }) => (
  <div className='container'>
    <div className="header">
      <div className="text">Admin</div>
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
   
  </div>
);

export default LoginForm;

