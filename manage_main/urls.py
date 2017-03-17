# -*- coding: utf-8 -*-

from django.conf.urls import url

from manage_main.views import new_or_edit_tag, permissao_content

from .views import index, new_or_edit_site, open_site, new_or_edit_sessao


app_name = 'manage_main'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<url>[-\w]+)/$', open_site, name='open_site'),
    url(r'^new/site/$', new_or_edit_site, name='new_site'),
    url(r'^edit/site/(?P<url>\w+)/$', new_or_edit_site, name='edit_site'),
    url(r'^edit/site/(?P<url>\w+)/sessoes/$', new_or_edit_sessao, name='new_edit_sessao_site'),
    url(r'^edit/site/(?P<url>\w+)/tags/$', new_or_edit_tag, name='new_edit_tag_site'),
    url(r'^edit/site/(?P<url>\w+)/(?P<opcao>\w+)/$', new_or_edit_site, name='edit_site'),
    url(r'^edit/site/(?P<url>\w+)/sessoes/(?P<sessao>[-\w]+)/$', new_or_edit_sessao, name='new_edit_sessao_site'),
    url(r'^edit/site/(?P<url>\w+)/tags/(?P<tag>[-\w]+)/$', new_or_edit_tag, name='new_edit_tag_site'),
    url(r'^edit/site/(?P<url>\w+)/permissao/contents/$', permissao_content, name='permissao_content_site'),
    ]