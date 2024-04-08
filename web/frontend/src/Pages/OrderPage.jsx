import React from 'react';
import { Button, Table, Container } from 'react-bootstrap';
import { ArrowLeft } from 'react-bootstrap-icons'; 
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer, toast , Bounce} from 'react-toastify';


const OrderForm = ({ pedidos, onDelete, navigate, username }) => {
    return (
        <Container>
        <div style={{display: 'flex', flexDirection: 'row', alignItems: 'center'}}>
              <Button 
            variant="light" 
            onClick={() => navigate(`/dashboard/${username}`)} 
            style={{border: 'none'}}>
            <ArrowLeft size={36} />
            </Button>
            <h1 className="my-4">Lista de pedidos en curso</h1>
        </div>
        <Table responsive="md">
                <thead>
                    <tr>
                        <th>Número de pedido</th>
                        <th>Platos</th>
                        <th>Precio Total</th>
                        <th>Acción</th>
                    </tr>
                </thead>
                <tbody>
                {Array.isArray(pedidos) && pedidos.map(pedido => (
        <tr key={pedido._id.$oid}>
                            <td>{pedido.numero_pedido}</td>
                            <td>
                                {pedido.platos.map((plato, index) => (
                                    <p key={index}>
                                        Tipo: {plato.tipo}, Nombre: {plato.nombre}, Tamaño:
                                        {plato.tamaño}, Precio: {plato.precio}€, Cantidad: {plato.cantidad}
                                    </p>
                                ))}
                            </td>
                            <td>{pedido.precio_total}€</td>
                            <td>
                                <Button variant="danger" onClick={() => onDelete(pedido._id.$oid)}>
                                   ¡ Pedido listo !
                                </Button>
                            </td>
                    </tr>
                    ))}
                </tbody>
            </Table>
            <ToastContainer/>
        </Container>
    );
}

export default OrderForm;