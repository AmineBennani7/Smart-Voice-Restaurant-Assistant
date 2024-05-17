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
import notificationSound from '../Components/Sounds/pending-notification.mp3'; // Importando el sonido
import DashboardPage from '../Pages/dashboardPage';
import useNotification from './Utils/useNotification'
import { Bar } from 'react-chartjs-2'; // Importa el componente de gráfico que deseas utilizar
import axios from 'axios';



const Dashboard = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const [initialTicketCount, setInitialTicketCount] = useState(null);
    const [showChangePasswordModal, setShowChangePasswordModal] = useState(false);
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    
    //MODIFICAR PASSWORD
    const handlePasswordChange = async (event) => {
        event.preventDefault();
    
        try {
            const token = localStorage.getItem("token"); // token del almacenamiento local
    
            const response = await axios.put(
                `http://localhost:5000/change_password/${username}`,
                {
                    current_password: oldPassword,
                    new_password: newPassword
                },
                {
                    headers: {
                        'Authorization': `Bearer ${token}`, // Incluye el token en los encabezados
                        'Content-Type': 'application/json'
                    }
                }
            );
    
            if (response.status === 200) {
                toast.success('Contraseña actualizada correctamente');
            } else {
                if (response.status === 401) {
                    toast.error('La contraseña actual es incorrecta');
                } else {
                    toast.error(response.data.message || 'Error al cambiar la contraseña');
                }
            }
        } catch (error) {
            // 
            toast.error('La contraseña actual es incorrecta');
        }
    };
    

  
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

      //chart por defecto, se cambia abajo
      const chartData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [
            {
                label: 'Tickets',
                backgroundColor: 'rgba(75,192,192,1)',
                borderColor: 'rgba(0,0,0,1)',
                borderWidth: 1,
                data: [65, 59, 80, 81, 56, 55]
            }
        ]
      };
    


return (

  <DashboardPage
      isSidebarOpen={isSidebarOpen}
      onToggleClick={() => setIsSidebarOpen(!isSidebarOpen)}
      tickets={tickets}
      username={username}
      navigate={navigate}
      handleLogout={handleLogout}
      showChangePasswordModal={showChangePasswordModal}
      setShowChangePasswordModal={setShowChangePasswordModal}
      handlePasswordChange={handlePasswordChange}
      oldPassword={oldPassword}
      setOldPassword={setOldPassword}
      newPassword={newPassword}
      setNewPassword={setNewPassword}
  >
      {}
      <div className="chart-container">
          <h2>Monthly Ticket Overview</h2>
          <Bar
              data={chartData}
              options={{
                  title: {
                      display: true,
                      text: 'Ticket Overview',
                      fontSize: 20
                  },
                  legend: {
                      display: true,
                      position: 'right'
                  }
              }}
          />
      </div>
  </DashboardPage>
);

}

export default Dashboard;