# -*- coding: utf-8 -*-

from datetime import datetime

from django.shortcuts import redirect, render

from ..forms import PastaForm
from ..models import Pasta
from ..comum.contents import get_site_url, reescrever_url,\
    save_in_portal_catalog, get_site_url_id, get_url_id_content, save_indice_url


TEMPLATE = '%s/documents.html' % 'comum'

def create(request):
    path_url = reescrever_url(request)
    form = PastaForm(request.POST or None,)
    site = get_site_url(request)
    if form.is_valid():
        model = form.save(commit=False)
        _url = save_indice_url(request, model.titulo)
        model.url = _url
        model.tipo = 'ATPasta'
        model.site = site
        model.dono = request.user
        model.save()
        path_url += _url + '/'
        save_in_portal_catalog(model, path_url)
        return redirect(path_url)

    context = {
        'form' : form,
        }
    
    return render(request, TEMPLATE, context)

def edit(request):
    _url = reescrever_url(request)
    _site_url = get_site_url_id(request)
    _content_url = get_url_id_content(request)
    _object = Pasta.objects.filter(site__url=_site_url).get(url=_content_url)
    form = PastaForm(request.POST or None, instance=_object)
    if form.is_valid():
        model = form.save(commit=False)
        model.update_at = datetime.now()
        model.save()
        save_in_portal_catalog(model)
        return redirect(_url)
    context = {
        'form' : form,
        }
    return render(request, TEMPLATE, context)

def workflow(request, portal_catalog, _workflow):
    _site_url = get_site_url_id(request)
    _o = Pasta.objects.filter(site__url=_site_url).get(url=portal_catalog.url)
    _o.workflow = _workflow
    if _o.workflow == 'Publicado' and _o.public_at==None:
        print _o.workflow
        _o.public_at = datetime.now()
    _o.save()
    save_in_portal_catalog(_o)