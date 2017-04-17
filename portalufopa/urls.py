# -*- coding: utf-8 -*-

from django.conf.urls import url

from .views import index


app_name = 'portais'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<url>\S+)/$', index, name='index'),
    ]