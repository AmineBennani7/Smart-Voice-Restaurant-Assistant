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








const dashboardPage = ({ isSidebarOpen, handleToggleClick,tickets, navigate, username,handleLogout }) => {

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
                        data-bs-target="#users" aria-expanded="false" aria-controls="users">
                        <i class="lni lni-user"></i>
                        <span>Usuarios</span>
                    </a>
                    <ul id="users" class="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                    <li class="sidebar-item">
                    <a href="#" class="sidebar-link" onClick={() => navigate(`/signup/${username}`)}>
                    Añadir un nuevo encargado
                  </a>
            </li>
                        <li class="sidebar-item">
                        <a href="#" class="sidebar-link" onClick={() => navigate(`/userInfo/${username}`)}>
                           Información de los encargados
                            </a>
                        </li>
                       
                    </ul>
                </li>
                <li class="sidebar-item">
                    <a href="#" class="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#notifications" aria-expanded="false" aria-controls="notifications">
                        <i class="lni lni-agenda"></i>
                        <span>Notificaciones</span>
                    </a>
                    <ul id="notifications" class="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                        <li class="sidebar-item">
                        <a href="#" class="sidebar-link" onClick={() => navigate(`/orders/${username}`)}>
                            Notificaciones cocina
                            </a>


                        </li>

                      
                    </ul>
                </li>
               
                <li class="sidebar-item">
                    <a href="#" class="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#customizations" aria-expanded="false" aria-controls="customizations">
                        <i class="lni lni-protection"></i>
                        <span>Personalizar</span>
                    </a>
                    <ul id="customizations" class="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                        <li class="sidebar-item">
                        <a href="#" class="sidebar-link" onClick={() => navigate(`/menuList/${username}`)}>
                            Personalizar menú
                            </a>
                        </li>
                        <li class="sidebar-item">
                        <a href="#" class="sidebar-link" onClick={() => navigate(`/customizationApp/${username}`)}>
                           Personalizar app móvil</a>
                            
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
    <div className="header">
        <div className="text">Bienvenido {username}</div>
        <div className="h6">
        <strong>Este es el panel de control donde se podrá añadir nuevos empleados, ver nuevos pedidos de los clientes o modificar la app móvil y el menú</strong>
        </div>     
     </div>
    

        
        <img src={Admin} style={{width: '300px', height: 'auto',  marginTop: '60px'}} alt="Cocinero" />
    </div>
</div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe"
        crossorigin="anonymous"></script>
    <script src="script.js"></script>
    <ToastContainer />
</body>
   
  );
};

export default dashboardPage;
