import "../styles/index.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Homepage from "./components/Homepage";
import Register from "./components/Register";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route path="/homepage/:familyId" element={<Homepage/>}/>
      </Routes>
    </Router>
  )
}

export default App