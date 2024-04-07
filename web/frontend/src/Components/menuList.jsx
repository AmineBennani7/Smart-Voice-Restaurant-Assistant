import React, { useState , useEffect } from 'react';
import { Table, Button, Modal, Form, Tooltip, OverlayTrigger } from 'react-bootstrap';
import { useNavigate , useParams } from 'react-router-dom';
import MenuListForm from '../Pages/menuListPage';




const MenuList = () => {
    
    const [platos, setPlatos] = useState([]); //Almacena la lista de platos
    const [show, setShow] = useState(false); //Controla la visibilidad del modal para añadir nuevos platos
    const [nuevoPlato, setNuevoPlato] = useState({ nombre: '', descripcion: '', categoria: '', variaciones: [] }); //almacena los detalles del uevo plato

    
    const [showEditModal, setShowEditModal] = useState(false); // Nuevo estado para el modal de edición
    const [editPlato, setEditPlato] = useState(null); // Nuevo estado para almacenar el plato seleccionado para la edición

    //Es dereact-router-dmm para obtener el parametro del URL de username 
    const navigate = useNavigate();
    const { username } = useParams();


    const handleClose = () => setShow(false);



//Al conectarme a esta página, veo si mi username== username del parametro del link, si no lo es me saca de esta página 
    useEffect(() => {
        const authenticatedUsername = localStorage.getItem("username"); //saco el username con el que estoy conectado
        if (authenticatedUsername !== username) {  //si ese username != username del parametro entnoces me saca de la pagina
            navigate('/');
        }
    }, [username, navigate]);


   // cargar la lista de platos cuando el componente se monta por primera vez. 
    useEffect(() => {
        fetch('http://localhost:5000/platos')
        .then(response => response.json())
        .then(data => setPlatos(data));
    }, []);    

//-------------------------------------------------------------------------------------------//
//1. EDITAR UN PLATO
     // Función para abrir el modal de edición
     const handleShowEditModal = (plato) => { // parametro plato:
        setEditPlato(plato); //usa useState para actualizar estado en los nuevos valores del plato
        setShowEditModal(true); //muestra la modal de editar 
    };
    // Función para cerrar el modal de edición
    const handleCloseEditModal = () => {
        setShowEditModal(false);
        setEditPlato(null);
    };

    const handleEdit = (e) => {
        e.preventDefault();
        fetch(`http://localhost:5000/platos/${editPlato._id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(editPlato) // Envía el plato editado al servidor
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message);
                });
            }
            return response;
        })
        .then(() => {
            handleCloseEditModal(); // Cierra el modal después de la edición exitosa
            window.location.reload();

        })
        .catch(error => {
            alert('Hubo un error al intentar editar el plato: ' + error.message);
        });
    };


//-------------------------------------------------------------------------------------------//
//2. AGREGAR UN NUEVO PLATO: 

//Resetea los platos y variaciones cuando abrimos el modal 
const handleShow = () => {
    setNuevoPlato({nombre: '', descripcion: '', categoria: '', variaciones: [{tipo:'', precio:''}]});
    setShow(true);
}

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
        handleCloseEditModal()
        window.location.reload();
    })
    .catch((error) => {
        alert(error.message);
    });
}
   
//----------------------------------------------------------------------------------------------------------//
//3.BORRAR EL PLATO DESEADO
    const handleDelete = (idPlato) => {    
        if (window.confirm('¿Estás seguro que quieres borrar este plato?')) {
            fetch(`http://localhost:5000/platos/${idPlato}`, {
                method: 'DELETE',
            })
            .then(() => {   //SI se borra de forma correcta, actualizar estado de platos (setPlatos)m fultrando el plato que se elimino para que no aparezca
                setPlatos(platos.filter(plato => plato._id !== idPlato));
                alert("Plato borrado con éxito");
            })
            .catch(() => {
                alert('Hubo un error al intentar borrar este plato');
            });
        }
    }





//Función que se activa ucnado se produce un cambio en un campo de VARIACIÓN en la interfaz de usuario 
//Parametros:
        //Index --> Indice de la variación
        //field --> Campo en el que se está modificando la varicación : tipo o precio 
        //value --> nuevo valor que se le va a asignar al campo 
const handleVariationChange = (index, field, value) => {
    

    if (editPlato && editPlato.variaciones && index >= 0 && index < editPlato.variaciones.length) { //si el plato editado existe    
                                                                                            //si tiene variaciones y si el indice proporcionado es correcto
        // Editar una variación existente en el plato editado
        const updatedEditPlato = { ...editPlato }; //copia del plato editado 
        updatedEditPlato.variaciones[index][field] = value;
        setEditPlato(updatedEditPlato);
    } else { //
        // Agregar una nueva variación al estado nuevoPlato
        setNuevoPlato(prevState => {   //setNuevoPlato : recibe el estado anterior como argumento (prevstate) y devuelve el nuevo estado actualizado
            const updatedVariations = [...prevState.variaciones];
            updatedVariations[index][field] = value;
            return { ...prevState, variaciones: updatedVariations };
        });
    }
};



    //agregar una nueva variación al plato,
            
    const addNewVariation = () => {
        if (show) {
            // Si estamos en el modo de agregar un nuevo plato, actualiza el estado de nuevoPlato
            setNuevoPlato(prevState => { 
                return {
                    ...prevState, 
                    variaciones: [...prevState.variaciones, { tipo: '', precio: 0 }] // Inicializar precio en 0
                };
            });
        } else if (showEditModal) {
            // Si estamos en el modo de edición, actualiza el estado de editPlato
            setEditPlato(prevState => { 
                return {
                    ...prevState, 
                    variaciones: [...prevState.variaciones, { tipo: '', precio: 0 }] // Inicializar precio en 0
                };
            });
        }
    };
    

    return (
        <MenuListForm
            platos={platos}
            show={show}
            handleClose={handleClose}
            handleShow={handleShow}
            handleAdd={handleAdd}
            nuevoPlato={nuevoPlato}
            setNuevoPlato={setNuevoPlato}
            handleVariationChange={handleVariationChange}
            addNewVariation={addNewVariation}
            handleDelete={handleDelete}
            handleShowEditModal={handleShowEditModal}
            showEditModal={showEditModal} 
            editPlato={editPlato} 
            setEditPlato={setEditPlato} 
            handleCloseEditModal={handleCloseEditModal} 
            handleEdit={handleEdit}
            navigate={navigate}
            username={username}
        />
    );  
};
export default MenuList;
    


