# -*- coding: utf-8 -*-

import json

from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template.exceptions import TemplateDoesNotExist
from django.db.models import Q

from .comum.utils import get_content_by_portal_catalog

from .comum import agendas
from .comum import paginas, pastas, noticias, imagens, links, banners, arquivos, informes, eventos
from .models import PortalCatalog, Pasta, Sessao
from .comum.contents import reescrever_url, get_url_id_content, get_site_url_id,\
    TYPE_NAME, WORKFLOW_ACTION, WORKFLOW
from portalufopa.comum.contents import fraguiment_url
from portalufopa.comum import portlets
from portalufopa.models import Imagem
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.
@login_required(login_url='/security/login/')
def __workflowObject(request):
    _site_url = get_site_url_id(request)
    
    _p = PortalCatalog.objects.filter(site__url=_site_url)
    _url = reescrever_url(request)
    _workflow = request.GET['workflow_action']
    if _workflow in WORKFLOW_ACTION:
        
        _p = _p.get(path_url=_url)
        
        if _p.tipo == 'ATPagina':
            paginas.workflow(request, _p, WORKFLOW[_workflow])
            
        if _p.tipo == 'ATLink':
            links.workflow(request, _p, WORKFLOW[_workflow])
            
        if _p.tipo == 'ATImagem':
            imagens.workflow(request, _p, WORKFLOW[_workflow])
        
        if _p.tipo == 'ATPasta':
            pastas.workflow(request, _p, WORKFLOW[_workflow])
            
        if _p.tipo == 'ATBanner':
            banners.workflow(request, _p, WORKFLOW[_workflow])
            
        if _p.tipo == 'ATNoticia':
            noticias.workflow(request, _p, WORKFLOW[_workflow])
            
        if _p.tipo == 'ATArquivo':
            arquivos.workflow(request, _p, WORKFLOW[_workflow])
        
        if _p.tipo == 'ATEvento':
            eventos.workflow(request, _p, WORKFLOW[_workflow])
            
        if _p.tipo == 'ATAgenda':
            agendas.workflow(request, _p, WORKFLOW[_workflow])
        
        if _p.tipo == 'ATInforme':
            informes.workflow(request, _p, WORKFLOW[_workflow])
            
    else:
        raise Http404('Operação não permitida.')
    
    return redirect(_url)

@login_required(login_url='/security/login/')
def __createObject(request):
    request.session['action'] = 'create'
    type_name = ''
    
    _site_url = get_site_url_id(request)
    
    p = PortalCatalog.objects.filter(site__url=_site_url)
    
    if 'type_name' in request.GET:
        type_name = request.GET['type_name'].lower()
    else:
        raise Http404('Tipo de objejo não foi informado.')
    
    try:
        _path_url = reescrever_url(request)
        _object = p.get(path_url=_path_url)
    except PortalCatalog.DoesNotExist:
        _object = PortalCatalog()
        
    if type_name in TYPE_NAME:
        if type_name=='pagina' and (_object.tipo in ['ATPasta', '']):
            return paginas.create(request)
        
        if type_name=='pasta' and (_object.tipo in ['ATPasta', '']):
            return pastas.create(request)
        
        if type_name=='noticia' and (_object.tipo in ['ATPasta', '']):
            return noticias.create(request)
        
        if type_name=='imagem' and (_object.tipo in ['ATPasta', '']):
            return imagens.create(request)
        
        if type_name=='link' and (_object.tipo in ['ATPasta', '']):
            return links.create(request)
        
        if type_name=='banner' and (_object.tipo in ['ATPasta', '']):
            return banners.create(request)
        
        if type_name=='arquivo' and (_object.tipo in ['ATPasta', '']):
            return arquivos.create(request)
        
        if type_name=='evento' and (_object.tipo in ['ATPasta', '']):
            return eventos.create(request)
        
        if type_name=='agenda' and (_object.tipo in ['ATPasta', '']):
            return agendas.create(request)
        
        if type_name=='informe' and (_object.tipo in ['ATPasta', '']):
            return informes.create(request)
        
        raise Http404('Não é permitido esse tipo de operação.')
    else:
        raise Http404('Tipo de conteúdo não existe.')
    
    return redirect('portal:index')

@login_required(login_url='/security/login/')
def __updateObject(request):
    _site_url = get_site_url_id(request)
    catalogs = PortalCatalog.objects.filter(site__url=_site_url)
    request.session['action'] = 'edit'
    try:
        _content_url = reescrever_url(request)
        _object = catalogs.get(path_url=_content_url)
        if _object.tipo == 'ATPagina':
            return paginas.edit(request)
        
        if _object.tipo == 'ATPasta':
            return pastas.edit(request)
        
        if _object.tipo == 'ATNoticia':
            return noticias.edit(request)
        
        if _object.tipo == 'ATImagem':
            return imagens.edit(request)
        
        if _object.tipo == 'ATLink':
            return links.edit(request)
        
        if _object.tipo == 'ATBanner':
            return banners.edit(request)
        
        if _object.tipo == 'ATArquivo':
            return arquivos.edit(request)
        
        if _object.tipo == 'ATEvento':
            return eventos.edit(request)
        
        if _object.tipo == 'ATAgenda':
            return agendas.edit(request)
        
        if _object.tipo == 'ATInforme':
            return informes.edit(request)
        
    except PortalCatalog.DoesNotExist:
        raise Http404('Página não encontrada.')

