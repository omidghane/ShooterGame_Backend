from django.urls import path, include
from .views import NFTAssetClass, ManageNFT
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'nfts', NFTAssetViewSet)
# router.register(r'transactions', GameTransactionViewSet)

urlpatterns = [
    # path('send-test-email/', MainClass.send_test_email, name='send_test_email'),
    path('character-names/', NFTAssetClass.as_view(), name='character-names'),
    path('nft/add/', ManageNFT.as_view(), name='add-nft'),  # URL for adding an NFT
    path('nft/remove/', ManageNFT.as_view(), name='remove-nft'),  # URL for removing or selling an NFT
    # path('', include(router.urls)),
]
