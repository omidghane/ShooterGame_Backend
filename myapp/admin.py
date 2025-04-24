from django.contrib import admin
from .models import NFTAsset, GameTransaction

@admin.register(NFTAsset)
class NFTAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'token_id', 'owner')
    search_fields = ('name', 'token_id', 'owner__user__username')
    list_filter = ('owner',)

@admin.register(GameTransaction)
class GameTransactionAdmin(admin.ModelAdmin):
    list_display = ('asset', 'sender', 'receiver', 'tx_hash', 'timestamp')
    search_fields = ('tx_hash', 'sender__user__username', 'receiver__user__username')
    list_filter = ('timestamp',)
