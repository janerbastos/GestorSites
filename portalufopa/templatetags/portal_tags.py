# -*- coding: utf-8 -*-

from datetime import date

from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404
from django.utils.html import format_html

from portalufopa.comum.utils import WORKFLOW_COLOR, ICONS,\
    get_content_by_tipo, MAIS_CONTENTS

from ..comum.utils import CONTENT_BY_TYPE
from ..models import Site, PortalCatalog, Sessao
from portalufopa.comum.contents import get_site_url_id, reescrever_url,\
    fraguiment_url
from portalufopa.models import Portlet


register = template.Library()

@register.assignment_tag(takes_context=True)
def has_site(context):
    ''' Função responsável por retorna os dados do site, passando como parametro a url rais do site
        param = @site
    '''
    _site_url = get_site_url_id(context.request)
    
    try:
        return Site.objects.get(url=_site_url)
    except ObjectDoesNotExist:
        raise Http404('Site não encontrado.')

@register.simple_tag(takes_context=True)
def has_visao_padrao(context, param):
    if param == 'sumaria':
        return param
    itens = param.split(',')
    site = context['site']
    _object = get_content_by_tipo(site.url, itens[0], itens[1])
    
    return _object

@register.simple_tag(takes_context=True)
def has_list_object_sessao(context, sessao):
    _site = context['site']
    try:
        _list_obj_sessao = Sessao.objects.filter(site__url = _site.url).get(sessao=sessao)
    except Sessao.DoesNotExist:
        return None
    
    return _list_obj_sessao.conteudo.all()

@register.simple_tag(takes_context=True)
def has_list_objects_pasta(context, **kwargs):
    url = context.request.path
    lista = []
    nivel = len(url.strip('/').split('/'))+1
    _p = PortalCatalog.objects.filter(path_url__startswith=url).exclude(path_url=url).order_by('ordenador')
    if 'excluir' in kwargs:
        _p = _p.exclude( tipo=kwargs['excluir'])
    for i in _p:
        if len(i.path_url.strip('/').split('/')) == nivel:
            lista.append(i)
    return lista

@register.simple_tag(takes_context=True)
def has_list_pastas(context):
    url_site = context.request.path.replace('/folder_contents', '')
    _p = PortalCatalog.objects.filter(path_url__startswith=url_site,).exclude(path_url=url_site).order_by('ordenador')
    nivel = len(url_site.strip('/').split('/'))+1
    _html = "<ul id='ordenador'>"
    for i in _p:
        if len(i.path_url.strip('/').split('/')) == nivel: 
            _html += "<li id='%s'><a href='%s' class='%s' >%s %s</a></li>" % (i.id, i.path_url, WORKFLOW_COLOR[i.workflow], ICONS[i.tipo], i.titulo)
    _html += '</ul>'
    return format_html(_html)

@register.assignment_tag(takes_context=True)
def has_session(context):
    _action = None
    try:
        _action = context.request.session['action']
    except:
        pass
    
    return _action

@register.simple_tag(takes_context=True)
def has_list_object_by_type(context, item, quantidade):
    content_type = CONTENT_BY_TYPE[item.replace('AT', '').lower()]
    _site = context['site']
    if quantidade == 0:
        _list_object =  PortalCatalog.objects.filter(site__url=_site.url, tipo=content_type).order_by('-public_at')
    else:
        _list_object =  PortalCatalog.objects.filter(site__url=_site.url, tipo=content_type).order_by('-public_at')[:quantidade]
    
    return _list_object

@register.simple_tag(takes_context=True)
def has_list_object(context, **kwargs):
    _site = context['site']
    _list_object = None
    
    if 'tipo' in kwargs:
        content_type = kwargs['tipo']
        _list_object =  PortalCatalog.objects.filter(site__url=_site.url, tipo=content_type)
    
    if 'list' in kwargs:
        _list = kwargs['list']
        if _list_object:
            _itens = _list.values_list('id', flat=True)
            _list_object = _list_object.exclude(id__in = _itens)
    
    if 'footer_url' in kwargs:
        content_footer = kwargs['footer_url']
        _list_object =  PortalCatalog.objects.filter(site__url=_site.url, path_url__startswith=content_footer).exclude(tipo='ATPasta').order_by('titulo')
       
    return _list_object

@register.simple_tag()
def has_content_by_portal_catalog(object_portal_catalog):
    _object = object_portal_catalog.get_content_object()

    return _object

@register.simple_tag()
def data_atual(format_string):
    return date.today().strftime(format_string)

