import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Container, Form, Button, Row, Col, Image, Modal } from 'react-bootstrap';
import { OverlayTrigger, Tooltip } from 'react-bootstrap';
import CustomizationForm from '../Pages/customizationPage';
import { useNavigate, useParams } from 'react-router-dom';





const Customization = () => {
  const [nombreRestaurante, setNombreRestaurante] = useState('');
  const [logoPrincipalSrc, setLogoPrincipalSrc] = useState('');
  const [logoSecundarioSrc, setLogoSecundarioSrc] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    nombreRestauranteModal: '',
    logoPrincipalModal: null,
    logoSecundarioModal: null
  });



  const navigate = useNavigate();
  const { username } = useParams();

  //Al conectarme a esta página, veo si mi username== username del parametro del link, si no lo es me saca de esta página 
  useEffect(() => {
    const authenticatedUsername = localStorage.getItem("username"); 
    if (authenticatedUsername === null) {  
      navigate('/');
    }
  }, [username, navigate]);


  useEffect(() => {
    fetchData();
  }, []);

  //Primero sacamos el primer id de la tabla, que contendrá nombre del establecimiento, y las 2 imagenes 
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

  //a partir de id de una imagen, la devuelve a formato png 
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

  //Actualizar el modal 
  const handleSaveChanges = async () => {
  try {
    const updatedFormData = new FormData(); // 
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
  <CustomizationForm
    nombreRestaurante={nombreRestaurante}
    logoPrincipalSrc={logoPrincipalSrc}
    logoSecundarioSrc={logoSecundarioSrc}
    showModal={showModal}
    handleModalShow={handleModalShow}
    handleModalClose={handleModalClose}
    handleInputChange={handleInputChange}
    handleSaveChanges={handleSaveChanges}
  />
);

}


export default Customization;