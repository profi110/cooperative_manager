from django.urls import path
from . import views

urlpatterns = [
    # Це головна сторінка ('') -> вона викликає функцію dashboard
    path('', views.dashboard, name='dashboard'),
    path('submit/<int:meter_id>/', views.submit_reading, name='submit_reading'),
]