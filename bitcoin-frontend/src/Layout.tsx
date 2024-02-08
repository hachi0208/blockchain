import "@mantine/core/styles/Text.css";
import { MantineProvider } from "@mantine/core";
import React from "react";
import "@mantine/core/styles.css";
import { Outlet } from "react-router-dom";
import { Container } from "@mantine/core";

const Layout = () => {
  return (
    <MantineProvider>
      <Container size="xl" mt="xl">
        <Outlet />
      </Container>
    </MantineProvider>
  );
};

export default Layout;
