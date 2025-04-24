from rest_framework import serializers
from .models import  NFTAsset, GameTransaction

class NFTAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = NFTAsset
        fields = '__all__'

class GameTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameTransaction
        fields = '__all__'
