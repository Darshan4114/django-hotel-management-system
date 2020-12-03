from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .forms import CustomUserCreationForm, CustomUserChangeForm   
from .models import CustomUser, Profile
from django.utils.translation import ugettext_lazy as _


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    ordering = ('email',)
    add_form = CustomUserCreationForm #CHANGIT
    form = CustomUserChangeForm #CHANGIT
    list_display = ( 'email', 'first_name', 'last_name', 'is_staff')
    # list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # search_fields = ('first_name', 'last_name', 'email')
    fieldsets = (
        (None, {'fields': ('email','password',)}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2',)}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
