"""Report URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from top import views
from django.conf.urls import include
from django.views.generic.base import RedirectView
from django.urls import re_path
from top.views import base
from django.views.generic import TemplateView
from Report.settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static
from Report import settings
from django.views.static import serve

urlpatterns = [
    path('main', views.mainworker,name = 'main'),
    re_path(r'^admin/*', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts', include('django.contrib.auth.urls')),
    re_path(r'^base', views.base, name='base'),
    re_path(r'^closing', views.closing, name='closing'),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^.*$', RedirectView.as_view(url='main')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

