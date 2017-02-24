# -*- coding: utf-8 -*-

import json

from django.http.response import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.template.exceptions import TemplateDoesNotExist

from portalufopa.comum.utils import ORGANIZADOR_CONTENT, IMAGE_BROWSE_URL,\
    get_content_by_portal_catalog
from portalufopa.models import Sessao

from .comum import agendas
from .comum import paginas, pastas, noticias, imagens, links, banners, arquivos, eventos_, informes
from .comum.utils import TYPE_NAME, get_url_request, CREATE_OBJECT, \
    EDIT_OBJECT, FOLDER_CONTENTS, CONTENT_STATUS_MODIFY, \
    WORKFLOW_ACTION, WORKFLOW, SELECT_DEFAULT_PAGE
from .models import PortalCatalog, Pagina, Pasta, Noticia, Imagem, Link, \
    Banner, Arquivo, Evento, Agenda, Informe


# Create your views here.
def __workflowObject(request):
    _p = PortalCatalog.objects.filter(site__url=get_url_request(request)[0])
    _url = request.path.replace('/content_status_modify', '')
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
            eventos_.workflow(request, _p, WORKFLOW[_workflow])
            
        if _p.tipo == 'ATAgenda':
            agendas.workflow(request, _p, WORKFLOW[_workflow])
        
        if _p.tipo == 'ATInforme':
            informes.workflow(request, _p, WORKFLOW[_workflow])
            
    else:
        raise Http404('Operação não permitida.')
    
    return redirect(_url)

def __createObject(request):
    request.session['action'] = 'create'
    type_name = ''
    p = PortalCatalog.objects.filter(site__url=get_url_request(request)[0])
    
    if 'type_name' in request.GET:
        type_name = request.GET['type_name'].lower()
    else:
        raise Http404('Nenhum tipo de objejo foi informado.')
    
    _url = request.path.replace('createObject', '%s')
    
    try:
        _object = p.get(path_url=request.path.replace('createObject/', ''))
    except PortalCatalog.DoesNotExist:
        _object = PortalCatalog()
        
    if type_name in TYPE_NAME:
        if type_name=='pagina' and (_object.tipo in ['ATPasta', '']):
            return paginas.create(request, _url)
        
        if type_name=='pasta' and (_object.tipo in ['ATPasta', '']):
            return pastas.create(request, _url)
        
        if type_name=='noticia' and (_object.tipo in ['ATPasta', '']):
            return noticias.create(request, _url)
        
        if type_name=='imagem' and (_object.tipo in ['ATPasta', '']):
            return imagens.create(request, _url)
        
        if type_name=='link' and (_object.tipo in ['ATPasta', '']):
            return links.create(request, _url)
        
        if type_name=='banner' and (_object.tipo in ['ATPasta', '']):
            return banners.create(request, _url)
        
        if type_name=='arquivo' and (_object.tipo in ['ATPasta', '']):
            return arquivos.create(request, _url)
        
        if type_name=='evento' and (_object.tipo in ['ATPasta', '']):
            return eventos_.create(request, _url)
        
        if type_name=='agenda' and (_object.tipo in ['ATPasta', '']):
            return agendas.create(request, _url)
        
        if type_name=='informe' and (_object.tipo in ['ATPasta', '']):
            return informes.create(request, _url)
        
        raise Http404('Não é permitido esse tipo de operação.')
    else:
        raise Http404('Tipo de conteúdo não existe.')
    
    return redirect('portal:index')

def __updateObject(request):
    p = PortalCatalog.objects.filter(site__url=get_url_request(request)[0])
    request.session['action'] = 'edit'
    try:
        _object = p.get(path_url=request.path.replace('/edit', ''))
        if _object.tipo == 'ATPagina':
            return paginas.edit(request, _object.path_url)
        
        if _object.tipo == 'ATPasta':
            return pastas.edit(request, _object.path_url)
        
        if _object.tipo == 'ATNoticia':
            return noticias.edit(request, _object.path_url)
        
        if _object.tipo == 'ATImagem':
            return imagens.edit(request, _object.path_url)
        
        if _object.tipo == 'ATLink':
            return links.edit(request, _object.path_url)
        
        if _object.tipo == 'ATBanner':
            return banners.edit(request, _object.path_url)
        
        if _object.tipo == 'ATArquivo':
            return arquivos.edit(request, _object.path_url)
        
        if _object.tipo == 'ATEvento':
            return eventos_.edit(request, _object.path_url)
        
        if _object.tipo == 'ATAgenda':
            return agendas.edit(request, _object.path_url)
        
        if _object.tipo == 'ATInforme':
            return informes.edit(request, _object.path_url)
        
    except PortalCatalog.DoesNotExist:
        raise Http404('Página não encontrada.')

def __listObject(request):
    request.session['action'] = 'list'
    _url = request.path.replace('/folder_contents', '')
    template = '%s/documents.html' % 'comum'
    context = {
        'url' : _url
        }
    return render(request, template, context)
        
