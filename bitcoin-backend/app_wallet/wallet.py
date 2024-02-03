import base58
import codecs
import hashlib

from ecdsa import NIST256p
from ecdsa import SigningKey

from .utils import sorted_dict_by_key


class Wallet(object):

    def __init__(self):
        self._private_key = SigningKey.generate(curve=NIST256p)
        self._public_key = self._private_key.get_verifying_key()
        self._blockchain_address = self.generate_blockchain_address()

    @property
    def private_key(self):
        return self._private_key.to_string().hex()

    @property
    def public_key(self):
        return self._public_key.to_string().hex()

    @property
    def blockchain_address(self):
        return self._blockchain_address

    # このアドレスは送信もととかに使われるやつ
    def generate_blockchain_address(self):
        # ECDSAを使ってpublickeyを生成
        public_key_bytes = self._public_key.to_string()
        # 公開鍵にSHA-256ハッシュ関数を適用し、ハッシュ値を取得します。
        sha256_bpk = hashlib.sha256(public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()

        # SHA-256ハッシュ値にさらにRIPEMD-160ハッシュ関数を適用します。これにより、公開鍵から短いハッシュ値が生成されます。
        ripemed160_bpk = hashlib.new('ripemd160')
        ripemed160_bpk.update(sha256_bpk_digest)
        ripemed160_bpk_digest = ripemed160_bpk.digest()
        ripemed160_bpk_hex = codecs.encode(ripemed160_bpk_digest, 'hex')

        # ネットワークバイト（ビットコインのメインネットワークでは 00）をRIPEMD-160ハッシュの前に追加します。
        network_byte = b'00'
        network_bitcoin_public_key = network_byte + ripemed160_bpk_hex

        # ネットワークバイトを含むハッシュ値に対して、さらに2回SHA-256ハッシュ関数を適用します。
        network_bitcoin_public_key_bytes = codecs.decode(
            network_bitcoin_public_key, 'hex')

        sha256_bpk = hashlib.sha256(network_bitcoin_public_key_bytes)
        sha256_bpk_digest = sha256_bpk.digest()
        sha256_2_nbpk = hashlib.sha256(sha256_bpk_digest)
        sha256_2_nbpk_digest = sha256_2_nbpk.digest()
        sha256_hex = codecs.encode(sha256_2_nbpk_digest, 'hex')

        # ダブルSHA-256ハッシュの最初の4バイト（8文字の16進数）をチェックサムとして使用し、
        # これをネットワークバイトとRIPEMD-160ハッシュ値の組み合わせに追加します。
        checksum = sha256_hex[:8]

        address_hex = (network_bitcoin_public_key + checksum).decode('utf-8')

        #Base58エンコーディングを適用して、ユーザーフレンドリーなブロックチェーンアドレスを生成します。
        # これにより、アドレスは英数字のみで構成され、ビットコインアドレスとして認識されやすくなります。
        blockchain_address = base58.b58encode(address_hex).decode('utf-8')
        return blockchain_address


class Transaction(object):

    def __init__(self, sender_private_key, sender_public_key,
                 sender_blockchain_address, recipient_blockchain_address,
                 value):
        self.sender_private_key = sender_private_key
        self.sender_public_key = sender_public_key
        self.sender_blockchain_address = sender_blockchain_address
        self.recipient_blockchain_address = recipient_blockchain_address
        self.value = value

    def generate_signature(self):
        sha256 = hashlib.sha256()
        transaction = sorted_dict_by_key({
            'sender_blockchain_address': self.sender_blockchain_address,
            'recipient_blockchain_address': self.recipient_blockchain_address,
            'value': float(self.value)
        })
        sha256.update(str(transaction).encode('utf-8'))
        message = sha256.digest()
        private_key = SigningKey.from_string(
            bytes().fromhex(self.sender_private_key), curve=NIST256p)
        private_key_sign = private_key.sign(message)
        signature = private_key_sign.hex()
        return signature
