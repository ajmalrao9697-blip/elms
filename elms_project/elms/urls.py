from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Admin branding
admin.site.site_header = "MARS BPO Admin"
admin.site.site_title = "MARS BPO Portal"
admin.site.index_title = "Welcome to MARS BPO"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('hr.urls', 'hr'), namespace='hr')),  # HR app routes
]

# Serve static & media in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
