from django.contrib import admin
from user_app.models import UserProfileInfo, CustomUser
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser')



# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(CustomUser, CustomUserAdmin)