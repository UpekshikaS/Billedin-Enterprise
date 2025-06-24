import React, { ReactElement } from "react";
import { Navigate } from "react-router-dom";

interface Props {
  children: ReactElement;
}

const PrivateRoute = ({ children }: Props): ReactElement => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/" replace />;
};

export default PrivateRoute;
