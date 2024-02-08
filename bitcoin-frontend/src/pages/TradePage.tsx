import React, { useState } from "react";
import { useRecoilValue } from "recoil";
import { walletState } from "../globalState/wallet";
import { useNavigate } from "react-router-dom";
import { usePostTransaction } from "../hooks/api/useTransaction";
import {
  Button,
  TextInput,
  NumberInput,
  Group,
  Box,
  Text,
} from "@mantine/core"; // UI コンポーネント

const TradePage = () => {
  const { postTransaction, postTransactionLoading, postTransactionError } =
    usePostTransaction();
  const walletData = useRecoilValue(walletState);
  const navigate = useNavigate();

  // フォームの状態を管理
  const [senderPrivateKey, setSenderPrivateKey] = useState<string | undefined>(
    walletData?.private_key
  );
  const [senderPublicKey, setSenderPublicKey] = useState<string | undefined>(
    walletData?.public_key
  );
  const [senderBlockchainAddress, setSenderBlockchainAddress] = useState<
    string | undefined
  >(walletData?.blockchain_address);
  const [recipientBlockchainAddress, setRecipientBlockchainAddress] =
    useState<string>("");
  const [value, setValue] = useState<number>(0);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); // フォーム送信のデフォルト動作を防ぐ
    // postTransaction 関数を呼び出し
    if (
      senderPrivateKey &&
      senderBlockchainAddress &&
      recipientBlockchainAddress &&
      senderPublicKey
    ) {
      await postTransaction(
        senderPrivateKey,
        senderBlockchainAddress, // 送信者のブロックチェーンアドレス
        recipientBlockchainAddress,
        senderPublicKey, // 送信者の公開鍵
        value
      );
    }
    // 成功した後のアクション（例：トランザクション履歴ページへのナビゲートなど）
  };

  return (
    <Box component="form" onSubmit={handleSubmit}>
      <TextInput
        label="Sender Private Key"
        value={senderPrivateKey}
        onChange={(e) => setSenderPrivateKey(e.target.value)}
        required
      />
      <TextInput
        label="Sender Blockchain Address"
        value={senderBlockchainAddress}
        onChange={(e) => setSenderBlockchainAddress(e.target.value)}
        required
      />
      <TextInput
        label="Sender Public Key"
        value={senderPublicKey}
        onChange={(e) => setSenderPublicKey(e.target.value)}
        required
      />
      <TextInput
        label="Recipient Blockchain Address"
        value={recipientBlockchainAddress}
        onChange={(e) => setRecipientBlockchainAddress(e.target.value)}
        required
      />

      <NumberInput
        label="Value"
        value={value}
        // `as number` を使用して `val` を `number` 型にキャスト
        onChange={(val) => setValue(val as number)}
        required
      />

      <Button type="submit" loading={postTransactionLoading}>
        Send Transaction
      </Button>

      {postTransactionError && <Text c="red">{postTransactionError}</Text>}
    </Box>
  );
};

export default TradePage;
