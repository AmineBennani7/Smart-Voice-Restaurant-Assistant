import React from 'react';
import { Button, Nav } from 'react-bootstrap';
// bootstrap import no es necesario aquí
import 'bootstrap/dist/css/bootstrap.min.css';
import '../Components/Styles/Dashboard.css';
import  { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Admin from '../Assets/admin.png';
import { ToastContainer, toast , Bounce} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';
import notificationSound from '../Components/Sounds/pending-notification.mp3'; // Importando el sonido
import DashboardPage from '../Pages/dashboardPage';
import useNotification from './Utils/useNotification'


const Dashboard = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [initialTicketCount, setInitialTicketCount] = useState(null);

  
    const handleToggleClick = () => {
      setIsSidebarOpen(!isSidebarOpen);
    }
  
    const navigate = useNavigate();
    const { username } = useParams();
  
    useEffect(() => {
        const authenticatedUsername = localStorage.getItem("username");
        if (authenticatedUsername !== username) {
            navigate('/');
        }
       
    }, [username, navigate]);


    //NOTIFICACIONES 
    const tickets = useNotification();    //funcion useNotification en carpeta utils 


    //PARA DESCONECTAR
    const handleLogout = () => {
        // Borrar los datos de autenticación del almacenamiento local 
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        // Redirigir al usuario a la página de inicio de sesión
        navigate('/');
      }
    

    return (
        <DashboardPage
          isSidebarOpen={isSidebarOpen}
          onToggleClick={handleToggleClick}
          tickets={tickets}
          username={username}
          navigate={navigate}
          handleLogout={handleLogout}
        />
      );
      
    }


    export default Dashboard;