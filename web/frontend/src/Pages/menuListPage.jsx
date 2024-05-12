import React, { useState , useEffect } from 'react';
import { Table, Button, Modal, Form, Tooltip, OverlayTrigger } from 'react-bootstrap';
import { useNavigate , useParams } from 'react-router-dom';
import { ArrowLeft } from 'react-bootstrap-icons'; 
import { ToastContainer, toast , Bounce} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Footer from '../Components/Utils/footer';


    
const MenuListForm = ({ platos, show, handleClose, handleShow, handleAdd, nuevoPlato, setNuevoPlato, handleVariationChange, addNewVariation, handleDelete, handleShowEditModal, showEditModal, editPlato,setEditPlato, handleCloseEditModal,handleEdit,username,navigate,ticket }) => (

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
                                    <Form.Control type="number" placeholder="Price" min="0" step="any"  value={variation.precio} onChange={e => handleVariationChange(index, 'precio', e.target.value)} />
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
            <Modal show={showEditModal} onHide={handleCloseEditModal}>
    <Modal.Header closeButton>
        <Modal.Title>Editar Plato</Modal.Title>
    </Modal.Header>
    <Modal.Body>
        {/* Formulario para editar el plato */}
        {editPlato && (
            <Form onSubmit={handleEdit}>
                <Form.Group controlId="nombre">
                    <Form.Label>Nombre del plato</Form.Label>
                    <Form.Control type="text" placeholder="Dish name" value={editPlato.nombre} onChange={e => setEditPlato(prevState => ({ ...prevState, nombre: e.target.value }))} />
                </Form.Group>
                <Form.Group controlId="descripcion">
                    <Form.Label>Descripción</Form.Label>
                    <Form.Control type="text" placeholder="Description" value={editPlato.descripcion} onChange={e => setEditPlato(prevState => ({ ...prevState, descripcion: e.target.value }))} />
                </Form.Group>
                <Form.Group controlId="categoria">
                    <Form.Label>Categoría</Form.Label>
                    <Form.Control type="text" placeholder="Category" value={editPlato.categoria} onChange={e => setEditPlato(prevState => ({ ...prevState, categoria: e.target.value }))} />
                </Form.Group>
                <div style={{ fontWeight: 'bold', marginBottom: '1em', textAlign: 'center' }}>
                    Variaciones
                    <hr style={{ borderTop: '3px solid black', width: '70%', margin: 'auto' }} />
                </div>
                {editPlato.variaciones && editPlato.variaciones.map((variation, index) => (
                    <div key={index}>
                        <Form.Group controlId={`variaciones-${index}-variacion`}>
                            <Form.Label>Tipo de variación</Form.Label>
                            <Form.Control type="text" placeholder="Type" value={variation.variacion} onChange={e => handleVariationChange(index, 'variacion', e.target.value)} />
                        </Form.Group>
                        <Form.Group controlId={`variaciones-${index}-precio`}>
                            <Form.Label>Precio de la variación</Form.Label>
                            <Form.Control type="number" placeholder="Price" min="0" step="any" value={variation.precio} onChange={e => handleVariationChange(index, 'precio', e.target.value)} />
                        </Form.Group>
                        {/* Línea horizontal */}
                        {index !== editPlato.variaciones.length - 1 && <hr style={{ borderTop: '2px solid black', marginBottom: '1em' }} />}
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
        )}
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
            <div style={{ display: 'flex', justifyContent: 'space-between', width: '150px' }}>
                <Button variant="danger" onClick={() => handleDelete(plato._id)}>Borrar</Button>
                <Button variant="primary" onClick={() => handleShowEditModal(plato)}>Editar</Button>
            </div>
</td>
                        </tr>
                    ))}
                </tbody>
            </Table>
            <ToastContainer />
        </div>
        
    );
                                     

export default MenuListForm;