def __view(request):
    request.session['action'] = 'view'
    _url_site = get_url_request(request)
    _path_url = request.path
    _site_url = get_url_request(request)[0]
    p = PortalCatalog.objects.filter(site__url=_site_url)
    _object = None
    try:
        p = p.get(path_url=_path_url)
        if p.tipo == 'ATPagina':
            _object = Pagina.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATPasta':
            _object = Pasta.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATNoticia':
            _object = Noticia.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATImagem':
            _object = Imagem.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATLink':
            _object = Link.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATBanner':
            _object = Banner.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATArquivo':
            _object = Arquivo.objects.filter(site__url=_site_url).get(url=p.url)
        
        if p.tipo == 'ATEvento':
            _object = Evento.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATAgenda':
            _object = Agenda.objects.filter(site__url=_site_url).get(url=p.url)
            
        if p.tipo == 'ATInforme':
            _object = Informe.objects.filter(site__url=_site_url).get(url=p.url)
            
    except PortalCatalog.DoesNotExist:
        raise Http404('Pagina não encontrada.')
    
    context = {
        'object' : _object,
        }
    
    return render(request, 'comum/documents.html', context)

def __organizador_content(request):
    _url_site = get_url_request(request)[0]
    object_post = request.body
    response_data = {}
    itens = json.loads(object_post)['objects']
    _lista = PortalCatalog.objects.filter(site__url=_url_site)
    nova_orden = 1
    for i in itens:
        o = _lista.get(id=i)
        o.ordenador = nova_orden
        o.save()
        nova_orden += 1
        
    return HttpResponse(json.dumps(response_data), content_type="application/json",)

def __image_browse_url(request):
    _url_site = get_url_request(request)[0]
    _list_imagens = Imagem.objects.filter(site__url=_url_site)
    data_json = []
    for img in _list_imagens:
        data={'url':img.imagem.url}
        data_json.append(data)
    return HttpResponse(json.dumps(data_json), content_type="application/text")
       
def __select_default_page(request):
    new_url = request.path.replace('/select_default_page', '')
    _url = new_url.strip('/').split('/')[-1]
    _url_site = get_url_request(request)[0]
    _object = Pasta.objects.filter(site__url = _url_site).get(url=_url)    
    
    if 'view' in request.GET:
        _view = request.GET['view']
        if _view == 'sumaria':
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

def __add_item_session(request):
    _url_site = get_url_request(request)[0]
    request.session['action'] = 'sessions_manage'
    template = 'sessions.html'
    
    
    if not 'type' in request.GET:
        raise Http404('Operação não permitida.')

    _session = request.GET['type']
    _objsct_session = Sessao.objects.filter(site__url=_url_site).get(sessao=_session)
    
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
    
    context = {
            'object' : _objsct_session,
            'list_sessions' : _list_sessions,
        }
    
    return render(request, template, context)
    
def index(request, url=None):
    
    if request.path == '/':
        return redirect('manage_main:index')
    
    request.session['action'] = 'index'
    context={
        'object' : None,
        }
    _url_site = get_url_request(request)
    
    template = '%s/index.html' % _url_site[0]
    
    if CREATE_OBJECT in _url_site:
        if CREATE_OBJECT in _url_site[-1]:
            return __createObject(request)
        else:
            raise Http404('Tipo de objeto reservado para o sistema')
    
    if FOLDER_CONTENTS in _url_site:
        if FOLDER_CONTENTS in _url_site[-1]:
            if len(_url_site) >= 2:
                return __listObject(request)
            else:
                raise Http404('Operação não permitida')
        else:
            raise Http404('Operação não permitida')
    
    if CONTENT_STATUS_MODIFY in _url_site:
        if 'workflow_action' in request.GET:
            return __workflowObject(request)
        else:
            raise Http404('Operação não permitida.')
        
    if SELECT_DEFAULT_PAGE in _url_site:
        if len(_url_site) > 2:
            return __select_default_page(request)
        else:
            raise Http404('Operação não permitida.')
        
    if EDIT_OBJECT in _url_site:
        if EDIT_OBJECT in _url_site[-1]:
            return __updateObject(request)
        else:
            raise Http404('Tipo de objeto reservado para o sistema')
    
    if ORGANIZADOR_CONTENT in _url_site:
        if len(_url_site) >= 2 and request.is_ajax():
            return __organizador_content(request)
        else:
            raise Http404('Operação não permitida.')
    
    if IMAGE_BROWSE_URL in _url_site:
        if len(_url_site) >= 2 and request.is_ajax():
            return __image_browse_url(request)
        else:
            raise Http404('Operação não permitida.')
        
    if 'sessions_manage' in _url_site:
        if len(_url_site) >= 2:
            return __add_item_session(request)
        else:
            raise Http404('Operação não permitida.')
    
    if len(_url_site) > 1:
        return __view(request)
    
    try:
        return render(request, template, context)
    except TemplateDoesNotExist:
        template = '%s/index.html' % 'comum'
        return render(request, template, context)

def login(request):
    request.session['action'] = None
    return redirect('evento:index')