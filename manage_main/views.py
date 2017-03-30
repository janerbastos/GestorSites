# -*- coding: utf-8 -*-

from django.http.response import Http404
from django.shortcuts import render, redirect
from django.utils.text import slugify

from manage_main.forms import CreateSiteForm, EnderecoSiteForm, \
    RedesSociaisSiteForm, DesenvolcedorSiteForm, AnalyticSiteForm, SessaoForm, \
    TagForm, UserForm, UserEditForm, GrupoForm
from portalufopa.models import Site, Sessao, Tag, ContentType
from django.contrib.auth.models import User
from manage_main.models import UserSite, Grupo, GrupoPapel


# Create your views here.
TEMPLATE = 'manage/%s.html'

def __excluir_sessao(request, url, sessao):
      
    sessao.delete()
    return redirect('manage_main:new_edit_sessao_site', url=url )

def __excluir_tag(request, url, tag):
      
    tag.delete()
    return redirect('manage_main:new_edit_tag_site', url=url )

def index(request):
    template = TEMPLATE % 'index'
    _list_site = Site.objects.all()
    
    context = {
        'list_sites' : _list_site
        }
    return render(request, template, context)

def open_site(request, url):
    
    if 'action' in request.GET:
        _action = request.GET['action']
        if _action == 'excluir':
            _object_site = Site.objects.get(url=url)
            _object_site.delete()
            return redirect('/manage_main')
    
    template = TEMPLATE % 'open_site'
    _object_site = Site.objects.get(url=url)
    action = 'open'
    context = {
        'site' : _object_site,
        'action' : action
        }
    return render(request, template, context)

def new_or_edit_site(request, url=None, opcao=None):
    
    try:
        _object_site = Site.objects.get(url=url)
        action = 'edit'
    except Site.DoesNotExist:
        action = 'new'
        _object_site = Site()
        
    form = None
    
    template = TEMPLATE % 'create_site_form'
    if not opcao:
        form = CreateSiteForm(request.POST or None, request.FILES or None, instance=_object_site)
    else : 
        action += '_'+opcao
    if opcao == 'endereco':
        form = EnderecoSiteForm(request.POST or None, instance=_object_site)
    if opcao == 'redes_sociais':
        form = RedesSociaisSiteForm(request.POST or None, instance=_object_site)
    if opcao == 'desenvolvedor':
        form = DesenvolcedorSiteForm(request.POST or None, instance=_object_site)
    if opcao == 'estatistica':
        form = AnalyticSiteForm(request.POST or None, instance=_object_site)
        
    if form.is_valid():
        model = form.save(commit=False)
        
        if not opcao:
            if 'logo' in request.FILES:
                model.logo = request.FILES['logo']
                
            if 'favicon' in request.FILES:
                model.favicon = request.FILES['favicon']
            
            if 'banner_topo' in request.FILES:
                model.banner_topo = request.FILES['banner_topo']
        
        model.save()
        
        #Adiciona por padrão todos os Tipos de contents para o site
        if not opcao:
            content_types = ContentType.objects.all().values_list('id', flat=True)
            model.content_type_permissao.add(*content_types)
            model.save()
        
        _url = model.url
        
        if action == 'new' : 
            return redirect('/%s' % _url)
        else:
            return redirect('manage_main:open_site', url=model.url)
    
    context = {
        'form' : form,
        'site' : _object_site,
        'action' : action
        }
    
    return render(request, template, context)

def new_or_edit_sessao(request, url, sessao=None,):
    try:
        _object_site = Site.objects.get(url=url)
        _object_sessao = Sessao.objects.filter(site=_object_site).get(sessao=sessao)
    except Site.DoesNotExist:
        raise Http404('Site não localizado')
    except Sessao.DoesNotExist:
        _object_sessao = Sessao()
    
    
    if 'action' in request.GET:
        if request.GET['action'] == 'excluir':
            return __excluir_sessao(request, url, _object_sessao)
    
    action = 'edit_sessao'
        
    _list_objects = Sessao.objects.filter(site=_object_site)
    
    form = SessaoForm(request.POST or None, instance=_object_sessao)
    
    if form.is_valid():
        model = form.save(commit=False)
        #if not model.id:
        model.sessao = slugify(model.titulo)
        model.site = _object_site
        model.save()
        return redirect('manage_main:new_edit_sessao_site', url=_object_site.url, )
    template = TEMPLATE % 'create_or_edit_sessao_site_form'
    
    context = {
        'site' : _object_site,
        'lista_sessoes' : _list_objects,
        'action' : action,
        'form' : form,
        }
    
    return render(request, template, context)

def new_or_edit_tag(request, url, tag=None):
    try:
        _object_site = Site.objects.get(url=url)
        _object_tag = Tag.objects.filter(site=_object_site).get(tag=tag)
    except Site.DoesNotExist:
        raise Http404('Site não localizado')
    except Tag.DoesNotExist:
        _object_tag = Tag()
    
    if 'action' in request.GET:
        if request.GET['action'] == 'excluir':
            return __excluir_tag(request, url, _object_tag)
    
    action = 'edit_tag'
        
    _list_objects = Tag.objects.filter(site=_object_site)
    
    form = TagForm(request.POST or None, request.FILES or None, instance=_object_tag)
    
    if form.is_valid():
        model = form.save(commit=False)
        #if not model.id:
        model.tag = slugify(model.titulo)
        model.site = _object_site
        
        if 'imagem' in request.FILES:
            model.imagem = request.FILES['imagem']
        
        model.save()
        return redirect('manage_main:new_edit_tag_site', url=_object_site.url, )
    
    template = TEMPLATE % 'create_or_edit_tag_site_form'
    
    context = {
        'site' : _object_site,
        'lista_tags' : _list_objects,
        'action' : action,
        'form' : form,
        }
    
    return render(request, template, context)

