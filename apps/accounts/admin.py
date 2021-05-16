from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.accounts.models import Profile, CustomUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Профиль"""
    list_display = ("user", "first_name")


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {'fields': (
                'email', 'first_name', 'last_name', 'username',
            )}
        ),
        (
            'Password', {'fields': ('password',)}
        ),
        (
            'Permissions',
            {'fields': (
                'is_staff', 'is_active', 'is_superuser', 'groups',
                'user_permissions'
            )}
        ),
    )
    add_fieldsets = (
        (
            None,
            {'fields': ('email', 'first_name', 'last_name', 'password1',
                        'password2')}
        ),
        (
            'Permissions',
            {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}
        ),
    )
    list_display = ('id', 'username',)
    ordering = ('id',)
