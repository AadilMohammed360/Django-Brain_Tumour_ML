from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('BaseApp.urls')),  # Replace 'your_app_name' with the actual name of your Django app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Serve media files during development
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)