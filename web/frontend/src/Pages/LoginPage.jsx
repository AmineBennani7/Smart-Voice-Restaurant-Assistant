import React from 'react';
import { Container, Form, Button, Image } from 'react-bootstrap';
import password from '../Assets/password.png';
import usuario from '../Assets/usuario.png';
import Admin2 from '../Assets/admin.png';
import Footer from '../Components/Utils/footer'; // 

const LoginForm = ({ handleChange, handleSubmit, formData }) => {
  return (
    <div className="d-flex flex-column min-vh-100"> {/* Establece una estructura de columna flexible para el contenido */}
      <Container className="flex-grow-1 d-flex justify-content-center align-items-center"> {/* Contenedor principal */}
        <div className="bg-white rounded-5 text-secondary p-5" style={{ width: '35rem', boxShadow: '0 4px 8px rgba(0,0,0,0.1)' }}>
          <div className="text-center mb-4">
            <Image src={Admin2} alt="admin" style={{ height: '6rem' }} />
            <div className="fs-3 fw-bold" style={{ color: 'black' }}>Iniciar sesión</div>
          </div>
          <Form onSubmit={handleSubmit}>
            <div className="mb-3 d-flex align-items-center">
              <Image src={usuario} alt="username" className="me-3" style={{ width: '40px', height: '40px' }} />
              <Form.Control
                type="text"
                placeholder="Nombre de usuario"
                name="username"
                size="lg"
                value={formData.username}
                onChange={handleChange}
              />
            </div>
            <div className="mb-3 d-flex align-items-center">
              <Image src={password} alt="password" className="me-3" style={{ width: '40px', height: '40px' }} />
              <Form.Control
                type="password"
                placeholder="Contraseña"
                name="password"
                size="lg"
                value={formData.password}
                onChange={handleChange}
              />
            </div>
            <div className="d-grid">
              <Button variant="primary" type="submit" size="lg">
                Iniciar sesión
              </Button>
            </div>
          </Form>
        </div>
      </Container>
      
      <Footer />
    </div>
  );
};

export default LoginForm;
