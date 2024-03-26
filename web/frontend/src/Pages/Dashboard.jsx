import React from 'react';
import { Button, Nav } from 'react-bootstrap';
// bootstrap import no es necesario aquí
import 'bootstrap/dist/css/bootstrap.min.css';
import '../Components/Styles/Dashboard.css';
import  { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Admin from '../Assets/admin.png';


const Dashboard = () => {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  
    const handleToggleClick = () => {
      setIsSidebarOpen(!isSidebarOpen);
    }
  
    const navigate = useNavigate();
    const { username } = useParams();
  
    useEffect(() => {
      const authenticatedUsername = localStorage.getItem("username");
      if(authenticatedUsername !== username) {
        navigate('/');
      }
    }, [username,navigate]);

    //PARA DESCONECTAR
    const handleLogout = () => {
        // Borrar los datos de autenticación del almacenamiento local 
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        // Redirigir al usuario a la página de inicio de sesión
        navigate('/');
      }
  



  return (
    <body>
    <div class="wrapper">
    <link rel="stylesheet" href="https://cdn.lineicons.com/4.0/lineicons.css" />

         <aside id="sidebar" className={isSidebarOpen ? "expand" : ""}>
            <div class="d-flex">
                <button class="toggle-btn"  type="button" onClick={handleToggleClick}>
                    <i class="lni lni-grid-alt"></i>
                </button>
                <div class="sidebar-logo">
                    <a href="#">Panel Admin</a>
                </div>
            </div>
            <ul class="sidebar-nav">
            <li class="sidebar-item">
                    <a href="#" class="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#auth" aria-expanded="false" aria-controls="auth">
                        <i class="lni lni-user"></i>
                        <span>Usuarios</span>
                    </a>
                    <ul id="auth" class="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                    <li class="sidebar-item">
                    <a href="#" class="sidebar-link" onClick={() => navigate(`/signup/${username}`)}>
                    Añadir un nuevo encargado
                  </a>
            </li>
                        <li class="sidebar-item">
                        <a href="#" class="sidebar-link" onClick={() => navigate(`/userInfo/${username}`)}>
                            <a href="#" class="sidebar-link">Borrar un encargado</a>
                            </a>
                        </li>
                       
                    </ul>
                </li>
                <li class="sidebar-item">
                    <a href="#" class="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#auth" aria-expanded="false" aria-controls="auth">
                        <i class="lni lni-agenda"></i>
                        <span>Notificaciones</span>
                    </a>
                    <ul id="auth" class="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                        <li class="sidebar-item">
                            <a href="#" class="sidebar-link">Notificaciones cocina</a>
                        </li>
                      
                    </ul>
                </li>
               
           
                
               
                <li class="sidebar-item">
                    <a href="#" class="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#auth" aria-expanded="false" aria-controls="auth">
                        <i class="lni lni-protection"></i>
                        <span>Personalizar</span>
                    </a>
                    <ul id="auth" class="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                        <li class="sidebar-item">
                            <a href="#" class="sidebar-link">Personalizar menú</a>
                        </li>
                        <li class="sidebar-item">
                            <a href="#" class="sidebar-link">Personalizar app móvil</a>
                        </li>
                    </ul>
                </li>
               
            </ul>
            <div className="sidebar-footer">
            <a href="#" className="sidebar-link" onClick={handleLogout}>
                <i className="lni lni-exit"></i>
                <span>Cerrar sesión</span>
            </a>
        </div>
        </aside>
        <div className="main p-3">
    <div className="text-center">
        
        <h1 className="mt-5">Bienvenido {username} </h1>
        <img src={Admin} style={{width: '150px', height: 'auto'}} alt="Cocinero" />
    </div>
</div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe"
        crossorigin="anonymous"></script>
    <script src="script.js"></script>
</body>
   
  );
};

export default Dashboard;
