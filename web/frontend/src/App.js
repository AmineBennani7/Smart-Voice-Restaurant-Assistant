// App.js

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Login from './Components/Login';
import SignUpPage from './Components/Signup';
import Dashboard from './Components/Dashboard';
import UsuariosInfo from './Pages/infoUser';
import MenuList from './Components/menuList';
import Customization from './Components/Customization';
import Orders from './Components/Order';
import Footer from './Components/Utils/footer';

const App = () => {
    return (
        <BrowserRouter>
            <div className="App">
                <Routes>
                    <Route path="/" element={<Login />} />
                <Route path="/menuList/:username" element={<MenuList />} />
                <Route path="/signup/:username" element={<SignUpPage />} />
                <Route path="/userInfo/:username" element={<UsuariosInfo />} />
                <Route path="/customizationApp/:username" element={<Customization />} />
                <Route path="/orders/:username" element={<Orders />} />

                    <Route path="/dashboard/:username" element={<Dashboard />} />
                </Routes>
            </div>
        </BrowserRouter>
    );
};


export default App;
