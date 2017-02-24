# -*- coding: utf-8 -*-
from datetime import date

from django.shortcuts import redirect, render
from django.utils.text import slugify

from ..comum.utils import create_portal_catalog, get_site_url, \
    get_url_request, update_portal_catalog, content_workflow_modify, WORKFLOW
from ..forms import InformeForm
from ..models import Informe


TEMPLATE = '%s/documents.html' % 'comum'

def create(request, path_url):
    form = InformeForm(request.POST or None,)
    site = get_site_url(get_url_request(request)[0])
    if form.is_valid():
        model = form.save(commit=False)
        _url = slugify(model.titulo)
        model.url = _url
        model.tipo = 'ATInforme'
        model.site = site
        model.update_at = date.today()
        if 'imagem' in request.FILES:
            model.imagem = request.FILES['imagem']
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
    _object = Informe.objects.filter(site__url=_url[0]).get(url=_url[-1])
    form = InformeForm(request.POST or None, instance=_object)
    if form.is_valid():
        model = form.save(commit=False)
        if 'imagem' in request.FILES:
            model.imagem = request.FILES['imagem']
        model.save()
        update_portal_catalog(model)
        return redirect(url)
    context = {
        'form' : form,
        }
    
    return render(request, TEMPLATE, context)

def workflow(request, _object, _workflow):
    _url_site = get_url_request(request)[0]
    _o = Informe.objects.filter(site__url=_url_site).get(url=_object.url)
    content_workflow_modify(_o, _workflow)