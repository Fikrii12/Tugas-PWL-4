import { BrowserRouter, Route, Routes } from "react-router-dom";
import React from "react";

import Beranda from "./page/Beranda";
import Login from "./page/Login";
import Register from "./page/Register";


export default function RoutesApp() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Beranda />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}
