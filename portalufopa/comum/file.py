# -*- coding: UTF-8 -*-
import md5
import os

from django.template.defaultfilters import slugify


def content_file_(instance, filename):
    ext = filename.split('.')[-1]
    filename = md5.new(slugify(filename)).hexdigest()
    filename = filename + '.' + ext
    return os.path.join('file/dev/%s/conf' % (instance.site.url,), filename)