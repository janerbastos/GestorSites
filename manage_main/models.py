#-*- coding: utf-8 -*-

from django.db import models
from portalufopa.models import Site, ContentType
from django.contrib.auth.models import User

#UM UNICO USUÁRIO POR SITE
class UserSite(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    grupo = models.ManyToManyField('Grupo', related_name='user_grupos')
    
    class Meta:
        unique_together = (("user", "site"),)

class GrupoPapel(models.Model):
    grupo = models.ForeignKey('Grupo', related_name='grupos')
    papeis = models.ManyToManyField('Papel', related_name='grupo_papeis')
    
    def __unicode__(self):
        return self.grupo.grupo_nome

class Grupo(models.Model):
    grupo_name = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.grupo_nome

class Papel(models.Model):
    papel_name = models.CharField(max_length=50)
    cod_name = models.SlugField(max_length=50, null=True)
    content_type = models.ForeignKey(ContentType, related_name='content_papel', null=True)
    
    def __unicode__(self):
        return self.papel_name