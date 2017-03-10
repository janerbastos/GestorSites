# -*- coding: utf-8 -*-
from django.db.models import Q 
from django.forms import models

from .models import Arquivo, Evento, Agenda
from .models import Site, Pagina, Noticia, Link, Imagem, Banner, \
    Pasta, Informe
from portalufopa.models import Portlet, Tag
from django import forms


class SiteForm(models.ModelForm):
    
    class Meta:
        model = Site
        fields = (
            'url', 'titulo', 'descricao', 'logo', 'banner_topo', 'telefone', 'email', 'texto_rodape',
            )
        labels = {
            'url' : 'Url do site',
            'titulo' : 'Título do site',
            'descricao' : 'Descriçãp do site',
            'logo' : 'Logo do site',
            'banner_topo' : 'Banner de destaque',
            'telefone' : 'Telefone para contato',
            'email' : 'Email para contato',
            'texto_rodape' : 'Informações adicionais no rodapé do site.',
            }

class PaginaForm(models.ModelForm):
    class Meta:
        model = Pagina
        fields = (
            'titulo', 'descricao', 'corpo_texto', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título da página',
            'descricao' : 'Sumário da página',
            'corpo_texto' : 'Corpo da página',
            'sessao' : 'Sessão da página',
            'excluir_nav' : 'Excluir da navagação',
            }

class NoticiaForm(models.ModelForm):
    
    def __init__(self, site, *args, **kwargs):
        super(NoticiaForm, self).__init__(*args, **kwargs)
        query_set_tags = Tag.objects.filter(site__url=site)
        self.fields['tag'] = forms.CharField(label='Tags.', required=False, widget=forms.Select(choices=[('', '')]+[(o.tag, o.titulo) for o in query_set_tags]))
        
    class Meta:
        model = Noticia
        fields = (
            'titulo', 'descricao', 'corpo_texto', 'imagem', 'legenda', 'tag', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título da notícia',
            'descricao' : 'Sumário da notícia',
            'corpo_texto' : 'Corpo da notícia',
            'imagem' : 'Imagem da notícia',
            'legenda' : 'Legenda da imagem',
            'excluir_nav' : 'Excluir da navagação',
            }
        
class InformeForm(models.ModelForm):
       
    class Meta:
        model = Informe
        fields = (
            'titulo', 'descricao', 'corpo_texto', 'imagem', 'legenda', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título do informe',
            'descricao' : 'Sumário da informe',
            'corpo_texto' : 'Corpo do informe',
            'imagem' : 'Imagem do informe',
            'legenda' : 'Legenda da imagem',
            'excluir_nav' : 'Excluir da navagação',
            }

class LinkForm(models.ModelForm):
        
    class Meta:
        model = Link
        fields = (
            'titulo', 'descricao', 'link', 'target', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título do link',
            'descricao' : 'Sumário do link',
            'link' : 'Endereço para direcionamento',
            'target' : 'Opções de link',
            'excluir_nav' : 'Excluir da navagação',
            }
        
class ImagemForm(models.ModelForm):
        
    class Meta:
        model = Imagem
        fields = (
            'titulo', 'descricao', 'imagem', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título do imagem',
            'descricao' : 'Sumário da imagem',
            'imagem' : 'Selecione o arquivo de imagem',
            'excluir_nav' : 'Excluir da navagação',
            }

class ArquivoForm(models.ModelForm):
        
    class Meta:
        model = Arquivo
        fields = (
            'titulo', 'descricao', 'arquivo', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título do arquivo',
            'descricao' : 'Sumário da arquivo',
            'arquivo' : 'Selecione um arquivo para submissão',
            'excluir_nav' : 'Excluir da navagação',
            }

class BannerForm(models.ModelForm):
        
    class Meta:
        model = Banner
        fields = (
            'titulo', 'descricao', 'imagem', 'link', 'target', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título do banner',
            'descricao' : 'Sumário do banner',
            'imagem' : 'Selecione o arquivo de imagem',
            'link' : 'Endereço do link para direcionamento',
            'target' : 'Opções do link',
            'excluir_nav' : 'Excluir da navagação',
            }

class PastaForm(models.ModelForm):
        
    class Meta:
        model = Pasta
        fields = (
            'titulo', 'descricao', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título do pasta',
            'descricao' : 'Sumário da pasta',
            'excluir_nav' : 'Excluir da navagação',
            }

class EventoForm(models.ModelForm):
    
        class Meta:
            model = Evento
            fields = (
                'titulo', 'descricao', 'local', 'inicio_at' , 'termino_at',
                'corpo_texto', 'participante', 'url_evento', 'contato', 'email',
                'telefone_contato', 'excluir_nav',
                )
            labels = {
                'titulo' : 'Título do evento',
                'descricao' : 'Sumário da evento',
                'local' : 'Local do evento',
                'inicio_at' : 'Início do evento',
                'termino_at' : 'Termino do evento',
                'corpo_texto' : 'Texto do corpo do evento',
                'participante' : 'Participantes',
                'url_evento' : 'URL do evento',
                'contato' : 'Nome do contato',
                'email' : 'E-Mail de contato',
                'telefone_contato' : 'Telefone de contato',
                'excluir_nav' : 'Excluir da navagação',
                }
            
            widgets = {
            }
            
class AgendaForm(models.ModelForm):
    
    class Meta:
        model = Agenda
        fields = (
            'titulo', 'descricao', 'data_at', 'local', 'excluir_nav'
            )
        labels = {
            'titulo' : 'Título do agenda',
            'descricao' : 'Sumário da Agenda',
            'data_at' : 'Data da programação',
            'local' : 'Local do programação',
            'excluir_nav' : 'Excluir da navagação',
            }
        
class PortletForm(models.ModelForm):
    
    class Meta:
        model = Portlet
        fields = (
            'titulo', 'quantidade'
            )
        labels = {
            'titulo' : 'Titulo do portlet',
            'quantidade' : 'Quantidade a ser exibido',
            }

class PortletDestaqueForm(models.ModelForm):
    
    class Meta:
        model = Portlet
        fields = (
            'titulo', 'tipo', 'quantidade'
            )
        labels = {
            'titulo' : 'Titulo do portlet',
            'tipo' : 'Tipo de contúdo',
            'quantidade' : 'Quantidade a ser exibido',
            }