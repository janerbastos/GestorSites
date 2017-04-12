from django.conf import settings
import os

def handle_uploaded_file(f, site, tipo):
    if tipo == 'html':
        _path = "%s/portalufopa/templates/comum/index-%s.%s" % (unicode(settings.BASE_DIR), site, tipo)
    else:
        _path = "%s/portalufopa/static/css/%s-custom.%s" % (unicode(settings.BASE_DIR), site, tipo)
        
    with open(_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
def is_file_exist(_file, tipo):
    _status = False
    if tipo == 'html':
        _path = "%s/portalufopa/templates/comum/%s" % (unicode(settings.BASE_DIR), _file)
        _status = os.path.exists(_path)
       
    if tipo == 'css':
        _path = "%s/portalufopa/static/css/%s" % (unicode(settings.BASE_DIR), _file)
        _status = os.path.exists(_path)
    
    return _status


def excluir_file(_file, tipo):
    _status = False
    if tipo == 'html':
        _path = "%s/portalufopa/templates/comum/%s" % (unicode(settings.BASE_DIR), _file)
        _status = os.remove(_path)
       
    if tipo == 'css':
        _path = "%s/portalufopa/static/css/%s" % (unicode(settings.BASE_DIR), _file)
        _status = os.remove(_path)
    
    return _status