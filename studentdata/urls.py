from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # Подключение URL-ов приложения
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


