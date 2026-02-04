from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('coops/', include('cooperatives.urls')),
    path('staff/', include('staff.urls')),
    path('meters/', include('meters.urls')),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
