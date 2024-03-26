import React, { useState } from 'react';
import '../Components/Styles/LoginSignup.css';
import ajustes from '../Assets/ajustes.png';
import password from '../Assets/password.png';
import usuario from '../Assets/usuario.png';
import telefono from '../Assets/ring-phone.png';
import correo from '../Assets/correo-electronico.png';

import { Link } from 'react-router-dom';



 
const SignupForm = ({ handleSubmit, handleChange, formData }) => (

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
            <input type="text" name="phone" placeholder="Número de Teléfono" value={formData.phone} onChange={handleChange} />
          </div>
        </div>
        <div className="submit-container">
        <button type="submit" className="submit">Crear cuenta</button>
        </div>
      </form>
      
    </div>
  );


export default SignupForm;
