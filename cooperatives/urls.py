from django.urls import path
from . import views

urlpatterns = [
    path('ajax/check-coop/', views.check_coop_id, name='check_coop_id'),
]
