from django.contrib import admin
from django.urls import path, include
from users import views as user_views
# 👇 Додайте цей імпорт, якщо його немає!
from cooperatives import views as coop_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('dashboard/', user_views.dashboard, name='user_dashboard'),
    path('register-coop/', coop_views.register_cooperative,name='register_coop'),

    path('users/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
    path('meters/', include('meters.urls')),
    ]
