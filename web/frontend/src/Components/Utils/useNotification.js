import { useState, useEffect } from 'react';
import axios from 'axios';
import notificationSound from '../Sounds/pending-notification.mp3';
import { toast, Bounce } from 'react-toastify';

const useNotifications = () => {
  const [tickets, setTickets] = useState([]);

  const fetchTickets = async () => {
    try {
      const response = await axios.get('http://localhost:5000/pedidos');
      setTickets((oldTickets) => {
        if (oldTickets.length === 0) { //Al principio cuando se carga la página, no aparece ninguna notificación 

          return response.data;
        }
        if (response.data.length > oldTickets.length) {
          let audio = new Audio(notificationSound);
          audio.play().catch((error) => { console.error(error); });
          toast.success('¡Un nuevo pedido ha sido creado!', {
            position: 'top-left',
            autoClose: 5000,
            closeOnClick: true,
            hideProgressBar: false,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            transition: Bounce,
          });
          return response.data;
        }
        return oldTickets;
      });
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchTickets();
    const interval = setInterval(fetchTickets, 5000); //Notificación dura 5sec en la pantalla 
    return () => clearInterval(interval);
  }, []);

  return tickets;
};

export default useNotifications;




