# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from .comum.imagem import content_file_documento
from .comum.imagem import content_file_imagem, content_file_imagem_site


# Create your models here.
CHOOSE_TARGTE = (
        ('_blank', 'Abrir em nova janela'),
        ('_top', 'Abrir na mesma janela'),
    )

CHOOSE_WORKFLOW = (
        ('Privado', 'Privado'),
        ('Publicado', 'Publicado'),
    )

CHOOSE_STATUS = (
        (False, 'Site Bloqueado'),
        (True, 'Site Ativo'),
    )

CHOOSE_TIPO_CONTENT = (
        ('', 'Informe um tipo de conteúdo'),
        ('ATPagina', 'Páginas'),
        ('ATNoticia', 'Notícias'),
        ('ATInforme', 'Informes'),
        ('ATLink', 'Links'),
        ('ATImagem', 'Imagens'),
        ('ATBanner', 'Banners'),
        ('ATEvento', 'Eventos'),
        ('ATAgenda', 'Agendas'),
        ('ATArquivo', 'Arquivo'),
    )

CHOOSE_TIPO_CONTENT_PORTLET = (
        ('', 'Informe um tipo de conteúdo'),
        ('ATPagina', 'Páginas'),
        ('ATLink', 'Links'),
        ('ATImagem', 'Imagens'),
        ('ATBanner', 'Banners'),
        ('ATArquivo', 'Arquivo'),
        )

CHOOSE_LAYOUT = (
        ('', 'Padrão'),
        ('layout_01', 'Sem Título'),
        ('layout_02', 'Destaque'),
    )
    
class Site(models.Model):
    url = models.SlugField(max_length=150, unique=True)
    titulo = models.CharField('Título', max_length=150)
    descricao = models.TextField('Breve descrição', default=None, null=True, blank=True)
    create_at = models.DateField('Data de criação', auto_now_add=True)
    update_at = models.DateField('Data de atualização', null=True, blank=True, default=None)
    status = models.BooleanField(default=False, choices=CHOOSE_STATUS)
    facebook_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    twitter_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    youtube_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    google_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    flicker_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    rss_link = models.URLField(max_length=255, null=True, blank=True, default=None)
    logo = models.ImageField('Logo do site', upload_to=content_file_imagem_site, blank=True, null=True, default=None)
    banner_topo = models.ImageField('Banner de destaque', upload_to=content_file_imagem_site, blank=True, null=True, default=None)
    favicon = models.ImageField('Favicon', upload_to=content_file_imagem_site, blank=True, null=True, default=None)
    texto_rodape = models.TextField(default=None, blank=True, null=True)
    facebook_cod = models.TextField(null=True, blank=True, default=None)
    twitter_cod = models.TextField(null=True, blank=True, default=None)
    youtube_cod = models.TextField(null=True, blank=True, default=None)
    google_cod = models.TextField(null=True, blank=True, default=None)
    flicker_cod = models.TextField(null=True, blank=True, default=None)
    analytic_cod = models.TextField(null=True, blank=True, default=None)
    email = models.EmailField(max_length=255, null=True, blank=True, default=None)
    telefone = models.CharField(max_length=255, null=True, blank=True, default=None)
    workflow = models.CharField(max_length=20, default='Privado', choices=CHOOSE_WORKFLOW)
    content_type_permissao = models.ManyToManyField('ContentType', related_name='list_permissao_tipo',)
    
    def __unicode__(self):
        return self.titulo
    
    def get_configure_url(self):
        return '/%s/configure/' % self.url
    
    def get_absolute_url(self):
        return '/%s/' % self.url

class ContentType(models.Model):
    tipo = models.CharField(max_length=20, choices=CHOOSE_TIPO_CONTENT, unique=True)
    descricao = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.descricao
    

class PortalUrl(models.Model):
    url = models.SlugField(max_length=255)
    site = models.ForeignKey(Site)
    indice = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.url

class Portlet(models.Model):
    portlet = models.CharField(max_length=150)
    tipo = models.CharField(max_length=15, choices=CHOOSE_TIPO_CONTENT_PORTLET, null=True, blank=True)
    titulo = models.CharField(max_length=150)
    quantidade = models.PositiveIntegerField(default=0)
    conteudo = models.ManyToManyField('PortalCatalog', related_name='lista_portlets')
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    layout = models.CharField(max_length=30, null=True, blank=True, choices=CHOOSE_LAYOUT)
    ordem = models.PositiveIntegerField(default=0)
    posicao = models.CharField(max_length=10, default='rigth')
    categoria = models.CharField(max_length=20, default='content')
    origem = models.CharField(max_length=20, default='dafault')
    
    def __unicode__(self):
        return self.titulo

