#-*- coding: utf-8 -*-
from django.forms import models

from portalufopa.models import Site, Sessao, Tag
from django.contrib.auth.models import User
from django import forms


class CreateSiteForm(models.ModelForm):
    
    class Meta:
        model = Site
        fields = (
            'url', 'titulo', 'descricao', 'logo', 'favicon', 'banner_topo',
            )
        labels = {
            'url' : 'Url do site',
            'titulo' : 'Titulo do site',
            'descricao' : 'Descrição sobre o site',
            'logo' : 'Logo, Brasão do Site',
            'favicon' : 'Icon do site',
            'banner-topo' : 'Banner de destaque na pagina principal',
            }
        
class EnderecoSiteForm(models.ModelForm):
    
    class Meta:
        model = Site
        fields = (
            'email', 'telefone', 'texto_rodape', 
            )
        labels = {
            'email' : 'E-Mail do site',
            'telefone' : 'Telefone de contato',
            'texto_rodape' : 'Endereço para correspondência'
            }
        
class RedesSociaisSiteForm(models.ModelForm):
    
    class Meta:
        model = Site
        fields = (
            'facebook_link', 'twitter_link', 'youtube_link', 'google_link', 'flicker_link', 'rss_link', 
            )
        labels = {
            'facebook_link' : 'Link para o facebook',
            'twitter_link' : 'Link para twitter',
            'google_link' : 'Link para o Google+',
            'flicker_link' : 'Link para o Flicker',
            'rss_link' : 'Link para rss',
            }
        
class DesenvolcedorSiteForm(models.ModelForm):
    
    class Meta:
        model = Site
        fields = (
            'facebook_cod', 'twitter_cod', 'youtube_cod', 'google_cod', 'flicker_cod', 
            )
        labels = {
            'facebook_cod' : 'Codigo JS facebook',
            'twitter_cod' : 'Codigo JS twitter',
            'youtube_cod' : 'Codigo JS YouTube',
            'google_cod' : 'Codigo JS Google+',
            'flicker_cod' : 'Codigo JS Flicker',
            }
        
class AnalyticSiteForm(models.ModelForm):
    
    class Meta:
        model = Site
        fields = (
            'analytic_cod', 
            )
        labels = {
            'analytic_cod' : 'Codigo JS do site de gestor de estatisticas',
            }

class SessaoForm(models.ModelForm):
    
    class Meta:
        model = Sessao
        fields = (
            'titulo', 'tipo', 'quantidade',
            )
        labels = {
            'titulo' : 'Título da sessão',
            'tipo' : 'Tipo de contéudo a ser apresentado',
            'quantidade' : 'Quantidade suportado',
            }
        
class TagForm(models.ModelForm):
    
    class Meta:
        model = Tag
        fields = (
            'titulo', 'imagem',
            )
        labels = {
            'titulo' : 'Título da tag',
            'imagem' : 'Selecione uma imagem vinculada a tag',
            }

class UserForm(models.ModelForm):
    pwd = forms.CharField(label='Senha.', max_length=32, widget=forms.PasswordInput)
    check_pwd = forms.CharField(label='Confirmar senha.',max_length=32, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'pwd',
            'check_pwd',
            )
        
        labels = {
            'fist_name':'Primeiro nome',
            'last_name':'Sobrenome',
            'username':'Username',
            'password':'Senha',
            'email':'E-mail',
        }
        
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        pwd = cleaned_data.get('pwd')
        check_pwd = cleaned_data.get('check_pwd')
        if not pwd==check_pwd:
            raise forms.ValidationError("Senha não confirma!")

