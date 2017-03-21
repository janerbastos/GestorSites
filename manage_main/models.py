#-*- coding: utf-8 -*-

from django.db import models
from portalufopa.models import Site
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
    site = models.ForeignKey(Site)
    grupo_name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.grupo_nome

class Papel(models.Model):
    papel_name = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.papel_name