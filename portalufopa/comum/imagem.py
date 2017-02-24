# -*- coding: UTF-8 -*-
from datetime import date
import md5
import os

from django.template.defaultfilters import slugify


def content_file_imagem(instance, filename):
    ext = filename.split('.')[-1]
    filename = md5.new(slugify(filename)).hexdigest()
    filename = filename + '.' + ext
    return os.path.join('file/site/%s/imagens/%s' % (instance.site.url, date.today().year), filename)

def content_file_documento(instance, filename):
    ext = filename.split('.')[-1]
    filename = md5.new(slugify(filename)).hexdigest()
    filename = filename + '.' + ext
    return os.path.join('file/site/%s/documentos/%s' % (instance.site.url, date.today().year), filename)

def content_file_imagem_site(instance, filename):
    ext = filename.split('.')[-1]
    filename = md5.new(slugify(filename)).hexdigest()
    filename = filename + '.' + ext
    return os.path.join('file/site/%s/imagens/configure' % (instance.url), filename)