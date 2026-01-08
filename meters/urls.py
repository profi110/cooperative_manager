from django.urls import path
from . import views

urlpatterns = [
      path('submit/<int:meter_id>/', views.submit_reading, name='submit_reading'),
]