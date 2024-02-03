import React from "react";
import "@mantine/core/styles.css";
import { Outlet } from "react-router-dom";

const Layout = () => {
  const port = window.location.port;

  return (
    <div>
      <Outlet />
    </div>
  );
};

export default Layout;
