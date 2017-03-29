# -*- coding: utf-8 -*-

from django.conf.urls import url

from manage_main.views import new_or_edit_tag, permissao_content,\
    create_or_edit_user, create_or_edit_permissao

from .views import index, new_or_edit_site, open_site, new_or_edit_sessao
from portalufopa.models import ContentType
from manage_main.models import Papel


app_name = 'manage_main'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^(?P<url>[-\w]+)/$', open_site, name='open_site'),
    url(r'^new/site/$', new_or_edit_site, name='new_site'),
    url(r'^edit/(?P<url>\w+)/$', new_or_edit_site, name='edit_site'),
    url(r'^edit/(?P<url>\w+)/sessoes/$', new_or_edit_sessao, name='new_edit_sessao_site'),
    url(r'^edit/(?P<url>\w+)/tags/$', new_or_edit_tag, name='new_edit_tag_site'),
    url(r'^edit/(?P<url>\w+)/(?P<opcao>\w+)/$', new_or_edit_site, name='edit_site'),
    url(r'^edit/(?P<url>\w+)/sessoes/(?P<sessao>[-\w]+)/$', new_or_edit_sessao, name='new_edit_sessao_site'),
    url(r'^edit/(?P<url>\w+)/tags/(?P<tag>[-\w]+)/$', new_or_edit_tag, name='new_edit_tag_site'),
    url(r'^edit/(?P<url>\w+)/permissao/contents/$', permissao_content, name='permissao_content_site'),
    
    url(r'^(?P<url>\w+)/users/$', create_or_edit_user, name='create_edit_user'),
    url(r'^(?P<url>\w+)/groups/$', create_or_edit_permissao, name='create_edit_permissao'),
    ]

#Metodo de atualização da base dados executado uma unica vez.
def start():
    try:
        if ContentType.objects.count()==0:
            LISTA_CONTENTS = {'ATNoticia':'Noticia', 'ATPagina':'Pagina', 'ATPasta':'Pasta', 'ATArquivo':'Arquivo',
                          'ATEvento':'Evento', 'ATAgenda':'Agenda', 'ATImagem':'Imagem', 'ATBanner':'Banner',
                          'ATInforme':'Informe', 'ATLink':'Link'}
            for key, value in LISTA_CONTENTS.iteritems():
                content_type = ContentType(tipo=key, descricao=value)
                content_type.save()
        print 'Atualizando os tipos de contens, OK.\n'
    except:
        print 'Atualizando os tipos de contens, Error.\n'
    
    try:
        if Papel.objects.count() == 0:
            contents_type = ContentType.objects.all()
            LISTA_PAPEIS = {'create':'Criar', 'delete':'Apagar', 'update':'Atualizar', 'workflow':'Publicar'}
            for i in contents_type:
                for key, valor in LISTA_PAPEIS.iteritems():
                    papel = Papel(papel_name=valor, cod_name=key, content_type=i)
                    papel.save()
        print 'Atualizando os papeis dos contents, Ok.\n'
    except:
        print 'Atualizando os papeis dos contents, Error.\n'
        
start()