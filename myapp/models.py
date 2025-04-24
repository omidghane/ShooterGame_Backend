from django.db import models
from accounts.models import User 


class NFTAsset(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    token_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    metadata = models.JSONField()

class GameTransaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_tx')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_tx')
    asset = models.ForeignKey(NFTAsset, on_delete=models.CASCADE)
    tx_hash = models.CharField(max_length=255, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
