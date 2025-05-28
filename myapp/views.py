from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from accounts.models import User
from .models import NFTAsset, GameTransaction
from .serializers import NFTAssetSerializer, GameTransactionSerializer

# class MainClass(APIView):
#     # permission_classes = [IsAuthenticated]
    
#     def send_test_email(request):
#         subject = 'Test Email from Django'
#         message = 'This is a test email sent from Django using SMTP on Liara server.'
#         recipient_list = ['omidjt2015@gmail.com']
        
#         email = EmailMessage(
#             subject,
#             message,
#             settings.EMAIL_FROM_ADDRESS,
#             recipient_list,
#             headers={"x-liara-tag": "test-tag"},
#         )

        
#         email.send(fail_silently=False)
#         return HttpResponse('Test email sent successfully!')

#     def get_character_names(request):
#         print(request.headers)
#         return JsonResponse({"names": ["Agile", "Tough"]})

class NFTAssetClass(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the authenticated user
        assets = NFTAsset.objects.filter(owner=user)  # Fetch NFTs owned by the user

        nft_names = [asset.name for asset in assets]  # Extract NFT names

        return Response({
            "username": user.username,
            "nft_names": nft_names
        }) 

class FetchUserNFTs(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  # Optional, but keeps it secure

    def get(self, request):
        # Get the username or wallet from query params
        username = request.query_params.get('username')
        wallet_address = request.query_params.get('wallet')

        try:
            if username:
                user = User.objects.get(username=username)
            elif wallet_address:
                user = User.objects.get(wallet_address=wallet_address)
            else:
                return Response({"error": "Username or wallet address is required."}, status=400)

            # Fetch their NFTs
            assets = NFTAsset.objects.filter(owner=user)

            data = [
                {
                    "token_id": asset.token_id,
                    "name": asset.name,
                    "image_url": asset.image_url,
                    "metadata": asset.metadata,
                }
                for asset in assets
            ]

            return Response({"user": user.username, "assets": data})

        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