class Sessao(models.Model):
    sessao = models.CharField(max_length=150)
    titulo = models.CharField(max_length=150)
    tipo = models.CharField(max_length=15, choices=CHOOSE_TIPO_CONTENT, null=True, blank=True)
    quantidade = models.PositiveIntegerField(default=0)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    conteudo = models.ManyToManyField('PortalCatalog', related_name='lista_conteudos')
    
    def __unicode__(self):
        return self.titulo

class Tag(models.Model):
    tag = models.SlugField(max_length=150)
    titulo = models.CharField(max_length=150)
    imagem = models.ImageField(upload_to=content_file_imagem)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)

class Content(models.Model):
    url = models.SlugField(max_length=150)
    titulo = models.CharField(max_length=150)
    descricao = models.TextField(default=None, null=True, blank=True)
    create_at = models.DateTimeField('Data de criação', auto_now_add=True)
    update_at = models.DateTimeField('Data de atualização', null=True, blank=True, default=None)
    public_at = models.DateTimeField(null=True, blank=True, default=None)
    workflow = models.CharField(max_length=20, default='Privado', choices=CHOOSE_WORKFLOW)
    tipo = models.CharField(max_length=20)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    excluir_nav = models.BooleanField(default=False)
    dono = models.ForeignKey(User, null=True, blank=True)
    
    class Meta:
        abstract = True
        ordering = ['titulo']
    
    def __unicode__(self):
        return self.titulo
    
    def get_absolute_url(self):
        pass
    
class PortalCatalog(Content):
    path_url = models.CharField(max_length=255, null=True, blank=True)
    ordenador = models.PositiveIntegerField(null=True)
    
    def get_content_object(self):
        _object = None
        if self.tipo == 'ATPagina':
            _object = Pagina.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATLink':
            _object = Link.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATPasta':
            _object = Pasta.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATImagem':
            _object = Imagem.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATNoticia':
            _object = Noticia.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATBanner':
            _object = Banner.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATInforme':
            _object = Informe.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATAgenda':
            _object = Agenda.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATEvento':
            _object = Evento.objects.filter(site = self.site).get(url=self.url)
        if self.tipo == 'ATArquivo':
            _object = Arquivo.objects.filter(site = self.site).get(url=self.url)
        return _object

class Pagina(Content):
    corpo_texto = models.TextField(default=None, null=True, blank=True)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_pagina')

class Noticia(Content):
    corpo_texto = models.TextField(default=None, null=True, blank=True)
    imagem = models.ImageField(upload_to=content_file_imagem, blank=True, default=None)
    legenda = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_noticia')
    
class Informe(Content):
    corpo_texto = models.TextField(default=None, null=True, blank=True)
    imagem = models.ImageField(upload_to=content_file_imagem, blank=True, default=None)
    legenda = models.CharField(max_length=255, blank=True, null=True)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_informe')
    
class Link(Content):
    link = models.URLField(max_length=255)
    target = models.CharField(max_length=30, choices=CHOOSE_TARGTE)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_link')
    
class Imagem(Content):
    imagem = models.ImageField(upload_to=content_file_imagem)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_imagem')
    
class Banner(Content):
    imagem = models.ImageField(upload_to=content_file_imagem)
    link = models.URLField(max_length=255)
    target = models.CharField(max_length=30, choices=CHOOSE_TARGTE)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_banner')

class Pasta(Content):
    visao_padrao = models.CharField(max_length=255, null=True, blank=True)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_pasta')

class Arquivo(Content):
    arquivo = models.FileField(upload_to=content_file_documento)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_arquivo')
        
class Evento(Content):
    local = models.CharField(max_length=150, null=True, blank=True, )
    inicio_at = models.DateTimeField()
    termino_at = models.DateTimeField()
    corpo_texto = models.TextField(null=True, blank=True, )
    participante = models.TextField(null=True, blank=True, )
    url_evento = models.URLField(null=True, blank=True, )
    contato = models.CharField(null=True, blank=True, max_length=150)
    email = models.EmailField(blank=True, null=True)
    telefone_contato = models.CharField(max_length=150, blank=True, null=True)
    portlet = models.ManyToManyField('Portlet', related_name='portlet_evento')

class Agenda(Content):
    data_at = models.DateTimeField()
    local = models.CharField(max_length=150)
    portlet = models.ManyToManyField('PortalCatalog', related_name='portlet_agenda')



