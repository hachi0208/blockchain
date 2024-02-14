from django.apps import AppConfig
from .blockchain import BlockChain
import os  # o

class AppChainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_chain'

    def ready(self):
        port = os.getenv('DJANGO_SERVER_PORT', '8000')
        print(port)
        if not hasattr(self, 'blockchain'):
            blockchain = BlockChain(port=port)
            blockchain.run()
            self.blockchain = blockchain
