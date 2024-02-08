export interface TransactionType {
  recipient_blockchain_address: string;
  sender_blockchain_address: string;
  value: number;
}

export interface TransactionsType {
  transactions: TransactionType[];
  length: number;
}

export interface BlockChainType {
  nonce: number;
  previous_hash: string;
  timestamp: number;
  transactions: TransactionType[];
}

export interface GetChainType {
  chain: BlockChainType[];
}
