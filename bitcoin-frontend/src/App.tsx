import "./App.css";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./Layout";
import TopPage from "./pages/TopPage";
import WalletPage from "./pages/WalletPage";
import { useRecoilState, RecoilRoot } from "recoil";
import MiningPage from "./pages/MiningPage";
import ChainPage from "./pages/ChainPage";
import TradePage from "./pages/TradePage";

function App() {
  return (
    <BrowserRouter>
      <RecoilRoot>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route>
              <Route index element={<TopPage />}></Route>
              <Route path="/wallet" element={<WalletPage />}></Route>
              <Route path="/mining" element={<MiningPage />}></Route>
              <Route path="/chain" element={<ChainPage />}></Route>
              <Route path="/trade" element={<TradePage />}></Route>
            </Route>
          </Route>
        </Routes>
      </RecoilRoot>
    </BrowserRouter>
  );
}

export default App;
