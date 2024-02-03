import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import { MantineProvider } from "@mantine/core";
import Layout from "./Layout";
import TopPage from "./pages/TopPage";
import { useRecoilState } from "recoil";

function App() {
  return (
    <MantineProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route>
              <Route index element={<TopPage />}></Route>
            </Route>
          </Route>
        </Routes>
      </BrowserRouter>
    </MantineProvider>
  );
}

export default App;
