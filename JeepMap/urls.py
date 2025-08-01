"""
URL configuration for JeepMap project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('dashboard/', accounts_views.home, name='home'), 
    path('', accounts_views.home, name='root'),
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin-master/', include('adminMaster.urls')),
    path('crew-master/', include('crewMaster.urls')),
    path('schedule-master/', include('scheduleMaster.urls')),
    path('vehicle-master/', include('vehicleMaster.urls')),
    path('route-master/', include('routeMaster.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
