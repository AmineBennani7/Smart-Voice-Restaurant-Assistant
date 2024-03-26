import React, { useState , useEffect } from 'react';
import SignupForm from '../Pages/SignupPage'; // Importando el nuevo componente
import '../Components/Styles/LoginSignup.css';
import { validateFormData, validateEmail, phoneNumberPattern } from './validators/signupValidator';
import { useNavigate, useParams } from 'react-router-dom';




const Signup = () => {
    const [formData, setFormData] = useState({
      fullname: '',
      lastname: '',
      username: '',
      email: '',
      password: '',
      phoneNumber: ''
    });

    const navigate = useNavigate();
    const { username } = useParams(); // get the username from the url
  
    useEffect(() => {
      // The token can be whatever identifier you're using for authentication
      const token = localStorage.getItem("token");
      const authenticatedUsername = localStorage.getItem("username");
      
      if (!token || authenticatedUsername !== username) {
        navigate("/login");
      }
    }, [username, navigate]);

  
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
        if (response.ok) { // Comprueba si el status de la respuesta es 200
          const authenticatedUsername = localStorage.getItem("username"); // usuario actual conectado
          alert('Usuario creado con éxito!')
          // Redirige al usuario al dashboard de la cuenta administradora
          navigate(`/dashboard/${authenticatedUsername}`);
        }
        else {
          alert(data.message); //Muestra un alert con el error
        }
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


    
    