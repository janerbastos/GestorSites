# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import _login, _logout


app_name = 'security'
urlpatterns = [
    url(r'^login/$', _login, name='login'),
    url(r'^logout/$', _logout, name='logout'),
    ]