from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Мы используем UserAdmin, чтобы интерфейс выглядел красиво
# (как стандартное управление пользователями в Django)
admin.site.register(CustomUser, UserAdmin)