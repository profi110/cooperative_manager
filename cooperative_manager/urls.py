from django.contrib import admin
from django.urls import path, include
from cooperatives import views as coop_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('users.urls')),

    path('ajax/check-coop/', coop_views.check_coop_id, name='check_coop_id'),
    path(
        'register-coop/', coop_views.register_cooperative,
        name='register_coop'),
    path(
        'chairman/dashboard/', coop_views.chairman_dashboard,
        name='chairman_dashboard'),
    path('chairman/add-street/', coop_views.add_street, name='add_street'),
    path(
        'chairman/delete-street/<int:street_id>/', coop_views.delete_street,
        name='delete_street'),
    path(
        'chairman/approve/<int:user_id>/', coop_views.approve_resident,
        name='approve_resident'),
    ]
