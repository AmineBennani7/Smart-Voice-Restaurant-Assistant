import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./Components/LoginSignup/LoginPage";
import SignUpPage from "./Components/LoginSignup/SignupPage";

const App = () => {
  return (
    <BrowserRouter>
      <div className="App">
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/signup" element={<SignUpPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

export default App;