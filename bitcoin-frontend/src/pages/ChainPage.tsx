import {
  BlockChainType,
  GetChainType,
  TransactionType,
} from "../types/blockchain";
import { axiosInstance } from "../hooks/axiosInstance";
import { useState } from "react";
import axios, { AxiosResponse } from "axios";
import { useSetRecoilState } from "recoil";
import { walletState } from "../globalState/wallet";
import { fetcher } from "../hooks/fetcher";
import useSWR from "swr";
import { Text, Button, Paper, Title, Flex, Card, Badge } from "@mantine/core";
import { useNavigate } from "react-router-dom";
import { TransactionCard } from "../componentes/TransactionCard";

const ChainPage = () => {
  //1秒ごとにfetch
  const { data, error } = useSWR<GetChainType, Error>("/chain", fetcher, {
    refreshInterval: 1000,
  });

  console.log(data);

  const navigate = useNavigate();
  const handleCardClick = (path: string) => {
    navigate(path); // React Routerを使ってURLに遷移
  };

  return (
    <>
      {data?.chain ? (
        <Flex
          gap="md"
          justify="center"
          align="flex-start"
          direction="column"
          wrap="wrap"
        >
          {data.chain.map((chain: BlockChainType, index: number) => (
            <Flex gap="xs" align="center">
              <Card shadow="sm" padding="lg" radius="md" withBorder>
                <Badge color="pink" variant="light">
                  Block:{index}
                </Badge>
                <Text>nonce:{chain.nonce}</Text>
                <Text>previous_hash:{chain.previous_hash}</Text>
                <Text>timestamp:{chain.timestamp}</Text>
                <Text>transactions:{chain.transactions.length}</Text>
              </Card>
              <TransactionCard
                key={chain.timestamp}
                transactions={chain.transactions}
              />
            </Flex>
          ))}
        </Flex>
      ) : (
        <Title order={3}>まだdata</Title>
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
    </>
  );
};
export default ChainPage;
