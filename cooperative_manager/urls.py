from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('coops/', include('cooperatives.urls')),
    path('staff/', include('staff.urls')), # Новий рядок
    path('meters/', include('meters.urls')),
]