import { Navigate } from "react-router-dom";
import React from "react";

interface Props {
  children: React.ReactNode;
}

export default function PrivateRoute({ children }: Props) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/" replace />;
}
