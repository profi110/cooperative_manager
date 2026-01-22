# meters/urls.py
from django.urls import path  # ЦЬОГО РЯДКА НЕ ВИСТАЧАЛО
from . import views

urlpatterns = [
    path('submit/', views.submit_reading, name='submit_reading'),
]