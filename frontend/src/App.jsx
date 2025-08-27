import "../styles/index.css";
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import Memberspage from "./components/Memberspage";

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login/>}/>
        <Route path="/register" element={<Register/>}/>
        <Route path="/memberspage/:familyId" element={<Memberspage/>}/>
      </Routes>
    </Router>
  )
}

export default App