def permissao_content(request, url):
    template = TEMPLATE % 'permissao_content'
    _object_site = Site.objects.get(url=url)
    _contents = ContentType.objects.all()
    _itens = _object_site.content_type_permissao.values_list('id', flat=True)
    _contents = _contents.exclude(id__in = _itens)
    
    if request.GET:
        _item = request.GET['remover']
        _object_site.content_type_permissao.remove(_item)
        return redirect(request.path)
        
    
    if request.POST:
        _list=request.POST.getlist('content')
        for i in _list:
            _object_site.content_type_permissao.add(i)
        return redirect(request.path)
    
    context = {
        'site' : _object_site,
        'contents' : _object_site.content_type_permissao.all(),
        'action' : 'contents',
        'lista_contents' : _contents,
        }
    return render(request, template, context)

def create_or_edit_user(request, url):
    template = TEMPLATE % 'create_or_edit_usuario_form'
    _user = None
    form  = None
    _object_site = Site.objects.get(url=url)
    
    action = False
    if 'edit' in request.GET:
        action = True
        _user = User.objects.get(username=request.GET['edit'])
        form = UserEditForm(request.POST or None, instance=_user)
        
    if 'new' in request.GET:
        action = True
        form = UserForm(request.POST or None, instance=_user)
        
    if 'bloquear' in request.GET:
        _user = User.objects.get(username=request.GET['bloquear'])
        _user.is_active = False
        _user.save()
        return redirect(request.path)
    
    if 'desbloquear' in request.GET:
        _user = User.objects.get(username=request.GET['desbloquear'])
        _user.is_active = True
        _user.save()
        return redirect(request.path)
    
    if 'vincular' in request.GET:
        _list=request.POST.getlist('content_users')
        for uid in _list:
            _user = User.objects.get(id=uid)
            user_site = UserSite(user=_user, site=_object_site)
            user_site.save()
        return redirect(request.path)
    
    if 'desvincular' in request.GET:
        username = request.GET['desvincular']
        user = UserSite.objects.filter(site=_object_site).get(user__username=username)
        user.delete()
        return redirect(request.path)
        
    
    if action:
        if form.is_valid():
            model = form.save(commit=False)
            if 'new' in request.GET:
                model.set_password(request.POST.get('pwd'))
            model.save()
            return redirect(request.path)
    
    _users = UserSite.objects.filter(site=_object_site)
    context = {
        'site' : _object_site,
        'form' : form,
        'action' : 'users',
        'users' : _users,
        'operacao' : action,
        }
    return render(request, template, context)

def create_or_edit_permissao(request, url):
    _grupos = Grupo.objects.all()
    _grupo = None
    _form = None
    _object_site = Site.objects.get(url=url)
    _grupo_papeis = None
    
    action = False
    if 'edit' in request.GET:
        action = True
        _grupo = Grupo.objects.get(grupo_name=request.GET['edit'])
        _form = GrupoForm(request.POST or None, instance=_grupo)
    
    if 'new' in request.GET:
        action = True
        _form = GrupoForm(request.POST or None, instance=_grupo)
        
    if 'delete' in request.GET:
        action = True
        _grupo = Grupo.objects.get(grupo_name=request.GET['delete'])
        _grupo.delete()
        return redirect(request.path)
    
    if 'vincular' in request.GET:
        _grupo_name = request.GET['vincular']
        _list=request.POST.getlist('content_permissao')
        _grupo = Grupo.objects.get(grupo_name=_grupo_name)
        try:
            _grupo_papeis = GrupoPapel.objects.get(grupo=_grupo) 
        except:
            _grupo_papeis = GrupoPapel(grupo=_grupo)
            _grupo_papeis.save()
        for gid in _list:
            _grupo_papeis.papeis.add(gid)
        return redirect(request.path)
    
    if 'permissao' in request.GET:
        _grupo = Grupo.objects.get(grupo_name=request.GET['permissao'])
        try:
            _grupo_papeis = GrupoPapel.objects.get(grupo=_grupo)
        except:
            _grupo_papeis = GrupoPapel()
    
    if 'desvincular_permissao' in request.GET:
        gp = request.GET['desvincular_permissao'].split('_')
        _grupo_papeis = GrupoPapel.objects.get(grupo__id=gp[0])
        _grupo_papeis.papeis.remove(gp[1])
        return redirect("%s?permissao=%s" % (request.path, _grupo_papeis.grupo.grupo_name))
    
    if action:
        if _form.is_valid():
            model = _form.save(commit=False)
            model.save()
            return redirect(request.path)
    
    template = TEMPLATE % 'create_or_edit_permissao_form'
    
    context = {
        'site' : _object_site,
        'grupos' : _grupos,
        'form' : _form,
        'grupo' : _grupo,
        'action' : 'groups',
        'operacao' : action,
        'grupo_papeis' : _grupo_papeis
        }
    return render(request, template, context)  