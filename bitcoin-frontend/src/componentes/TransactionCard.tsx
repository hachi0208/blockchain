import { FC } from "react";
import { TransactionType } from "../types/blockchain";
import { Text, Card, Badge } from "@mantine/core";

type TransactionCardProps = {
  key: number;
  transactions: TransactionType[];
};

export const TransactionCard: FC<TransactionCardProps> = ({ transactions }) => {
  return (
    <Card shadow="sm" padding="lg" radius="md" withBorder>
      {transactions.length > 0 ? (
        transactions.map((transaction: TransactionType, index: number) => (
          <>
            <Badge color="green" variant="light" fullWidth>
              transaction:{index}
            </Badge>
            <Text>
              recipient_blockchain_address:
              {transaction.recipient_blockchain_address}
            </Text>
            <Text>
              sender_blockchain_address:{transaction.sender_blockchain_address}
            </Text>
            <Text>value:{transaction.value}</Text>
          </>
        ))
      ) : (
        <Text>取引なし</Text>
      )}
    </Card>
  );
};
