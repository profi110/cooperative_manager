# staff/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('approve/<int:user_id>/', views.approve_resident, name='approve_resident_staff'),
    path('update-tariffs/', views.update_tariffs, name='update_tariffs'),
    path('add-street/', views.add_street, name='staff_add_street'),
    path('delete-street/<int:street_id>/', views.delete_street, name='staff_delete_street'),
    path('readings/', views.all_readings, name='staff_readings'),
]