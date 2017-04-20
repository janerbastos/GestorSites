from portalufopa.forms import PortletForm, PortletDestaqueForm
from portalufopa.comum.contents import reescrever_url, get_site_url, get_url_id_content,\
    get_site_url_id
from django.template.defaultfilters import slugify
from django.shortcuts import redirect, render
from portalufopa.models import PortalCatalog, Portlet
from portalufopa.comum.utils import CONTENT_BY_TYPE
from security.anotation import permission_group

@permission_group('Administradores', login_url='/security/login/')
def create(request):
    path_url = reescrever_url(request)
    content_url = get_url_id_content(request)
    site = get_site_url(request)
    
    tipo = request.GET['create']
    if tipo == 'destaque':
        form = PortletDestaqueForm(request.POST or None)
    else:
        form = PortletForm(request.POST or None)
        
    if form.is_valid():
        
        model = form.save(commit=False)
        
        _url = '%s-%s' % (slugify(model.titulo), content_url)

        model.portlet = _url
        model.site = site
        model.posicao = 'left'
        
        if tipo != 'destaque':
            model.tipo = CONTENT_BY_TYPE[tipo]
        else:
            model.categoria = tipo 
        
        if site.url == content_url:
            model.origem = 'pagina-inicial'
        
        model.save()
        
        if site.url != content_url:
            portal_catalog = PortalCatalog.objects.filter(site=site).get(url=content_url)
            _obj = portal_catalog.get_content_object()
            _obj.portlet.add(model)
        
        path_url += '@@manage-portlets'
        
        return redirect(path_url)

    template = 'comum/portlets.html'
    context = {
        'form' : form,
        }
    
    return render(request, template, context)

@permission_group('Administradores', login_url='/security/login/')
def edit(request):
    path_url = reescrever_url(request)
    tipo = request.GET['edit']
    _site_url = get_site_url_id(request)
    _content_url = get_url_id_content(request)
 
    portlet = Portlet.objects.filter(site__url=_site_url).get(portlet=tipo)
    
    if portlet.categoria == 'destaque':
        form = PortletDestaqueForm(request.POST or None, instance=portlet)
    else:
        form = PortletForm(request.POST or None, instance=portlet)
        
    if form.is_valid():
        model = form.save(commit=False)
        _url = slugify(model.titulo)
        model.save()
        path_url += '@@manage-portlets'
        return redirect(path_url)

    template = 'comum/portlets.html'
    context = {
        'form' : form,
        }
    
    return render(request, template, context)

@permission_group('Administradores', login_url='/security/login/')   
def delete(request):
    path_url = reescrever_url(request)
    portlet_url = request.GET['delete']
    _site_url = get_site_url_id(request)
    portlet = Portlet.objects.filter(site__url=_site_url).get(portlet=portlet_url)
    portlet.delete()
    path_url += '@@manage-portlets'
    return redirect(path_url)

@permission_group('Administradores', login_url='/security/login/')
def add_item_portlet(request):
    _site_url = get_site_url_id(request)
    portlet_url = request.GET['portlet']
    portlet = Portlet.objects.filter(site__url=_site_url).get(portlet=portlet_url)
    
    if 'excluir' in request.GET:
        _item_excluir = request.GET['excluir']
        portlet.conteudo.remove(_item_excluir)
    
    if request.POST:
        _list=request.POST.getlist('content')
        for i in _list:
            portlet.conteudo.add(i)
    
    conteudos = portlet.conteudo.all()
    template = 'comum/portlets.html'
    context = {
        'portlet' : portlet,
        'conteudos' : conteudos,
        }
    
    return render(request, template, context)