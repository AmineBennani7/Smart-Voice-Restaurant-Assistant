import React from 'react';
import { Button, Table } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';
import axios from 'axios';
import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import OrderList from '../Pages/OrderPage';

import useNotification from './Utils/useNotification'




const Ordering = () => {
    const [pedidos, setPedidos] = useState([]);

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
  axios.get('http://localhost:5000/pedidos')
    .then(response => {
        const responseData = JSON.parse(response.data);
        console.log(JSON.stringify(responseData, null, 2));
        setPedidos(responseData);
    })
    .catch(error => {
        console.error('Error', error);
    });
}, []);


    const handleDelete = (id) => {
        axios.delete(`http://localhost:5000/pedidos/${id}`)
            .then(response => {
                setPedidos(pedidos.filter(pedido => pedido._id.$oid !== id));
            })
            .catch(error => {
                console.error('Error', error);
            });
    };
    const tickets = useNotification();    //funcion useNotification en carpeta utils 

  
  
    return (
        <OrderList
        pedidos={pedidos}
          onDelete={handleDelete}
          username={username}
          navigate={navigate}
          tickets={tickets}
        />
    );
  
  }
  
  
  export default Ordering;

