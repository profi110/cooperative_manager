from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/check-duplicates/', views.check_duplicates_api, name='api_check_duplicates'),
    path('api/check-coop/', views.check_coop_id_api, name='check_coop_id'),
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    ]
