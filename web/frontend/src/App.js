import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Components/Login";
import SignUpPage from "./Components/Signup";
import Dashboard from "./Pages/Dashboard";

const App = () => {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<SignUpPage />} />
          <Route path="/dashboard/" element={<Dashboard />} />

        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;