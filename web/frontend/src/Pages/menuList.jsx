import React, { useState , useEffect } from 'react';
import { Table, Button, Modal, Form, Tooltip, OverlayTrigger } from 'react-bootstrap';
import { useNavigate , useParams } from 'react-router-dom';
import { ArrowLeft } from 'react-bootstrap-icons'; 

const MenuList = () => {
    
    const [platos, setPlatos] = useState([]); //Almacena la lista de platos
    const [show, setShow] = useState(false); //Controla la visibilidad del modal para añadir nuevos platos
    const [nuevoPlato, setNuevoPlato] = useState({ nombre: '', descripcion: '', categoria: '', variaciones: [] }); //almacena los detalles del uevo plato

    //Es dereact-router-dmm para obtener el parametro del URL de username 
    const navigate = useNavigate();
    const { username } = useParams();


    const handleClose = () => setShow(false);


//CONTROLADOR para agregar un nuevo plato
const handleAdd = (e) => {
    e.preventDefault();
    fetch(`http://localhost:5000/platos`, {   //Va a la API de platos y realiza post
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(nuevoPlato) //convierte el objeto nuevoPlato a formato JSON
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.message);
            });
        }
        return response;
    })
    .then(() => {  //Si todo es correcto, rienici el estado de nuevoPLato a vacio y nos reinicia la pagina con el nuevo plato añadido
        setShow(false);
        setNuevoPlato({ nombre: '', descripcion: '', categoria: '', variaciones: [] });
        window.location.reload();
    })
    .catch((error) => {
        alert(error.message);
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
        const authenticatedUsername = localStorage.getItem("username");
        if (authenticatedUsername !== username) {
            navigate('/');
        }
    }, [username, navigate]);

    useEffect(() => {
        fetch('http://localhost:5000/platos')
        .then(response => response.json())
        .then(data => setPlatos(data));
    }, []);

    const handleShow = () => {
        // Reset plate and variations when the modal opens
        setNuevoPlato({nombre: '', descripcion: '', categoria: '', variaciones: [{tipo:'', precio:''}]});
        setShow(true);
    }


    const handleVariationChange = (index, field, value) => {
        let newVariations = [...nuevoPlato.variaciones];
        newVariations[index][field] = value;
    
        setNuevoPlato(prevState => { 
            return {...prevState, variaciones: newVariations} 
        });
    };
            
    const addNewVariation = () => {
        setNuevoPlato(prevState => { 
            return {...prevState, variaciones: [...prevState.variaciones, {tipo: '', precio: ''}]} 
        });
    };

    
    return (
        <div className="container" style={{ marginTop: '2em', marginBottom: '2em' }}>
             <div style={{display: 'flex', alignItems: 'center'}}>
                <Button variant="light" onClick={() => navigate(`/dashboard/${username}`)} style={{border: 'none'}}><ArrowLeft size={36} /></Button>
                <h1 className="my-4 ml-4" style={{marginLeft: '2rem'}}>Lista de platos disponibles</h1>
            </div>
            
            
            <Button variant="primary" onClick={handleShow} style={{ marginBottom: '1em' }}>
                Añadir nuevo plato
            </Button>
    
            <Modal show={show} onHide={handleClose}>
                <Modal.Header closeButton>
                    <Modal.Title>Añadir nuevo plato</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <Form onSubmit={handleAdd}>
                        <Form.Group controlId="nombre">
                            <Form.Label>Nombre del plato</Form.Label>
                            <Form.Control type="text" placeholder="Dish Name" value={nuevoPlato.nombre} onChange={e => setNuevoPlato(prevState => { return { ...prevState, nombre: e.target.value } })} />
                        </Form.Group>
    
                        <Form.Group controlId="descripcion">
                            <Form.Label>Descripción</Form.Label>
                            <Form.Control type="text" placeholder="Description" value={nuevoPlato.descripcion} onChange={e => setNuevoPlato(prevState => { return { ...prevState, descripcion: e.target.value } })} />
                        </Form.Group>
    
                        <Form.Group controlId="categoria">
                            <Form.Label>Categoría</Form.Label>
                            <Form.Control type="text" placeholder="Category" value={nuevoPlato.categoria} onChange={e => setNuevoPlato(prevState => { return { ...prevState, categoria: e.target.value } })} />
                        </Form.Group>
    
                        <div style={{ fontWeight: 'bold', marginBottom: '1em', textAlign: 'center' }}>
                            Variations
                            <hr style={{ borderTop: '3px solid black', width: '70%', margin: 'auto' }} />
                        </div>
    
                        {nuevoPlato.variaciones && nuevoPlato.variaciones.map((variation, index) => (
                            <div key={index}>
                                <Form.Group controlId={`variaciones-${index}-variacion`}>
                                    <Form.Label>Tipo de variación</Form.Label>
                                    <Form.Control type="text" placeholder="Type" value={variation.variacion} onChange={e => handleVariationChange(index, 'variacion', e.target.value)} />
                                </Form.Group>
                                <Form.Group controlId={`variaciones-${index}-precio`}>
                                    <Form.Label>Precio de la variación</Form.Label>
                                    <Form.Control type="number" placeholder="Price" value={variation.precio} onChange={e => handleVariationChange(index, 'precio', e.target.value)} />
                                </Form.Group>
                                {/* Línea horizontal */}
                                {index !== nuevoPlato.variaciones.length - 1 && <hr style={{ borderTop: '2px solid black', marginBottom: '1em' }} />}
                            </div>
                        ))}
                        {/* Botón para agregar nueva variación */}
                        <div className="d-flex justify-content-between align-items-center" style={{ marginTop: '1em' }}>
                            <span>
                                <Button variant="primary" onClick={addNewVariation}>Añadir nueva variación</Button>
                                <OverlayTrigger placement="right" overlay={<Tooltip>Pulse en este botón para añadir nuevas variaciones.</Tooltip>}>
                                    <Button variant="info" style={{ marginLeft: '1em' }}>?</Button>
                                </OverlayTrigger>
                            </span>
                            <Button variant="primary" type="submit">Confirmar</Button>
                        </div>
                    </Form>
                </Modal.Body>
            </Modal>
    
            <Table responsive="md">
                <thead>
                    <tr>
                        <th>Nombre</th>
                        <th>Descripción</th>
                        <th>Categoría</th>
                        <th>Variaciones</th>
                        <th>Acción</th>
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
                                <Button variant="danger" onClick={() => handleDelete(plato._id)}>Borrar</Button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </Table>
        </div>
    );
                                }       

export default MenuList;