from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'user_type']

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
            ),
        }),
    
        (_('Personal Info'),{
            'fields':(
                'user_type',
            ),
        }),

        ( _('permissions'),{
            'fields':(
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),

        ( _('important dates'),{
            'fields':(
                'last_login',
            )
        })

    )
    
    add_fieldsets = (
        (None, {
            'classes':('wide',),
            'fields':('email', 'user_type', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)