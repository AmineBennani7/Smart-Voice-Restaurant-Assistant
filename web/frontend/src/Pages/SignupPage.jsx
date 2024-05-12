import React from 'react';
import { Container, Form, Button, Image } from 'react-bootstrap';
import usuario from '../Assets/usuario.png';
import password from '../Assets/password.png';
import correo from '../Assets/correo-electronico.png';
import telefono from '../Assets/ring-phone.png';
import licencia from '../Assets/licencia-de-conducir.png';
import perfil from '../Assets/perfil.png';
import { useNavigate, useParams } from 'react-router-dom'; 
import { ArrowLeft } from 'react-bootstrap-icons'; 
import Footer from '../Components/Utils/footer'; 

const SignupForm = ({ handleSubmit, handleChange, formData }) => {
  const navigate = useNavigate(); 
  const { username } = useParams();

  const handleBack = () => {
    navigate(`/dashboard/${username}`);
  };

  return (
    <div className="d-flex flex-column min-vh-100">
      <Container className="flex-grow-1 d-flex justify-content-center align-items-center">
        <div className="position-relative bg-white rounded-5 text-secondary p-5" style={{ width: '35rem', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
          <Button
            variant="light"
            onClick={handleBack}
            className="position-absolute top-0 start-0 m-3"
            style={{ zIndex: 1 }}
          >
            <ArrowLeft size={20} />
          </Button>

          <div className="text-center mb-4">
            <Image src={perfil} alt="usuario" style={{ height: '6rem' }} />
            <div className="fs-3 fw-bold" style={{ color: 'black' }}>Añadir un nuevo empleado</div>
          </div>

          <Form onSubmit={handleSubmit}>
          <div className="mb-3 d-flex align-items-center">
              <Image src={licencia} alt="nombre" className="me-3" style={{ width: '40px', height: '40px' }} />
              <Form.Control
                type="text"
                placeholder="Nombre"
                name="fullname"
                value={formData.fullname}
                onChange={handleChange}
              />
              {/* Agregar espacio entre Nombre y Apellido */}
              <Form.Control
                type="text"
                placeholder="Apellido"
                name="lastname"
                value={formData.lastname}
                onChange={handleChange}
                className="ms-3"
              />
            </div>
            <div className="mb-3 d-flex align-items-center">
              <Image src={usuario} alt="usuario" className="me-3" style={{ width: '40px', height: '40px' }} />
              <Form.Control
                type="text"
                placeholder="Usuario"
                name="username"
                value={formData.username}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3 d-flex align-items-center">
              <Image src={correo} alt="email" className="me-3" style={{ width: '40px', height: '40px' }} />
              <Form.Control
                type="email"
                placeholder="Email"
                name="email"
                value={formData.email}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3 d-flex align-items-center">
              <Image src={password} alt="password" className="me-3" style={{ width: '40px', height: '40px' }} />
              <Form.Control
                type="password"
                placeholder="Password"
                name="password"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3 d-flex align-items-center">
              <Image src={telefono} alt="telefono" className="me-3" style={{ width: '40px', height: '40px' }} />
              <Form.Control
                type="text"
                placeholder="Número de Teléfono"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
              />
            </div>
            <div className="d-grid">
              <Button variant="primary" type="submit" size="lg">
                Crear cuenta
              </Button>
            </div>
          </Form>
        </div>
      </Container>
      
    </div>
  );
};

export default SignupForm;
