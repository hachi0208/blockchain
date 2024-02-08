from django.db import models

# Create your models here.
class BlockChainModel(models.Model):
    # モデルのフィールドを定義します
    transaction = models.JSONField(default=list)
    nonce = models.PositiveIntegerField()
    previous_hash = models.CharField(max_length=64)
    timestamp = models.DateTimeField(auto_now_add=True)