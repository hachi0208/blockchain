import { Text, Button, Paper, Title, Flex } from "@mantine/core";
import { usePostMining } from "../hooks/api/useMining";
import { WalletType } from "../types/wallet";
import { useRecoilValue } from "recoil";
import { walletState } from "../globalState/wallet";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import axios, { AxiosResponse, AxiosError } from "axios";

const MiningPage = () => {
  const { postMiningLoading, postMiningError, postMining } = usePostMining();
  const [res, setRes] = useState<string | undefined>();
  const walletData = useRecoilValue(walletState);
  const navigate = useNavigate();

  const handleCardClick = (path: string) => {
    navigate(path); // React Routerを使ってURLに遷移
  };

  const handleMining = async () => {
    if (walletData) {
      try {
        const response = await postMining(walletData.blockchain_address);
        if (response) {
          setRes(response.data.message); // レスポンスからメッセージを設定
        } else {
          // エラーメッセージを設定するなどの処理
        }
      } catch (error) {
        console.error("Mining error:", error);
      }
    }
  };

  return (
    <>
      {walletData ? (
        <>
          <Flex gap="xs" align="center">
            <Title order={3}>Blockchain Address:</Title>
            <Text>{walletData.blockchain_address}</Text>
          </Flex>
          <Button
            variant="light"
            color="violet"
            mt="xl"
            onClick={() => handleMining()}
          >
            Mining
          </Button>
        </>
      ) : (
        <Title order={3}>まだaddressがありません。生成してください。</Title>
      )}

      <Button
        variant="light"
        color="violet"
        mt="xl"
        ml="xl"
        onClick={() => handleCardClick(`/`)}
      >
        ホームへ
      </Button>
      {res && <div>{res}</div>}
    </>
  );
};
export default MiningPage;
