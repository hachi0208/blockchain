from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .wallet import Wallet, Transaction
import requests
import urllib.parse


# Create your views here.
class WalletAPIView(APIView):
    def post(self, request, *args, **kwargs):
        my_wallet = Wallet()
        response = {
            'private_key': my_wallet.private_key,
            'public_key': my_wallet.public_key,
            'blockchain_address': my_wallet.blockchain_address,
        }
        return Response(response, status=status.HTTP_200_OK)

class TransactionAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        required = (
            'sender_private_key',
            'sender_blockchain_address',
            'recipient_blockchain_address',
            'sender_public_key',
            'value')
        if not all(k in data for k in required):
            return Response('missing values', status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction(
            data['sender_private_key'],
            data['sender_public_key'],
            data['sender_blockchain_address'],
            data['recipient_blockchain_address'],
            float(data['value']))

        json_data = {
            'sender_blockchain_address': data['sender_blockchain_address'],
            'recipient_blockchain_address': data['recipient_blockchain_address'],
            'sender_public_key': data['sender_public_key'],
            'value': data['value'],
            'signature': transaction.generate_signature(),
        }

        response = requests.post(
            urllib.parse.urljoin('http://127.0.0.1:5000', 'transactions'),
            json=json_data, timeout=3)

        if response.status_code == 201:
            return Response({'message': 'success'}, status=status.HTTP_201_CREATED)
        return Response({'message': 'fail', 'response': response.content}, status=status.HTTP_400_BAD_REQUEST)

class AmountAPIView(APIView):
    def get(self, request, *args, **kwargs):
        blockchain_address = request.GET.get('blockchain_address')
        if not blockchain_address:
            return Response('Missing values', status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(
            urllib.parse.urljoin('http://127.0.0.1:5000', 'amount'),
            {'blockchain_address': blockchain_address},
            timeout=3)
        if response.status_code == 200:
            total = response.json()['amount']
            return Response({'message': 'success', 'amount': total}, status=status.HTTP_200_OK)
        return Response({'message': 'fail', 'error': response.content}, status=status.HTTP_400_BAD_REQUEST)