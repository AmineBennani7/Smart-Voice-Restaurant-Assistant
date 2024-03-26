import React, { useState } from 'react';
import SignupForm from '../Pages/SignupPage'; // Importando el nuevo componente
import '../Components/Styles/LoginSignup.css';
import { validateFormData, validateEmail, phoneNumberPattern } from './validators/signupValidator';




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
        <SignupForm handleChange={handleChange} handleSubmit={handleSubmit} formData={formData} />
      );
    }
    
    export default Signup;

    