from django.contrib import admin
from django.urls import path, include
from users import views as user_views  # 👈 Імпорт юзерів
from cooperatives import views as coop_views  # 👈 Імпорт кооперативів

urlpatterns = [
    path('admin/', admin.site.urls),

    # Головна сторінка (порожній шлях '')
    path('', user_views.home, name='home'),

    # Заявка на кооператив
    path(
        'register-coop/', coop_views.register_cooperative,
        name='register_coop'),

    # Твої старі шляхи...
    path('users/', include('django.contrib.auth.urls')),
    path('register/', user_views.register, name='register'),
    # Якщо у тебе є функція register
    path('', include('meters.urls')),
    ]