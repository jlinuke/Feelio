"""
Feelio Root URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Public landing
    path('', include('dashboard.urls')),

    # Auth
    path('', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),

    # App modules
    path('tracker/', include('tracker.urls')),
    path('community/', include('community.urls')),
    path('resources/', include('resources.urls')),

    # Internationalisation
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
