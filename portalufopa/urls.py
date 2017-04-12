# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import index, _login, _logout


app_name = 'portais'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^security/login/$', _login, name='login'),
    url(r'^security/logout/$', _logout, name='logout'),
    url(r'^(?P<url>\S+)/$', index, name='index'),
    ]