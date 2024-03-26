import React, { useState , useEffect } from 'react';
import { Table, Button } from 'react-bootstrap';
import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft } from 'react-bootstrap-icons'; // Import the left arrow icon from 'react-bootstrap-icons'


const UsuariosInfo = () => {
    const [users, setUsers] = useState([]);
    const navigate = useNavigate();
    const { username } = useParams();

    useEffect(() => {
        const authenticatedUsername = localStorage.getItem("username");
        if (authenticatedUsername !== username) {
            navigate('/');
        }
    }, [username, navigate]);

    useEffect(() => {
        fetch('http://localhost:5000/users')
        .then(response => response.json())
        .then(data => setUsers(data));
    }, []);

   const handleDelete = (userId, userUsername) => {
    const authenticatedUsername = localStorage.getItem("username");

    if (authenticatedUsername === userUsername) {
        alert('No puedes borrar tu propio usuario');
        return;
    }
    
    if (window.confirm('¿Estás seguro que quieres borrar este encargado?')) {
        fetch(`http://localhost:5000/user/${userId}`, {
            method: 'DELETE',
        })
        .then(() => {
            setUsers(users.filter(user => user._id !== userId));
            alert("Usuario borrado con éxito");
        })
        .catch(() => {
            alert('Hubo un error al intentar borrar este encargado');
        });
    }
}

    return (
        <div className="container">
           <div style={{display: 'flex', alignItems: 'center'}}>
                <Button variant="light" onClick={() => navigate(`/dashboard/${username}`)} style={{border: 'none'}}><ArrowLeft size={36} /></Button>
                <h1 className="my-4 ml-4" style={{marginLeft: '2rem'}}>Información de los encargados</h1>
            </div>
            <Table responsive="md">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Apellido</th>
                        <th>Nombre de Usuario</th>
                        <th>Correo Electrónico</th>
                        <th>Número de Teléfono</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map(user => (
                        <tr key={user._id}>
                            <td>{user.fullname}</td>
                            <td>{user.lastname}</td>
                            <td>{user.username}</td>
                            <td>{user.email}</td>
                            <td>{user.phone}</td>
                            <td>
                                <Button variant="danger" onClick={() => handleDelete(user._id, user.username)}>Borrar</Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
}

export default UsuariosInfo;