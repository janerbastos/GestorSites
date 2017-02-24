# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import datetime

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
    
    def __unicode__(self):
        return self.titulo
    
    def get_configure_url(self):
        return '/%s/configure/' % self.url
    
    def get_absolute_url(self):
        return '/%s/' % self.url
    
class PortalUrl(models.Model):
    url = models.SlugField(max_length=255)
    site = models.ForeignKey(Site)
    indice = models.PositiveIntegerField()
    
    def __unicode__(self):
        return self.url

class Sessao(models.Model):
    sessao = models.CharField('Identificador da sessão', max_length=150)
    titulo = models.CharField('Título da sessão', max_length=150)
    tipo = models.CharField('Tipo de conteúdo', max_length=15, choices=CHOOSE_TIPO_CONTENT, null=True, blank=True)
    quantidade = models.PositiveIntegerField('Quantidades exibidos', default=0)
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
    create_at = models.DateField('Data de criação', auto_now_add=True)
    update_at = models.DateField('Data de atualização', null=True, blank=True, default=None)
    public_at = models.DateField(null=True, blank=True, default=None)
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

class Noticia(Content):
    corpo_texto = models.TextField(default=None, null=True, blank=True)
    imagem = models.ImageField(upload_to=content_file_imagem, blank=True, default=None)
    legenda = models.CharField(max_length=255, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    
class Informe(Content):
    corpo_texto = models.TextField(default=None, null=True, blank=True)
    imagem = models.ImageField(upload_to=content_file_imagem, blank=True, default=None)
    legenda = models.CharField(max_length=255, blank=True, null=True)
    
class Link(Content):
    link = models.URLField(max_length=255)
    target = models.CharField(max_length=30, choices=CHOOSE_TARGTE)
    
class Imagem(Content):
    imagem = models.ImageField(upload_to=content_file_imagem)
    
class Banner(Content):
    imagem = models.ImageField(upload_to=content_file_imagem)
    link = models.URLField(max_length=255)
    target = models.CharField(max_length=30, choices=CHOOSE_TARGTE)

class Pasta(Content):
    visao_padrao = models.CharField(max_length=255, null=True, blank=True)

class Arquivo(Content):
    arquivo = models.FileField(upload_to=content_file_documento)
        
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

class Agenda(Content):
    data_at = models.DateTimeField(default=datetime.now())
    local = models.CharField(max_length=150)
    
'''def save_object(signal, instance, sender, **kwargs):
    if instance.id == None:
        pass

signals.pre_save.connect(save_object, sender=Pagina)
signals.pre_save.connect(save_object, sender=Noticia)
signals.pre_save.connect(save_object, sender=Link)
signals.pre_save.connect(save_object, sender=Imagem)
signals.pre_save.connect(save_object, sender=Banner)'''

