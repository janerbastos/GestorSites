# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import index, login


app_name = 'portais'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^login/$', login, name='login'),
    url(r'^(?P<url>\S+)/$', index, name='index'),
    ]