import React, { useState , useEffect } from 'react';
import { Table, Button, Modal, Form, Tooltip, OverlayTrigger } from 'react-bootstrap';
import { useNavigate , useParams } from 'react-router-dom';
import MenuListForm from '../Pages/menuListPage';


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
   

//BORRAR EL PLATO DESEADO
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

    //Se ejecuta cada vez que "username" cambie, 
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


    //Resetea los platos y variaciones cuando abrimos el modal 
    const handleShow = () => {
        setNuevoPlato({nombre: '', descripcion: '', categoria: '', variaciones: [{tipo:'', precio:''}]});
        setShow(true);
    }
//Actualizar un campo 
    const handleVariationChange = (index, field, value) => { //index: indice de la variacion dentro de variaciones
                                                             //field: Campo que se quiere actualizar dentro de variacion (variacion o precio)
                                                            //value : Valor del campo que se quiere actulizar
        let newVariations = [...nuevoPlato.variaciones]; //creo nueva copia de nuevoPlato.variaciones
        newVariations[index][field] = value; //se actualiza el campo especifico de field dentro del indice
    
        setNuevoPlato(prevState => {   //luego se actualiza el estado nuevoPlato usando setNuevoPLato
            return {...prevState, variaciones: newVariations} 
        });
    };

    //agregar una nueva variación al plato,
            
    const addNewVariation = () => {
        setNuevoPlato(prevState => { 
            return {...prevState, variaciones: [...prevState.variaciones, {tipo: '', precio: ''}]} 
        });
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
        navigate={navigate}
        username={username}
      />
    );   
};
export default MenuList;
    