@login_required(login_url='/security/login/')
def __deleteObjec(request):
    _site_url = get_site_url_id(request)
    p = PortalCatalog.objects.filter(site__url=_site_url)
    
    try:
        _content_url = reescrever_url(request)
        _object = p.get(path_url=_content_url)
        if _object.tipo == 'ATPagina':
            return paginas.delete(request, _object)
        
        if _object.tipo == 'ATPasta':
            #Verificar sua implementação
            return redirect(reescrever_url(request))
        
        if _object.tipo == 'ATNoticia':
            return noticias.delete(request, _object)
        
        if _object.tipo == 'ATImagem':
            return imagens.delete(request, _object)
        
        if _object.tipo == 'ATLink':
            return links.delete(request, _object)
        
        if _object.tipo == 'ATBanner':
            return banners.delete(request, _object)
        
        if _object.tipo == 'ATArquivo':
            return arquivos.delete(request, _object)
        
        if _object.tipo == 'ATEvento':
            return eventos.delete(request, _object)
        
        if _object.tipo == 'ATAgenda':
            return agendas.delete(request, _object)
        
        if _object.tipo == 'ATInforme':
            return informes.delete(request, _object)
        
    except PortalCatalog.DoesNotExist:
        raise Http404('Página não encontrada.')

def __listObject(request):
    request.session['action'] = 'list'
    _url = reescrever_url(request)
    template = '%s/documents.html' % 'comum'
    context = {
        'url' : _url
        }
    return render(request, template, context)
        
def __view(request):
    request.session['action'] = 'view'
    _site_url = get_site_url_id(request)
    _path_url = reescrever_url(request)
    
    p = PortalCatalog.objects.filter(site__url=_site_url)
    _object = None
    try:
        p = p.get(path_url=_path_url)
        _object = p.get_content_object()
    except PortalCatalog.DoesNotExist:
        raise Http404('Pagina não encontrada.')
    
    template = '%s/documents.html' % 'comum'
    context = {
        'object' : _object,
        }
    
    return render(request, template, context)

@login_required(login_url='/security/login/')
def __organizador_content(request):
    _site_url = get_site_url_id(request)
    object_post = request.body
    response_data = {}
    itens = json.loads(object_post)['objects']
    _lista = PortalCatalog.objects.filter(site__url=_site_url)
    nova_orden = 1
    for i in itens:
        o = _lista.get(id=i)
        o.ordenador = nova_orden
        o.save()
        nova_orden += 1
        
    return HttpResponse(json.dumps(response_data), content_type="application/json",)

@login_required(login_url='/security/login/')
def __image_browse_url(request):
    _url_site = get_site_url_id(request)
    _list_imagens = Imagem.objects.filter(site__url=_url_site)
    data_json = []
    for img in _list_imagens:
        data={'url':img.imagem.url}
        data_json.append(data)
    return HttpResponse(json.dumps(data_json), content_type="application/text")

@login_required(login_url='/security/login/')       
def __select_default_page(request):
    new_url = reescrever_url(request)
    _content_url = get_url_id_content(request)
    _site_url = get_site_url_id(request)
    _object = Pasta.objects.filter(site__url = _site_url).get(url=_content_url)    
    
    if 'view' in request.GET:
        _view = request.GET['view']
        if _view in ('sumaria', 'agenda', 'evento', 'arquivo', 'noticia'):
            _object.visao_padrao = _view
            _object.save()

        return redirect(new_url)

    if 'content_view_url' in request.POST:
        _obj_id = request.POST['content_view_url']
        _portal_catalog = PortalCatalog.objects.get(id=_obj_id)
        
        _obj_select = get_content_by_portal_catalog(_portal_catalog)
        
        if _obj_select:    
            _object.visao_padrao = '%s,%s' % (_obj_select.id, _obj_select.tipo)
            _object.save()
    else:
        _object.visao_padrao = None
        _object.save()
            
    #Faz a subetituição
    return redirect(new_url)

