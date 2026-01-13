from django.contrib import admin
from .models import Cooperative, Street, Membership

@admin.register(Cooperative)
class CooperativeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'inn')
    readonly_fields = ('id',)
    fields = ('id', 'title', 'inn')

@admin.register(Street)
class StreetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cooperative')

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('user', 'cooperative', 'role')
