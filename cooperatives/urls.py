# cooperatives/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Цей маршрут потрібен для Fetch-запиту під час реєстрації мешканців
    path('ajax/check-coop/', views.check_coop_id, name='check_coop_id'),
]