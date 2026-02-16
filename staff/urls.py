from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('approve/<int:user_id>/', views.approve_resident, name='approve_resident_staff'),
    path('update-tariffs/', views.update_tariffs, name='update_tariffs'),
    path('streets/', views.manage_streets, name='manage_streets'),
    path('edit-street/<int:street_id>/', views.edit_street, name='edit_street'),
    path('delete-street/<int:street_id>/', views.delete_street, name='delete_street'),
    path('readings/', views.all_readings, name='staff_readings'),
    path('voting/', views.voting_list, name='staff_voting'),
    path('manage/', views.manage_coop, name='staff_manage'),
    path('manage/edit/<int:membership_id>/', views.edit_member, name='staff_edit_member'),
    path('manage/delete/<int:membership_id>/', views.delete_member, name='staff_delete_member'),
    path('readings/add/<int:membership_id>/', views.add_reading, name='add_reading'),
    path('readings/edit/<int:reading_id>/', views.edit_reading, name='staff_edit_reading'),
    path('readings/find/', views.find_meter_by_number, name='find_meter_by_number'),
    path('delete-request/<int:user_id>/', views.delete_registration_request_staff, name='delete_registration_request_staff'),
    path('delete-all-requests/', views.delete_all_registration_requests, name='delete_all_registration_requests'),
]
