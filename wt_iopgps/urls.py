"""
URL configuration for acv_alarms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path("", views.home, name="home")
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path("", Home.as_view(), name="home")
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path("blog/", include("blog.urls"))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework.documentation import include_docs_urls

API_URL_BASE = "api/v1/"

urlpatterns = [
    path("api_generate_token/", views.obtain_auth_token),
    path("admin/", admin.site.urls),
    path("documentation/", include_docs_urls(title="Developer API documentation")),
    path(API_URL_BASE, include("alarms.urls")),
    path(API_URL_BASE, include("batteries.urls")),
    path(API_URL_BASE, include("devices.urls")),
    path(API_URL_BASE, include("users.urls")),
    path(API_URL_BASE, include("routes.urls")),
    path(API_URL_BASE, include("vehicles.urls")),
    path(API_URL_BASE, include("licenses.urls")),
    path(API_URL_BASE, include("movement_orders.urls")),
    path(API_URL_BASE, include("maintenance_manuals.urls")),
    path(API_URL_BASE, include("mileage.urls")),
    path(API_URL_BASE, include("statuses.urls")),
    path(API_URL_BASE, include("tires.urls")),
    path(API_URL_BASE, include("work_orders.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
