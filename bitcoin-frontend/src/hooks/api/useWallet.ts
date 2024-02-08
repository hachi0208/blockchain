import { axiosInstance } from "../axiosInstance";
import { useState } from "react";
import { WalletType } from "../../types/wallet";
import axios, { AxiosResponse } from "axios";
import { useSetRecoilState } from "recoil";
import { walletState } from "../../globalState/wallet";

export const usePostWallet = () => {
  const [postWalletLoading, setPostWalletLoading] = useState<boolean>(false);
  const [postWalletError, setPostWalletError] = useState<string | null>(null);
  const setWallet = useSetRecoilState(walletState);

  const postWallet = async () => {
    try {
      setPostWalletLoading(true);
      const response: AxiosResponse = await axiosInstance.post("/wallet");
      setPostWalletLoading(false);
      const data: WalletType = response.data;
      setWallet(data);
    } catch (e) {
      if (axios.isAxiosError(e)) {
        setPostWalletError(e.message);
      }
      setPostWalletLoading(false);
    }
  };
  return { postWalletLoading, postWalletError, postWallet };
};