@login_required(login_url='/security/login/')
def __add_item_session(request):
    _site_url = get_site_url_id(request)
    request.session['action'] = 'sessions_manage'
    
    if not 'type' in request.GET:
        raise Http404('Operação não permitida.')

    _session = request.GET['type']
    _objsct_session = Sessao.objects.filter(site__url=_site_url).get(sessao=_session)
    
    if 'excluir' in request.GET:
        _item_excluir = request.GET['excluir']
        _objsct_session.conteudo.remove(_item_excluir)
        return redirect('%s?type=%s' % (request.path, _session))
    
    if request.POST:
        _list=request.POST.getlist('content')
        for i in _list:
            _objsct_session.conteudo.add(i)
            
        return redirect('%s?type=%s' % (request.path, _session))
    
    _list_sessions = _objsct_session.conteudo.all()
    
    template = 'comum/sessions.html'
    context = {
            'object' : _objsct_session,
            'list_sessions' : _list_sessions,
        }
    
    return render(request, template, context)

def __search(request):
    template = 'comum/search.html'
    _result = None
    request.session['action'] = 'search'
    if request.POST:
        _search = request.POST['search']
        _result = PortalCatalog.objects.filter(Q(titulo__icontains=_search)|Q(descricao__icontains=_search))
        if 'search_all_sites' in request.POST:
            _site_url = get_site_url_id(request)
            _result = _result.filter(site__url=_site_url)
        
        _result = _result.filter(workflow='Publicado')
        
    context = {
        'search' : _result
        }
    return render(request, template, context)

@login_required(login_url='/security/login/')
def __portlet(request):
    
    request.session['action'] = 'portlet'
    
    if 'create' in request.GET:
        return portlets.create(request)
    
    if 'edit' in request.GET:
        return portlets.edit(request)
    
    if 'delete' in request.GET:
        return portlets.delete(request)
    
    if 'portlet' in request.GET:
        return portlets.add_item_portlet(request)
    
    template = 'comum/portlets.html'
    
    context = {
        
        }
    
    return render(request, template, context)

def index(request, url=None):
    
    if request.path == '/':
        return redirect('manage_main:index')
    
    request.session['action'] = 'index'
    context={
        'object' : None,
        }
    _site_url = get_site_url_id(request)
    
    template = '%s/index.html' % _site_url
    
    _fragment_url = fraguiment_url(request)
    
    if '@@manage-portlets' in _fragment_url:
        if len(_fragment_url) >= 1:
            return __portlet(request)
        else:
            raise Http404('Operação não permitida.')
    
    if 'createObject' in _fragment_url:
        if 'createObject' in _fragment_url[-1]:
            return __createObject(request)
        else:
            raise Http404('Tipo de objeto reservado para o sistema')
    
    if 'folder_contents' in _fragment_url:
        if 'folder_contents' in _fragment_url[-1]:
            if len(_fragment_url) >= 2:
                return __listObject(request)
            else:
                raise Http404('Operação não permitida')
        else:
            raise Http404('Operação não permitida')
    
    if 'content_status_modify' in _fragment_url:
        if 'workflow_action' in request.GET:
            return __workflowObject(request)
        else:
            raise Http404('Operação não permitida.')
        
    if 'select_default_page' in _fragment_url:
        if len(_fragment_url) > 2:
            return __select_default_page(request)
        else:
            raise Http404('Operação não permitida.')
    
    
    if 'edit' in _fragment_url:
        if 'edit' == _fragment_url[-1]:
            return __updateObject(request)
        else:
            raise Http404('Tipo de objeto reservado para o sistema')
    
    if 'organizador_content' in _fragment_url:
        if len(_fragment_url) >= 2 and request.is_ajax():
            return __organizador_content(request)
        else:
            raise Http404('Operação não permitida.')
    
    if 'image_browse_url' in _fragment_url:
        if len(_fragment_url) >= 2 and request.is_ajax():
            return __image_browse_url(request)
        else:
            raise Http404('Operação não permitida.')
        
    if 'sessions_manage' in _fragment_url:
        if len(_fragment_url) >= 2:
            return __add_item_session(request)
        else:
            raise Http404('Operação não permitida.')
    
    if 'search' in _fragment_url:
        if len(_fragment_url) >= 2:
            return __search(request)
        else:
            raise Http404('Operação não permitida.')
        
    if 'delete' in _fragment_url:
        if len(_fragment_url)>=2:
            return __deleteObjec(request)
        else:
            raise Http404('Operação não permitida.')
    
    if len(_fragment_url) > 1:
        return __view(request)
    
    try:
        return render(request, template, context)
    except TemplateDoesNotExist:
        template = '%s/index.html' % 'comum'
        return render(request, template, context)

def _login(request):
    request.session['action'] = None
    template = 'login.html'
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        url_next = 'portais:login'
        if user:
            if user.is_active:
                login(request, user)
                try:
                    url_next = request.GET['next']
                except:
                    pass
                return redirect(url_next)
            else:
                messages.warning(request, 'Conta de usuário esta bloqueada para acessar ao sistema.', 'alert-success')
        else:
            messages.warning(request, 'Usuário ou senha invalida! Corrija e tente novamente.', 'alert-warning')
    return render(request, template, context)