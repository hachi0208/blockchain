import { BlockChainType } from "../../types/blockchain";
import { axiosInstance } from "../axiosInstance";
import { useState } from "react";
import axios, { AxiosResponse } from "axios";
import { useSetRecoilState } from "recoil";
import { walletState } from "../../globalState/wallet";
import { fetcher } from "../fetcher";
import useSWR from "swr";

export const useGetChain = () => {
  const [getChainLoading, setGetChainLoading] = useState<boolean>(false);
  const [getChainError, setGetChainError] = useState<string | null>(null);

  const getChain = async () => {
    try {
      setGetChainLoading(true);
      await axiosInstance.get("/chain");
      setGetChainLoading(false);
    } catch (e) {
      if (axios.isAxiosError(e)) {
        setGetChainError(e.message);
      }
      setGetChainLoading(false);
    }
  };
  return { getChainLoading, getChainError, getChain };
};
