import React from 'react';
import '../Components/Styles/LoginSignup.css';
import ajustes from '../Assets/ajustes.png';
import password from '../Assets/password.png';
import usuario from '../Assets/usuario.png';
import telefono from '../Assets/ring-phone.png';
import correo from '../Assets/correo-electronico.png';
import { useNavigate, useParams } from 'react-router-dom';

import { Button } from 'react-bootstrap';
import { ArrowLeft } from 'react-bootstrap-icons';

import { ToastContainer, toast , Bounce} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';



const SignupForm = ({ handleSubmit, handleChange, formData }) => {

  const navigate = useNavigate();
  const { username } = useParams();

  return (
    <div className='container'>
      <div className="header">
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <Button variant="light" onClick={() => navigate(`/dashboard/${username}`)} style={{ border: 'none' }}><ArrowLeft size={36} /></Button>
          <div className="text">Añadir nuevo empleado</div>
        </div>
      </div>
      <div className="underline"></div>

      <form onSubmit={handleSubmit}>
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
    <ToastContainer/>
  </div>
);
}

export default SignupForm;