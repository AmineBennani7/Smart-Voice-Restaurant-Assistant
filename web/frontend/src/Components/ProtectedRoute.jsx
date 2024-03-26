import React, { useEffect, useState } from "react";
import { Route, Navigate } from "react-router-dom";

const ProtectedRoute = ({ element, ...rest }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  return isAuthenticated ? <Route {...rest} element={element} /> : <Navigate to="/" />;
};

export default ProtectedRoute;