import { Text, Button, Paper, Title, Flex } from "@mantine/core";
import { usePostWallet } from "../hooks/api/useWallet";
import { WalletType } from "../types/wallet";
import { useRecoilValue } from "recoil";
import { walletState } from "../globalState/wallet";
import { useNavigate } from "react-router-dom";

const WalletPage = () => {
  const { postWalletLoading, postWalletError, postWallet } = usePostWallet();
  const walletData = useRecoilValue(walletState);
  const navigate = useNavigate();

  const handleCardClick = (path: string) => {
    navigate(path); // React Routerを使ってURLに遷移
  };

  return (
    <>
      {walletData ? (
        <Paper
          shadow="xs"
          radius="xl"
          p="xl"
          style={{ backgroundColor: "#E7D6FB" }}
        >
          <Flex gap="xs" align="center">
            <Title order={3}>Private Key:</Title>
            <Text>{walletData.private_key}</Text>
          </Flex>
          <Flex gap="xs" align="center">
            <Title order={3}>Public:</Title>
            <Text>{walletData.public_key}</Text>
          </Flex>
          <Flex gap="xs" align="center">
            <Title order={3}>Blockchain Address:</Title>
            <Text>{walletData.blockchain_address}</Text>
          </Flex>
        </Paper>
      ) : (
        <Title order={3}>まだKeyがありません。生成してください。</Title>
      )}
      <Button
        variant="light"
        color="violet"
        mt="xl"
        onClick={() => postWallet()}
      >
        Keyを取得
      </Button>
      <Button
        variant="light"
        color="violet"
        mt="xl"
        ml="xl"
        onClick={() => handleCardClick(`/`)}
      >
        ホームへ
      </Button>
    </>
  );
};
export default WalletPage;
