from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Додаємо це: стандартні шляхи для входу/виходу
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('meters.urls')),
]
