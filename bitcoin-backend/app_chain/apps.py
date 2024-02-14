from django.apps import AppConfig
from .blockchain import BlockChain

class AppChainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_chain'

    def ready(self):
        if not hasattr(self, 'blockchain'):
            blockchain = BlockChain(port='8000')
            blockchain.run()
            self.blockchain = blockchain
