import contextlib
import hashlib
import json
import logging
import sys
import time
import threading
import os
from ecdsa import NIST256p
from ecdsa import VerifyingKey
import requests

from .utils import sorted_dict_by_key, find_neighbours, get_host



#0が最初に何個揃うか
MINING_DIFFICULTY = 4

MINING_SENDER = 'THE BLOCKCHAIN'

#miningしたときに貰える金額
MINING_REWARD = 1.0
MINING_TIMER_SEC = 20

#どこのportで動かすか
BLOCKCHAIN_PORT_RANGE = (8000, 8003)
NEIGHBOURS_IP_RANGE_NUM = (0, 1)
BLOCKCHAIN_NEIGHBOURS_SYNC_TIME_SEC = 20

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)


class BlockChain(object):

    #定義
    def __init__(self, blockchain_address=None, port=None):
        #transactionをチェーンに繋げるまで保存する場所
        self.transaction_pool = []
        self.chain = []
        self.neighbours = []
        self.create_block(0, self.hash({}))
        self.blockchain_address = blockchain_address
        self.port = port
        #semaphoreの1は同時アクセス数
        self.mining_semaphore = threading.Semaphore(1)
        self.sync_neighbours_semaphore = threading.Semaphore(1)

    def run(self):
        self.sync_neighbours()
        self.resolve_conflicts()
        self.start_mining()

    def set_neighbours(self):
        self.neighbours = find_neighbours(
            get_host(), self.port,
            NEIGHBOURS_IP_RANGE_NUM[0], NEIGHBOURS_IP_RANGE_NUM[1],
            BLOCKCHAIN_PORT_RANGE[0], BLOCKCHAIN_PORT_RANGE[1])
        logger.info({
            'action': 'set_neighbours', 'neighbours': self.neighbours
        })

    # 他のノード（port）を探す
    # セマフォはこのATMの利用権を表しています。
    # もしATMが利用中でなければ（セマフォが利用可能であれば）、最初に来た人（スレッド）がATMを使用できます。
    # しかし、もしATMが既に使用中であれば（セマフォが利用不可能であれば）、他の人（スレッド）は待たずに離れて他のことをします
    def sync_neighbours(self):
        #falseにすることでセマフォが利用可能でない場合にスレッドが待機するのではなく、ただちに False を返してメソッドの実行を続行します
        # このコマンドは、セマフォを「非ブロッキングモード」で取得しようとします。
        # つまり、セマフォが利用可能であれば、それを取得して先に進みます。
        # しかし、もしセマフォがすでに別のスレッドによって取得されている場合、このコマンドは待たずにすぐに False を返し、処理を終了します。
        # これにより、複数のスレッドが同時に同じ処理を行うのを防ぎます。
        is_acquire = self.sync_neighbours_semaphore.acquire(blocking=False)
        #空いてたら（trueなら）実行
        if is_acquire:
            with contextlib.ExitStack() as stack:
                # with ブロックを抜ける際（たとえばメソッドの終わりに到達するか、エラーが発生した場合など）、
                # 確実にセマフォが解放されることが保証されます。
                # ようは一番最後に解放されるってこと。
                stack.callback(self.sync_neighbours_semaphore.release)
                self.set_neighbours()
                # 定期的に繰り返す
                loop = threading.Timer(
                    BLOCKCHAIN_NEIGHBOURS_SYNC_TIME_SEC, self.sync_neighbours)
                loop.start()

    def create_block(self, nonce, previous_hash):
        block = sorted_dict_by_key({
            'timestamp': time.time(),
            'transactions': self.transaction_pool,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        self.chain.append(block)
        self.transaction_pool = []

        for node in self.neighbours:
            requests.delete(f'http://{node}/api/transactions')

        return block

    def hash(self, block):
        sorted_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(sorted_block.encode()).hexdigest()

    def add_transaction(self, sender_blockchain_address,
                        recipient_blockchain_address, value,
                        sender_public_key=None, signature=None):
        transaction = sorted_dict_by_key({
            'sender_blockchain_address': sender_blockchain_address,
            'recipient_blockchain_address': recipient_blockchain_address,
            'value': float(value)
        })

        if sender_blockchain_address == MINING_SENDER:
            self.transaction_pool.append(transaction)
            return True

        if self.verify_transaction_signature(
                sender_public_key, signature, transaction):

            if (self.calculate_total_amount(sender_blockchain_address)
                    < float(value)):
                logger.error(
                        {'action': 'add_transaction', 'error': 'no_value'})
                return False

            self.transaction_pool.append(transaction)
            return True
        return False

    def create_transaction(self, sender_blockchain_address,
                           recipient_blockchain_address, value,
                           sender_public_key, signature):

        is_transacted = self.add_transaction(
            sender_blockchain_address, recipient_blockchain_address,
            value, sender_public_key, signature)

        if is_transacted:
            for node in self.neighbours:
                requests.put(
                    f'http://{node}/api/transactions',
                    json={
                        'sender_blockchain_address': sender_blockchain_address,
                        'recipient_blockchain_address':
                            recipient_blockchain_address,
                        'value': value,
                        'sender_public_key': sender_public_key,
                        'signature': signature,
                    }
                )
        return is_transacted

    def verify_transaction_signature(
            self, sender_public_key, signature, transaction):
        sha256 = hashlib.sha256()
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        signature_bytes = bytes().fromhex(signature)
        verifying_key = VerifyingKey.from_string(
            bytes().fromhex(sender_public_key), curve=NIST256p)
        verified_key = verifying_key.verify(signature_bytes, message)
        return verified_key

    def valid_proof(self, transactions, previous_hash, nonce,
                    difficulty=MINING_DIFFICULTY):
        guess_block = sorted_dict_by_key({
            'transactions': transactions,
            'nonce': nonce,
            'previous_hash': previous_hash
        })
        guess_hash = self.hash(guess_block)
        return guess_hash[:difficulty] == '0'*difficulty

    def proof_of_work(self):
        transactions = self.transaction_pool.copy()
        previous_hash = self.hash(self.chain[-1])
        nonce = 0
        while self.valid_proof(transactions, previous_hash, nonce) is False:
            nonce += 1
        return nonce

    def mining(self, blockchain_address):
        # if not self.transaction_pool:
        #     return False
        print(blockchain_address)

        self.add_transaction(
            sender_blockchain_address=MINING_SENDER,
            recipient_blockchain_address=blockchain_address,
            value=MINING_REWARD)
        nonce = self.proof_of_work()
        previous_hash = self.hash(self.chain[-1])
        self.create_block(nonce, previous_hash)
        logger.info({'action': 'mining', 'status': 'success'})

        for node in self.neighbours:
            requests.put(f'http://{node}/api/consensus')

        return True

    def start_mining(self):
        port = f"{os.getenv('DJANGO_SERVER_PORT', '8000')}+port"
        is_acquire = self.mining_semaphore.acquire(blocking=False)
        if is_acquire:
            with contextlib.ExitStack() as stack:
                stack.callback(self.mining_semaphore.release)
                self.mining(port)
                loop = threading.Timer(MINING_TIMER_SEC, self.start_mining)
                loop.start()

    def calculate_total_amount(self, blockchain_address):
        total_amount = 0.0
        for block in self.chain:
            for transaction in block['transactions']:
                value = float(transaction['value'])
                if blockchain_address == \
                        transaction['recipient_blockchain_address']:
                    total_amount += value
                if blockchain_address == \
                        transaction['sender_blockchain_address']:
                    total_amount -= value
        return total_amount

    # blockchainが有効であるかどうか
    def valid_chain(self, chain):
        pre_block = chain[0]
        current_index = 1
        # blockが全部有効かチェック
        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(pre_block):
                return False

            if not self.valid_proof(
                    block['transactions'], block['previous_hash'],
                    block['nonce'], MINING_DIFFICULTY):
                return False

            pre_block = block
            current_index += 1
        return True

    # 他のノードと比較し、他のノードの方が長ければそれに自分も反映させる
    def resolve_conflicts(self):
        longest_chain = None
        max_length = len(self.chain)
        for node in self.neighbours:
            response = requests.get(f'http://{node}/api/chain')
            if response.status_code == 200:
                response_json = response.json()
                chain = response_json['chain']
                chain_length = len(chain)
                if chain_length > max_length and self.valid_chain(chain):
                    max_length = chain_length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            logger.info({'action': 'resolve_conflicts', 'status': 'replaced'})
            return True

        logger.info({'action': 'resolve_conflicts', 'status': 'not_replaced'})
        return False
