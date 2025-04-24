from django.urls import path, include
from .views import NFTAssetClass
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'nfts', NFTAssetViewSet)
# router.register(r'transactions', GameTransactionViewSet)

urlpatterns = [
    # path('send-test-email/', MainClass.send_test_email, name='send_test_email'),
    path('character-names/', NFTAssetClass.as_view(), name='character-names'),
    # path('', include(router.urls)),
]
