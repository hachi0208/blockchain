from django.urls import path
from .views import *

urlpatterns = [
    path('chain', ChainAPIView.as_view(), name='chain'),
    path('mine', MineAPIView.as_view(), name='mine'),
    path('transactions', TransactionAPIView.as_view(), name='transactions'),
    path('mine/start', StartMineAPIView.as_view(), name='start_mine'),
    path('consensus', ConsensusAPIView.as_view(), name='consensus'),
]
