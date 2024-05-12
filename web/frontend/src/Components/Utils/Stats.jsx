import React, { useEffect, useState } from 'react';
import { Chart } from 'react-google-charts';
import axios from 'axios';

const PlatosPie = () => {
  const [categoriasData, setCategoriasData] = useState([]);
  const [pedidosActivos, setPedidosActivos] = useState(0);
  const [empleadosActivos, setEmpleadosActivos] = useState(0);
  const [platosActivos, setPlatosActivos] = useState(0);
  const [categoriasActivas, setCategoriaActivas] = useState(0);

  
  const fetchData = async () => {
    try {
      
        //PORCENTAJE DE PLATOS POR CATEGORIA: 


        // Obtener la lista de categorías desde el backend
        const responseCategorias = await axios.get('http://localhost:5000/categorias');
        const categorias = responseCategorias.data;
    
        console.log('Categorías obtenidas:', categorias);

        

        // Obtener todos los platos desde el backend
        const responsePlatos = await axios.get('http://localhost:5000/platos');
        const platos = responsePlatos.data;
        console.log('Platos obtenidos:', platos);


        // Calcular el recuento de platos por categoría
        const platosCount = {};
        platos.forEach(plato => {
          const { categoria } = plato;
          platosCount[categoria] = platosCount[categoria] ? platosCount[categoria] + 1 : 1;
        });
        console.log('Recuento de platos por categoría:', platosCount);

        // Calcular el porcentaje de platos por categoría
        const totalPlatos = platos.length;
        const categoriasWithPercentage = categorias.map(categoria => {
          const count = platosCount[categoria] || 0;
        
          const percentage = (count / totalPlatos) * 100;
          return [categoria, percentage];
        });
        console.log('Categorías con porcentajes:', categoriasWithPercentage);

        // Actualizar el estado con los datos de categorías y porcentajes
        setCategoriasData([['Categoría', 'Porcentaje'], ...categoriasWithPercentage]);

        //----------------------------------------------------------------------------------------------//
        //NUMERO DE PEDIDOS ACTIVOS

        // Obtener el número de pedidos activos
        const responsePedidos = await axios.get('http://localhost:5000/pedidos');
        const pedidosData = responsePedidos.data;
       // console.log(pedidosData)
       const pedidos = JSON.parse(pedidosData);
       // console.log(pedidos.length) 


        // Calcular el número de pedidos activos (total de documentos en la colección de pedidos)
        const numeroPedidosActivos = (pedidos.length) ;
       // console.log(numeroPedidosActivos)

        // Establecer el estado con el número de pedidos activos
        setPedidosActivos(numeroPedidosActivos);

      
 //----------------------------------------------------------------------------------------------//
 //NUMERO DE EMPLEADOS ACTIVOS 
 const responseUsuarios = await axios.get('http://localhost:5000/users');
 const usersData = responseUsuarios.data;
 console.log("Empleados", usersData)



 const empleadosActivos = (usersData.length) ;
 setEmpleadosActivos(empleadosActivos);

//----------------------------------------------------------------------------------------------//
 //NUMERO DE PLATOS ACTIVOS

        const platosData = responsePlatos.data;
        const platosActivos = (platosData.length) ;
        setPlatosActivos(platosActivos);


//---------------------------------------------
//Numero de categorias: 
const categoriasActivas=categorias.length
setCategoriaActivas = setCategoriaActivas(categoriasActivas)


} catch (error) {
  console.error('Error fetching data:', error);
}
};
useEffect(() => {
  fetchData();
  const intervalId = setInterval(fetchData, 5000); // llama a fetchData cada 5 segundos

  return () => clearInterval(intervalId); // detiene el intervalo cuando el componente se desmonta
}, []); 
  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-6">
          <Chart
            width={'100%'}
            height={'400px'}
            chartType="PieChart"
            loader={<div>Cargando gráfico...</div>}
            data={categoriasData}
            options={{
              title: 'Porcentaje de Platos por Categoría en el Menú',
              backgroundColor: '#fafbfe', // Establece el color de fondo del gráfico
            }}
          />
        </div>
        <div className="col-md-6 d-flex justify-content-center p-3">
        <div className="card">
      <div className="card-header">
        Estadísticas
      </div>
      <ul className="list-group list-group-flush ">
        <li className=" text-start list-group-item">
          <strong>Número de Pedidos Activos : </strong> {pedidosActivos}
        </li>
        <li className="text-start list-group-item">
          <strong>Número de Empleados Activos : </strong> {empleadosActivos}

        </li>
        <li className="text-start list-group-item">
          <strong>Número de Platos Disponibles:</strong> {platosActivos}

</li>
<li className="text-start list-group-item">
          <strong>Número de Categorías de Platos :</strong> {categoriasActivas}

</li>


      </ul>
    </div>
        </div>
      </div>
    </div>
  );
};

export default PlatosPie;
