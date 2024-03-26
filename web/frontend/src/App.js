import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Components/Login";
import SignUpPage from "./Components/Signup";
import Dashboard from "./Pages/Dashboard";
import UsuariosInfo from "./Pages/infoUser"

const App = () => {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup/:username" element={<SignUpPage />} />
          <Route path="/dashboard/:username" element={<Dashboard />} />
          <Route path="/userInfo/:username" element={<UsuariosInfo />} />

        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;