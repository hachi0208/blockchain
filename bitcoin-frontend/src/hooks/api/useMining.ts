import { axiosInstance } from "../axiosInstance";
import { useState } from "react";
import { WalletType } from "../../types/wallet";
import axios, { AxiosResponse, AxiosError } from "axios";
import { useSetRecoilState } from "recoil";
import { walletState } from "../../globalState/wallet";

export const usePostMining = () => {
  const [postMiningLoading, setPostMiningLoading] = useState<boolean>(false);
  const [postMiningError, setPostMiningError] = useState<string | null>(null);

  const postMining = async (
    blockchain_address: string
  ): Promise<AxiosResponse | undefined> => {
    try {
      setPostMiningLoading(true);
      const response = await axiosInstance.post("/mine", {
        blockchain_address: blockchain_address,
      });
      setPostMiningLoading(false);
      return response;
    } catch (e) {
      if (axios.isAxiosError(e)) {
        setPostMiningError(e.message);
      }
      setPostMiningLoading(false);
    }
  };
  return { postMiningLoading, postMiningError, postMining };
};
