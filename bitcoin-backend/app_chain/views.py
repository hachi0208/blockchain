from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .blockchain import BlockChain


# Create your views here.
# グローバル変数としてブロックチェーンインスタンスを作成
blockchain = BlockChain()

class ChainAPIView(APIView):
    def get(self, request, *args, **kwargs):
        chain = blockchain.chain
        return Response({'chain': chain}, status=status.HTTP_200_OK)

class MineAPIView(APIView):
    #postに変更。誰がminingしたかわからない
    def post(self, request, *args, **kwargs):
        blockchain_address = request.data.get('blockchain_address')
        print(blockchain_address)
        result = blockchain.mining(blockchain_address)
        if result:
            return Response({'message': 'New block mined'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Mining failed'}, status=status.HTTP_400_BAD_REQUEST)

class TransactionAPIView(APIView):
    def get(self, request, *args, **kwargs):
        transactions = blockchain.transaction_pool
        return Response({
            'transactions': transactions,
            'length': len(transactions)
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        required = [
            'sender_blockchain_address',
            'recipient_blockchain_address',
            'value',
            'sender_public_key',
            'signature'
        ]
        if not all(k in data for k in required):
            return Response({'message': 'missing values'}, status=status.HTTP_400_BAD_REQUEST)

        is_created = blockchain.create_transaction(
            data['sender_blockchain_address'],
            data['recipient_blockchain_address'],
            data['value'],
            data['sender_public_key'],
            data['signature']
        )
        if not is_created:
            return Response({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'success'}, status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        blockchain.transaction_pool = []
        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class StartMineAPIView(APIView):
    def get(self, request, *args, **kwargs):
        blockchain.start_mining()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)

class ConsensusAPIView(APIView):
    def put(self, request, *args, **kwargs):
        replaced = blockchain.resolve_conflicts()
        return Response({'replaced': replaced}, status=status.HTTP_200_OK)