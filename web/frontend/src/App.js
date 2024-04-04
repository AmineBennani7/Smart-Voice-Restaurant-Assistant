import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Components/Login";
import SignUpPage from "./Components/Signup";
import Dashboard from "./Pages/Dashboard";
import UsuariosInfo from "./Pages/infoUser"
import MenuList from "./Components/menuList"
import CustomizationForm from "./Pages/customizationPage"

const App = () => {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/menuList/:username" element={<MenuList />} />
          <Route path="/signup/:username" element={<SignUpPage />} />
          <Route path="/dashboard/:username" element={<Dashboard />} />
          <Route path="/userInfo/:username" element={<UsuariosInfo />} />
          <Route path="/customizationApp" element= {<CustomizationForm/>} />


        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;