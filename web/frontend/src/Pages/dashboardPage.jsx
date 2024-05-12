import React from 'react';
import { Button, Nav, Col, Row, Card, ListGroup } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import '../Components/Styles/Dashboard.css';
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import Admin from '../Assets/admin.png';
import { ToastContainer, toast, Bounce } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Footer from '../Components/Utils/footer';
import { Chart } from 'react-google-charts';
import PlatosPie from '../Components/Utils/Stats'




  
  const DashboardPage = ({ isSidebarOpen, handleToggleClick, tickets, navigate, username, handleLogout }) => {
   



  return (
    <body>
   

    <div className="wrapper">
    <link rel="stylesheet" href="https://cdn.lineicons.com/4.0/lineicons.css" />

         <aside id="sidebar" className={isSidebarOpen ? "expand" : ""}>
            <div className="d-flex">
                
                <div className="sidebar-logo">
                    <a href="#">Panel Admin</a>
                </div>
            </div>
            <ul className="sidebar-nav">
            <li className="sidebar-item">
                    <a href="#" className="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#users" aria-expanded="false" aria-controls="users">
                        <i className="lni lni-user"></i>
                        <span>Usuarios</span>
                    </a>
                    <ul id="users" className="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                    <li className="sidebar-item">
                    <a href="#" className="sidebar-link" onClick={() => navigate(`/signup/${username}`)}>
                    Añadir un nuevo encargado
                  </a>
            </li>
                        <li className="sidebar-item">
                        <a href="#" className="sidebar-link" onClick={() => navigate(`/userInfo/${username}`)}>
                           Información de los encargados
                            </a>
                        </li>
                       
                    </ul>
                </li>
                <li className="sidebar-item">
                    <a href="#" className="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#notifications" aria-expanded="false" aria-controls="notifications">
                        <i className="lni lni-agenda"></i>
                        <span>Notificaciones</span>
                    </a>
                    <ul id="notifications" className="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                        <li className="sidebar-item">
                        <a href="#" className="sidebar-link" onClick={() => navigate(`/orders/${username}`)}>
                            Pedidos en curso
                            </a>
                        </li>         
                    </ul>
                </li>
               
                <li className="sidebar-item">
                    <a href="#" className="sidebar-link collapsed has-dropdown" data-bs-toggle="collapse"
                        data-bs-target="#customizations" aria-expanded="false" aria-controls="customizations">
                        <i className="lni lni-protection"></i>
                        <span>Personalizar</span>
                    </a>
                    <ul id="customizations" className="sidebar-dropdown list-unstyled collapse" data-bs-parent="#sidebar">
                        <li className="sidebar-item">
                        <a href="#" className="sidebar-link" onClick={() => navigate(`/menuList/${username}`)}>
                            Personalizar menú
                            </a>
                        </li>
                        <li className="sidebar-item">
                        <a href="#" className="sidebar-link" onClick={() => navigate(`/customizationApp/${username}`)}>
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
        <div className="main p-3 text-center">
           <div className="header" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
             <div className="text">
               Panel de Control
             </div>
            
             <div style={{ display: 'flex', alignItems: 'center' }}>
             <div className='ml-2' style={{fontSize: '15px', color: '#888', fontWeight: 'normal'}}>
                ¡ Hola {username}!
               </div>
             </div>
           </div>
           
        <div className="main p-3">
        <Card className='my-5'>
             <Card.Header className='text-start'><strong>Este es el panel de control diseñado exclusivamente para empleados y administradores del restaurante. En él puedes realizar las siguientes funciones:</strong></Card.Header>
             <Card.Body className="">
                 <ListGroup variant="flush" className="pl-0"> {/* Agregamos la clase 'pl-0' para eliminar el padding a la izquierda */}
                 <ListGroup.Item className=" text-start border-1">Añade y borra empleados</ListGroup.Item> {/* Eliminamos el borde de los elementos ListGroup.Item */}
                 <ListGroup.Item className="text-start border-1">Gestiona los pedidos en curso</ListGroup.Item>
                 <ListGroup.Item className="text-start border-1">Personaliza el menú del restaurante</ListGroup.Item>
                 <ListGroup.Item className=" text-start border-1">Personaliza la app móvil del restaurante</ListGroup.Item>
                 </ListGroup>
             </Card.Body>
    </Card>
    <PlatosPie></PlatosPie>







          </div>
        </div>
       
      </div>
     
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-ENjdO4Dr2bkBIFxQpeoTz1HIcje39Wm4jDKdf19U8gI4ddQ3GYNS7NTKfAdVQSZe"
        crossOrigin="anonymous"></script>
    <script src="script.js"></script>
    <ToastContainer />
</body>
   
  );
};

export default DashboardPage;