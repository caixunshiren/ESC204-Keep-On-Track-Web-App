# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('dashboard/', views.index, name='home'),
    path('data/', views.data, name='data'),
    path('delete/<int:id>/', views.track_delete, name='delete'),
    path('refresh/', views.refresh, name='refresh'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
