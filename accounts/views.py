from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from .forms import *
from .models import *
import random
from mysite.utils.sendsms import send_sms
from .serializers import *
from datetime import timedelta
from django.conf import settings
# Create your views here.

from django.db import IntegrityError 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(
                    request, username=username, password=password
                )
                if user is not None:
                    login(request, user)
                    request.session.set_expiry(3600)
                    return redirect(request.GET.get("next", '/'))
                else:
                    messages.error(request, "نام کاربری یا رمز عبور اشتباه می باشد.", 'danger')
            else:
                return render(request, "accounts/login.html", {"form": form})

        form = LoginForm()
        context = {"form": form, "next": request.GET.get("next", '/')}
        return render(request, "accounts/login.html", context)
    else:
        next = request.GET.get("next", '/')
        return redirect(next)


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.filter(username=username)
            if user.exists():
                messages.error(request, "نام کاربری موجود می باشد.", 'danger')
                return redirect("accounts:register")
            else:
                user = User.objects.create_user(username=username, password=password,
                                                is_personnel=form.cleaned_data.get("is_personnel"))
                user.save()
                messages.success(request, "حساب کاربری با موفقیت ایجاد شد.", 'success')
                return redirect("accounts:login")
        else:
            return render(
                request, "accounts/register.html", {"form": form}
            )

    form = RegisterForm()
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def verify(request, phone=None):
    if request.method == "POST":
        form = CodeForm(request.POST)
        if form.is_valid():
            code1 = form.cleaned_data.get("code1")
            code2 = form.cleaned_data.get("code2")
            code3 = form.cleaned_data.get("code3")
            code4 = form.cleaned_data.get("code4")
            code5 = form.cleaned_data.get("code5")
            code6 = form.cleaned_data.get("code6")

            code = str(code1) + str(code2) + str(code3) + str(code4) + str(code5) + str(code6)

            true_code = PhoneLogin.objects.filter(phone=phone, code=code, expires_at__gt=datetime.now(), used=False)

            if true_code.exists():
                true_code.update(used=True)
                return redirect('accounts:user_closet_form')
    else:
        form = CodeForm()
        context = {"phone": phone, "form": form}
        return render(request, "accounts/verify.html", context=context)


def login_phone_view(request):
    if request.method == "POST":
        form = PhoneForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get("phone")
            code = str(random.randint(100000, 999999))

            send_sms(phone, code)

            PhoneLogin.objects.create(phone=phone, code=code, created_at=datetime.now(),
                                      expires_at=(datetime.now() + timedelta(minutes=2)))

            return redirect('accounts:verify', phone=phone)

    form = PhoneForm()
    return render(request, "accounts/phone.html", context={'form': form})


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [IsAuthenticated]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            response.data['refresh_expires_in'] = int(refresh_token_lifetime.total_seconds())
            response.data['access_expires_in'] = int(access_token_lifetime.total_seconds())
        return response

class SimpleTokenObtainPairView(TokenObtainPairView):
    serializer_class = SimpleTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
            response.data['refresh_expires_in'] = int(refresh_token_lifetime.total_seconds())
            response.data['access_expires_in'] = int(access_token_lifetime.total_seconds())
        return response


class TokenRefreshView(TokenRefreshView):
    pass


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get("username") 
        password = data.get("password")
        wallet_address = data.get("wallet_address")
        is_personnel = data.get("is_personnel", False)

        if not username or not password or not wallet_address:
            raise ValidationError({"error": "Username, password, and wallet address are required."})

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        try:

            user = User.objects.create_user(
                username=username,
                password=password,
                is_personnel=is_personnel,
                wallet_address=wallet_address  # Assuming the User model has a wallet_address field
            )
            user.save()

            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)
            tokens = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            refresh_token_lifetime = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
            access_token_lifetime = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

            return Response({
                "message": "User registered successfully.",
                "tokens": tokens,
                "refresh_expires_in": int(refresh_token_lifetime.total_seconds()),
                "access_expires_in": int(access_token_lifetime.total_seconds())
            }, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            if "UNIQUE constraint failed: accounts_user.wallet_address" in str(e):
                print(f"IntegrityError: {e}")
                return Response({"error": "This wallet address is already registered."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
