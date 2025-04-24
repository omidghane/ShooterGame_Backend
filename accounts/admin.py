from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    model = User

    list_display = ('username', 'wallet_address', 'is_staff', 'is_superuser', 'is_active', 'is_personnel', 'created_at')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_personnel')

    search_fields = ('username', 'wallet_address')
    ordering = ('-created_at',)

    fieldsets = (
        ('Authentication', {'fields': ('username', 'password')}),
        ('Wallet Info', {'fields': ('wallet_address',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'is_active', 'is_personnel')}),
        ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'wallet_address', 'password1', 'password2', 'is_staff', 'is_superuser', 'is_active', 'is_personnel'),
        }),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'employee_code')
    search_fields = ('user__username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('created_at', 'employee_code')
