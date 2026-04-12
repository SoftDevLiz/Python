"""
Root URL configuration for the News Application.

URL structure:
  /                     – public-facing news views (news app)
  /api/                 – REST API (news app)
  /admin/               – Django admin
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # All web (HTML) and API routes live inside the news app
    path('', include('news.urls')),
]
