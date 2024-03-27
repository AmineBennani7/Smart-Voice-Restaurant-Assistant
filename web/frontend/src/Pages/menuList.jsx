import React, { useState , useEffect } from 'react';
import { Table, Button, Modal, Form } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';

const MenuList = () => {
    
    const [platos, setPlatos] = useState([]);
    const [show, setShow] = useState(false); //state to handle modal display
    const [nuevoPlato, setNuevoPlato] = useState({ nombre: '', descripcion: '', categoria: '', variaciones: [] });
    const navigate = useNavigate();

    const handleClose = () => setShow(false);
    const handleShow = () => setShow(true);

    const handleAdd = (e) => {
        e.preventDefault();
        fetch(`http://localhost:5000/platos`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(nuevoPlato)
        })
        .then(() => {
            setShow(false);
            setNuevoPlato({ nombre: '', descripcion: '', categoria: '', variaciones: [] });
            window.location.reload();
        })
        .catch(() => {
            alert('Hubo un error al intentar añadir este plato');
        });
    }

   

    const handleDelete = (idPlato) => {    
        if (window.confirm('¿Estás seguro que quieres borrar este plato?')) {
            fetch(`http://localhost:5000/platos/${idPlato}`, {
                method: 'DELETE',
            })
            .then(() => {
                setPlatos(platos.filter(plato => plato._id !== idPlato));
                alert("Plato borrado con éxito");
            })
            .catch(() => {
                alert('Hubo un error al intentar borrar este plato');
            });
        }
    }
    useEffect(() => {
        fetch('http://localhost:5000/platos')
        .then(response => response.json())
        .then(data => setPlatos(data));
    }, []);

    return (
        <div className="container">
            <h1 className="my-4" style={{marginLeft: '2rem'}}>Información de los Platos</h1>
           
            <Button variant="primary" onClick={handleShow}>
                Add Dish
            </Button>

            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Add Dish</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleAdd}>
                        <Form.Group controlId="nombre">
                            <Form.Label>Name</Form.Label>
                            <Form.Control type="text" placeholder="Dish Name" value={nuevoPlato.nombre} onChange={e => setNuevoPlato(prevState => { return {...prevState, nombre: e.target.value} })}/>
                        </Form.Group>

                        <Form.Group controlId="descripcion">
                            <Form.Label>Description</Form.Label>
                            <Form.Control type="text" placeholder="Description" value={nuevoPlato.descripcion} onChange={e => setNuevoPlato(prevState => { return {...prevState, descripcion: e.target.value} })}/>
                        </Form.Group>

                        <Form.Group controlId="categoria">
                            <Form.Label>Category</Form.Label>
                            <Form.Control type="text" placeholder="Category" value={nuevoPlato.categoria} onChange={e => setNuevoPlato(prevState => { return {...prevState, categoria: e.target.value} })}/>
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            Submit
                        </Button>
                    </Form>
                </Modal.Body>
            </Modal>

            <Table responsive="md">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Description</th>
                        <th>Category</th>
                        <th>Variations</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {platos.map(plato => (
                        <tr key={plato._id}>
                            <td>{plato.nombre}</td>
                            <td>{plato.descripcion}</td>
                            <td>{plato.categoria}</td>
                            <td>
                                {plato.variaciones.map((variacion, index) => (
                                    <p key={index}>{variacion.variacion}: {variacion.precio}€</p>
                                ))}
                            </td>
                            <td>
                                <Button variant="danger" onClick={() => handleDelete(plato._id)}>Delete</Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>

        </div>
    );
}

export default MenuList;