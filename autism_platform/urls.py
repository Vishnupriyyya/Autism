"""
URL configuration for Autism Learning and Skill Development Platform.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("children/", include("children.urls")),
    path("learning/", include("learning.urls")),
    path("recommendations/", include("recommendations.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
