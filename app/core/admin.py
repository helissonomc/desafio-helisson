from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models
from django.contrib.auth.models import Group
from .forms import GroupAdminForm
from django.contrib.auth import get_user_model
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    def group(self, user):
        groups = []
        for group in user.groups.all():
            groups.append(group.name)
        return ' '.join(groups)
    group.short_description = 'Groups'

    list_display = ['email', 'group']

    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password',
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
            'fields':('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)

admin.site.unregister(Group)

# Create a new Group admin.
class GroupAdmin(admin.ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.
admin.site.register(Group, GroupAdmin)

admin.site.register(models.Demanda)