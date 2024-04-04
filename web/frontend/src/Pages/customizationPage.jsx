import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Form, Button, Row, Col, Image, Modal } from 'react-bootstrap';

const PersonalizationImage = () => {
  const [nombreRestaurante, setNombreRestaurante] = useState('');
  const [logoPrincipalSrc, setLogoPrincipalSrc] = useState('');
  const [logoSecundarioSrc, setLogoSecundarioSrc] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    nombreRestauranteModal: '',
    logoPrincipalModal: null,
    logoSecundarioModal: null
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const response = await axios.get('http://localhost:5000/app_customization/primer_oid');
      const data = response.data;

      setNombreRestaurante(data.nombre_restaurante);
      fetchImage(data.logo_principal_oid, setLogoPrincipalSrc);
      fetchImage(data.logo_secundario_oid, setLogoSecundarioSrc);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const fetchImage = async (oid, setImageSrc) => {
    try {
      const response = await axios.get(`http://localhost:5000/app_customization/file/${oid}`, { responseType: 'blob' });
      const reader = new FileReader();
      reader.onloadend = () => {
        setImageSrc(reader.result);
      };
      reader.readAsDataURL(response.data);
    } catch (error) {
      console.error('Error fetching image:', error);
    }
  };

  const handleModalClose = () => setShowModal(false);
  const handleModalShow = () => setShowModal(true);

  const handleInputChange = (event) => {
    const { name, value, files } = event.target;
    setFormData({
      ...formData,
      [name]: files ? files[0] : value
    });
  };

  const handleSaveChanges = async () => {
  try {
    const updatedFormData = new FormData(); // Renombrado formData
    updatedFormData.append('nombre_restaurante', formData.nombreRestauranteModal);
    updatedFormData.append('logo_principal', formData.logoPrincipalModal);
    updatedFormData.append('logo_secundario', formData.logoSecundarioModal);

    const response = await axios.put('http://localhost:5000/app_customization', updatedFormData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });

    if (response.status === 200) {
      fetchData();
      handleModalClose();
    } else {
      console.error('Error al guardar cambios:', response.data.message);
    }
  } catch (error) {
    console.error('Error al guardar cambios:', error);
  }
};

  return (
    <Container>
      <Row className="mb-3 justify-content-center">
        <Col>
          <h2>Personalización de la Aplicación Móvil</h2>
        </Col>
      </Row>

      <Row className="mb-3 justify-content-end">
        <Col>
          <Form.Group controlId="nombreRestaurante">
            <Form.Label><b>Nombre del Restaurante</b></Form.Label>
            <Form.Control type="text" placeholder="Nombre del Restaurante" value={nombreRestaurante} readOnly />
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
          <Button variant="primary" onClick={handleModalShow}>Personalizar estos datos</Button>
        </Col>
      </Row>

      {/* Modal para editar datos */}
      <Modal show={showModal} onHide={handleModalClose}>
        <Modal.Header closeButton>
          <Modal.Title>Editar Datos de Personalización</Modal.Title>
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
    </Container>
  );
};

export default PersonalizationImage;
