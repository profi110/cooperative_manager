from django.contrib import admin
from .models import Cooperative, Membership, Street

admin.site.register(Cooperative)
admin.site.register(Membership)
admin.site.register(Street)