@register.inclusion_tag('tags/menu_horizontal.html', takes_context=True)
def has_menu_horizontal(context):
    _site = context['site']
    _p = PortalCatalog.objects.filter(site__url=_site.url).order_by('ordenador')
    n_1 = _p.filter(path_url__startswith='/%s'%_site.url)
    menu=[]
    indice = 1
    for i in n_1:
        nivel = len(i.path_url.strip('/').split('/'))
        if nivel == 2:
            menu.append(i)
            indice +=1
    return {'menu':menu, 'site' : _site }

@register.simple_tag()
def has_sub_menu(obj, posicao):
    _sn = PortalCatalog.objects.filter(path_url__startswith=obj.path_url).order_by('ordenador')
    menu=[]
    for i in _sn:
        nivel = len(i.path_url.strip('/').split('/'))
        if nivel == posicao:
            menu.append(i)
    return menu

@register.simple_tag(takes_context=True)
def has_action_view_edit(context, action):
    _new_url = ''
    _url_aux = fraguiment_url(context.request)
    _url_default = context.request.path
    
    if action in ['edit', 'folder_contents']:
        if action not in _url_aux: 
            _new_url = '%s%s/' % (_url_default, action)
        else:
            _new_url = _url_default
    elif action == 'view':
        _new_url = reescrever_url(context.request)
            
    return _new_url

@register.simple_tag(takes_context=True)
def format_menu_admin_content(context, tipo):
    _html = context.request.path.replace('/folder_contents', '')
    _url = "%screateObject/?type_name=%s" % (_html, tipo)
    return _url

@register.simple_tag(takes_context=True)
def format_menu_session(context, sessao):
    site = context['site']
    return '/%s/sessions_manage/?type=%s' % (site.url, sessao)

@register.simple_tag()
def has_icon_content(tipo):
    return format_html(ICONS[CONTENT_BY_TYPE[tipo]])

@register.simple_tag()
def has_workflow_color(workflow):
    _html = WORKFLOW_COLOR[workflow]
    return format_html(_html)

@register.simple_tag(takes_context=True)
def has_breadcrumbs(context):
    _html = " <div class='linha-inicio'> <ol>"
    _site_url = get_site_url_id(context.request)
    _p = PortalCatalog.objects.filter(site__url=_site_url,)
    aux = '/'
    count = 0
    _url = reescrever_url(context.request).strip('/').split('/')
    if len(_url) == 1:
        _html += "<li class='active'>Pagina Inicial</li>"
    else:
        for i in _url:
            
            if i not in ['folder_contents', 'createObject', 'edit'] :
                
                if count < len(_url)-1:
                    aux += i + '/'
                    if count == 0:
                        _html += "<li><a href='%s'>Inicio</a>&nbsp;-&nbsp;</li>" % aux
                    else:
                        text_link = _p.get(path_url=aux)
                        _html += "<li><a href='%s'>%s</a>&nbsp;-&nbsp;</li>" % (aux, text_link.titulo)
                    
                    count += 1
                else:
                    aux += i + '/'
                    text_link = _p.get(path_url=aux)
                    _html += "<li class='active'>%s</li>" % text_link.titulo
            else:
                _html += "<li class='active'>[...]</li>"
    _html += "</ol> </div>"
    
    return format_html(_html)

@register.simple_tag(takes_context=True)
def has_list_sessions_site(context):
    _site = context['site'] 
    _list_sessions = Sessao.objects.filter(site=_site)
    
    return _list_sessions

@register.inclusion_tag('tags/menu_footer.html', takes_context=True)
def has_menu_footer(context):
    return has_menu_horizontal(context)

@register.simple_tag()
def has_select_item_menu(list_objects):
    _new_list = []
    
    for i in list_objects:
        if i.tipo != 'ATPasta':
            _new_list.append(i)
    return _new_list

@register.simple_tag()
def has_ifinlist(values, text):
    _list = values.split(',')
    if text in _list:
        return True
    else:
        return False

@register.simple_tag(takes_context=True)
def has_formata_url(context):
    return reescrever_url(context.request)

@register.simple_tag(takes_context=True)
def format_menu_portlets(context):
    _new_url = reescrever_url(context.request)
    return '%s%s' % (_new_url, "@@manage-portlets")

@register.simple_tag(takes_context=True)
def has_portlets(context):
    _url = reescrever_url(context.request).strip('/').split('/')
    _site_url = get_site_url_id(context.request)
    
    _result = []
    for item in _url:
        _p = None
        if item == _site_url:
            p_ = Portlet.objects.filter(site__url=_site_url, origem='pagina-inicial')
        else:
            portal_catalog = PortalCatalog.objects.filter(site__url=_site_url).get(url=item)
            _obj = portal_catalog.get_content_object()
            p_ = _obj.portlet.all()
            
        for i in p_:
            _result.append(i)
    return _result

@register.simple_tag()    
def has_text_mais_tipo(tipo):
    tipo = tipo.replace('AT', '').lower()
    return MAIS_CONTENTS[tipo]