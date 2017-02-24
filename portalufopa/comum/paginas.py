# -*- coding: utf-8 -*-
from datetime import date

from django.shortcuts import redirect, render
from django.utils.text import slugify

from ..comum.utils import create_portal_catalog, get_site_url, \
get_url_request, update_portal_catalog, content_workflow_modify
from ..forms import PaginaForm
from ..models import Pagina


TEMPLATE = '%s/documents.html' % 'comum'

def create(request, path_url):
    form = PaginaForm(request.POST or None,)
    site = get_site_url(get_url_request(request)[0])
    if form.is_valid():
        model = form.save(commit=False)
        _url = slugify(model.titulo)
        model.url = _url
        model.tipo = 'ATPagina'
        model.site = site
        model.update_at = date.today()
        model.dono = request.user
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
    _object = Pagina.objects.filter(site__url=_url[0]).get(url=_url[-1])
    form = PaginaForm(request.POST or None, instance=_object)
    if form.is_valid():
        model = form.save(commit=False)
        model.save()
        update_portal_catalog(model)
        return redirect(url)
    context = {
        'form' : form,
        }
    
    return render(request, TEMPLATE, context)

def workflow(request, portal_catalog, _workflow):
    _o = Pagina.objects.filter(site__url=get_url_request(request)[0]).get(url=portal_catalog.url)
    content_workflow_modify(_o, _workflow)
    