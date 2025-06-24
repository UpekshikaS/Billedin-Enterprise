
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import React, { JSX } from "react";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import PrivateRoute from "./PrivateRoute";
import ProductList from "./pages/productList";
import InvoiceCreate from "./pages/InvoiceCreate";
import AdminDashboard from "./pages/AdminDashboard";

function RequireAuth({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem("authToken");
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/dashboard"
          element={
            <RequireAuth>
              <Dashboard />
            </RequireAuth>
          }
        />
        <Route
          path="/products"
          element={
            <RequireAuth>
              <ProductList />
            </RequireAuth>
          }
        />
        <Route
          path="/invoice"
          element={
            <RequireAuth>
              <InvoiceCreate />
            </RequireAuth>
          }
        />
        <Route
          path="/admin"
          element={
            <RequireAuth>
              <AdminDashboard />
            </RequireAuth>
          }
        />
        <Route path="*" element={<Navigate to="/dashboard" />} />
      </Routes>
    </BrowserRouter>
  );
}
