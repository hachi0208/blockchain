import { axiosInstance } from "../axiosInstance";
import { useState } from "react";
import { WalletType } from "../../types/wallet";
import axios, { AxiosResponse } from "axios";
import { useSetRecoilState } from "recoil";
import { walletState } from "../../globalState/wallet";

export const usePostTransaction = () => {
  const [postTransactionLoading, setPostTransactionLoading] =
    useState<boolean>(false);
  const [postTransactionError, setPostTransactionError] = useState<
    string | null
  >(null);

  const postTransaction = async (
    sender_private_key: string,
    sender_blockchain_address: string,
    recipient_blockchain_address: string,
    sender_public_key: string,
    value: number
  ) => {
    try {
      setPostTransactionLoading(true);
      const payload = {
        sender_private_key: sender_private_key,
        sender_blockchain_address: sender_blockchain_address,
        recipient_blockchain_address: recipient_blockchain_address,
        sender_public_key: sender_public_key,
        value: value,
      };
      await axiosInstance.post("/transaction", payload);
      setPostTransactionLoading(false);
    } catch (e) {
      if (axios.isAxiosError(e)) {
        setPostTransactionError(e.message);
      }
      setPostTransactionLoading(false);
    }
  };
  return { postTransactionLoading, postTransactionError, postTransaction };
};
