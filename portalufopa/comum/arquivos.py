# -*- coding: utf-8 -*-
from datetime import date

from django.shortcuts import redirect, render
from django.utils.text import slugify

from ..comum.utils import create_portal_catalog, get_site_url, \
    get_url_request, update_portal_catalog, content_workflow_modify
from ..forms import ArquivoForm
from ..models import Arquivo


TEMPLATE = '%s/documents.html' % 'comum'

def create(request, path_url):
    form = ArquivoForm(request.POST or None, request.FILES or None)
    site = get_site_url(get_url_request(request)[0])
    if form.is_valid():
        model = form.save(commit=False)
        _url = slugify(model.titulo)
        model.url = _url
        model.tipo = 'ATArquivo'
        model.site = site
        model.dono = request.user
        if 'arquivo' in request.FILES:
            model.arquivo = request.FILES['arquivo']
        model.save()
        if path_url:
            path_url = path_url % _url
        create_portal_catalog(model, path_url)
        return redirect(path_url)

    context = {
        'form' : form,
        }
    
    return render(request, TEMPLATE, context)

def edit(request, url):
    _url = url.strip('/').split('/')
    _object = Arquivo.objects.filter(site__url=_url[0]).get(url=_url[-1])
    form = ArquivoForm(request.POST or None, request.FILES or None, instance=_object)
    if form.is_valid():
        model = form.save(commit=False)
        model.update_at = date.today()
        if 'arquivo' in request.FILES:
            model.imagem = request.FILES['arquivo']
        model.save()
        update_portal_catalog(model)
        return redirect(url)
    context = {
        'form' : form,
        }
    
    return render(request, TEMPLATE, context)

def workflow(request, portal_catalog, _workflow):
    _o = Arquivo.objects.filter(site__url=get_url_request(request)[0]).get(url=portal_catalog.url)
    content_workflow_modify(_o, _workflow)