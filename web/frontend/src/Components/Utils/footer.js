import React from 'react';

const Footer = () => {
  return (
    <footer className="page-footer font-small pt-2">
      <div className="text-center py-2 text-dark">
        <h5 className="text-uppercase text-dark">Panel de control</h5>
        <p>
        Esta aplicación forma parte de un proyecto de trabajo de fin de grado en Ingeniería Informática de la Universidad de Sevilla y sigue en desarrollo activo.
        </p>
      </div>
      <div className="footer-copyright text-center text-dark my-2">
        © 2024
        <a href="http://www.lsi.us.es/" className="text-secondary"> Departamento de Lenguajes y Sistemas Informáticos</a> |
        <a href="https://www.us.es/" className="text-secondary"> Universidad de Sevilla</a>
      </div>
    </footer>
  );
};

export default Footer;
