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


const Dashboard = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [tickets, setTickets] = useState([]);
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
        fetchTickets();
    }, [username, navigate]);


    //NOTIFICACIONES 
    const fetchTickets = async () => {
    try {
        const response = await axios.get('http://localhost:5000/pedidos');
        setTickets(oldTickets => {
            if (oldTickets.length === 0) { //Al principio cuando se carga la página, no aparece ninguna notificación 
                return response.data;
            }
            if (response.data.length !== oldTickets.length) {
                let audio = new Audio(notificationSound);
                audio.play();
                toast.success('¡Un nuevo pedido ha sido creado!', {
                    position: "top-left",
                    autoClose: 5000,
                    closeOnClick: true,                    
                    hideProgressBar: false,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                    transition: Bounce
                });
                return response.data;
            }
            return oldTickets;
        });
    } catch (err) {
        console.error(err);
    }
};
    
    useEffect(() => {
        fetchTickets();
        const interval = setInterval(fetchTickets, 5000); //Notificación dura 5sec en la pantalla 
        return () => clearInterval(interval);
    }, []);

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