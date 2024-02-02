from django.urls import path
from .views import *

urlpatterns = [
    path('wallet', WalletAPIView.as_view(), name='wallet'),
    path('transaction', TransactionAPIView.as_view(), name='transaction'),
    path('wallet/amount', AmountAPIView.as_view(), name='amount'),
]
