import React, { useState, useEffect } from 'react';

import { Container, Form, Button, Row, Col, Image, Modal } from 'react-bootstrap';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import { ArrowLeft } from 'react-bootstrap-icons'; 
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast , Bounce} from 'react-toastify';


const Customization = ({
  handleInputChange,
  handleModalClose,
  handleModalShow,
  handleSaveChanges,
  logoPrincipalSrc,
  logoSecundarioSrc,
  nombreRestaurante,
  showModal,username,navigate,ticket
}) => {
  return (
    <Container>
<div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px' }}>
        <Button 
            variant="light" 
            onClick={() => navigate(`/dashboard/${username}`)} 
            style={{border: 'none'}}>
            <ArrowLeft size={36} />
        </Button>
        <div className="text">Personalización de la Aplicación Móvil</div>
     
    </div>


      <Row className="mb-3 justify-content-end">
        <Col>
          <Form.Group controlId="nombreRestaurante">
            <Form.Label><b>Nombre del Establecimiento</b></Form.Label>
            <Form.Control type="text" placeholder="Nombre del establecimiento" value={nombreRestaurante} readOnly />
          </Form.Group>
        </Col>
      </Row>

      <Row className="mb-3 justify-content-end">
        <Col>
          <Form.Group controlId="logoPrincipal">
            <Form.Label><b>Logo Principal</b></Form.Label>
          </Form.Group>
        </Col>
      </Row>

      <Row className="mb-3 justify-content-end">
        <Col>
          <Image src={logoPrincipalSrc} alt="Logo Principal" thumbnail style={{ maxWidth: '100px' }} />
        </Col>
      </Row>

      <Row className="mb-3 justify-content-end">
        <Col>
          <Form.Group controlId="logoSecundario">
            <Form.Label><b>Logo Secundario</b></Form.Label>
          </Form.Group>
        </Col>
      </Row>

      <Row className="mb-3 justify-content-end">
        <Col>
          <Image src={logoSecundarioSrc} alt="Logo Secundario" thumbnail style={{ maxWidth: '100px' }} />
        </Col>
      </Row>

      {/* Botón para abrir el modal */}
      <Row className="mb-3 justify-content-center">
        <Col>
          <Button variant="primary" onClick={handleModalShow}>Personalizar elementos</Button>
        </Col>
      </Row>

      {/* Modal para editar datos */}
      <Modal show={showModal} onHide={handleModalClose}>
      <Modal.Header closeButton>
  <Modal.Title>
    Editar Datos de Personalización
    
    <OverlayTrigger
      placement="right"
      overlay={
        <Tooltip>
          No es necesario rellenar todos los campos
        </Tooltip>
      }
    >
      <Button variant="info" style={{ padding: "0 5px", marginLeft: "10px" }}>?</Button>
    </OverlayTrigger>
  </Modal.Title>
</Modal.Header>
        <Modal.Body>
          {/* Formulario para editar datos */}
          <Form>
            <Form.Group controlId="nombreRestauranteModal">
              <Form.Label>Nombre del Restaurante</Form.Label>
              <Form.Control type="text" placeholder="Nombre del Restaurante" name="nombreRestauranteModal" onChange={handleInputChange} />
            </Form.Group>
            <Form.Group controlId="logoPrincipalModal">
              <Form.Label>Logo Principal</Form.Label>
              <Form.Control type="file" name="logoPrincipalModal" onChange={handleInputChange} accept="image/*" />
            </Form.Group>
            <Form.Group controlId="logoSecundarioModal">
              <Form.Label>Logo Secundario</Form.Label>
              <Form.Control type="file" name="logoSecundarioModal" onChange={handleInputChange} accept="image/*" />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleModalClose}>Cerrar</Button>
          <Button variant="primary" onClick={handleSaveChanges}>Guardar Cambios</Button>
        </Modal.Footer>
      </Modal>
      <ToastContainer />
    </Container>
    
  );
    }

export default Customization;
