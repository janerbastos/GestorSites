# -*- coding: utf-8 -*-
from datetime import datetime

from django.shortcuts import redirect, render

from ..forms import BannerForm
from ..models import Banner
from ..comum.contents import reescrever_url, get_site_url,\
    save_in_portal_catalog, get_site_url_id, get_url_id_content, save_indice_url, format_visao_by_delete
from security.anotation import permission_content


TEMPLATE = '%s/documents.html' % 'comum'

@permission_content(tipo='ATBanner', permissao='create', login_url='/security/login/')
def create(request):
    path_url = reescrever_url(request)
    form = BannerForm(request.POST or None, request.FILES or None)
    site = get_site_url(request)
    if form.is_valid():
        model = form.save(commit=False)
        _url = save_indice_url(request, model.titulo)
        model.url = _url
        model.tipo = 'ATBanner'
        model.site = site
        if 'imagem' in request.FILES:
            model.imagem = request.FILES['imagem']
        model.dono = request.user
        model.save()
        path_url += _url + '/'
        save_in_portal_catalog(model, path_url)
        return redirect(path_url)

    context = {
        'form' : form,
        }
    _site_url = get_site_url_id(request)
    template = '%s/documents.html' % _site_url
    try:
        return render(request, template, context)
    except:
        return render(request, TEMPLATE, context)

@permission_content(tipo='ATBanner', permissao='update', login_url='/security/login/')
def edit(request):
    _url = reescrever_url(request)
    _site_url = get_site_url_id(request)
    _content_url = get_url_id_content(request)
    _object = Banner.objects.filter(site__url=_site_url).get(url=_content_url)
    form = BannerForm(request.POST or None, request.FILES or None, instance=_object)
    if form.is_valid():
        model = form.save(commit=False)
        model.update_at = datetime.now()
        if 'imagem' in request.FILES:
            model.imagem = request.FILES['imagem']
        model.save()
        save_in_portal_catalog(model)
        return redirect(_url)
    context = {
        'form' : form,
        }
    template = '%s/documents.html' % _site_url
    try:
        return render(request, template, context)
    except:
        return render(request, TEMPLATE, context)

@permission_content(tipo='ATBanner', permissao='delete', login_url='/security/login/')
def delete(request, portal_catalog):
    content_url = get_url_id_content(request)
    content = portal_catalog.get_content_object()
    content.delete()
    portal_catalog.delete()
    _new_url = reescrever_url(request)
    _new_url = _new_url.replace('/'+content_url, '')
    _site_url = get_site_url_id(request)
    #verica ocorrencia de visão do content na pasta e formata para visão sumaria
    format_visao_by_delete(_site_url, _new_url)
    return redirect(_new_url)

@permission_content(tipo='ATBanner', permissao='workflow', login_url='/security/login/')
def workflow(request, portal_catalog, _workflow):
    _site_url = get_site_url_id(request)
    _o = Banner.objects.filter(site__url=_site_url).get(url=portal_catalog.url)
    _o.workflow = _workflow
    if _o.workflow == 'Publicado' and _o.public_at==None:
        _o.public_at = datetime.now()
    _o.save() 
    save_in_portal_catalog(_o)