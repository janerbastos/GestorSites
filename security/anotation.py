# -*- encoding: utf-8 -*-

from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from manage_main.models import GrupoPapel


def __path_to__(request):
    messages.warning(request, 'Usuário sem premissão para acessar essa pagina', 'alert-danger')
    url = ''
    try:
        url = '?next='+request.path
    except:
        pass
    return url

class permission_group(object):
    def __init__(self, grupo, sistema, login_url='config'):
        self.login_url = login_url
        self.grupo = grupo
        self.sistema = sistema
        
    def __call__(self, f):
        def wrapped_f(request, *args, **kwargs):
            user = request.user
            try:
                permissao = request.session['permissao']
                if self.grupo in permissao[str(user.id)] and user.is_authenticated():
                    return f(request, *args, **kwargs)
                else:
                    return redirect(self.login_url+__path_to__(request))
            except:
                return redirect(self.login_url+__path_to__(request))
        return wrapped_f

class permission_sistema(object):
    def __init__(self, sistema, login_url='config'):
        self.login_url = login_url
        self.sistema = sistema
        
    def __call__(self, f):
        def wrapped_f(request, *args, **kwargs):
            user = request.user
            try:
                sistema = request.session['sistema']
                if sistema[str(user.id)] == self.sistema and user.is_authenticated():
                    return f(request, *args, **kwargs)
                else:
                    return redirect(self.login_url+__path_to__(request))
            except:
                return redirect(self.login_url+__path_to__(request))
        return wrapped_f

class permission_content(object):
    def __init__(self, tipo, permissao, login_url='config'):
        self.login_url = login_url
        self.content = tipo
        self.permissao = permissao
        
    def __call__(self, f):
        def wrapped_f(request, *args, **kwargs):
            flag = False
            user = User.objects.filter(is_superuser=True)
            if user:
                return f(request, *args, **kwargs) 
            try:
                permissoes = request.session['permissao']
                for key, _contents in permissoes.items():
                    if self.content in _contents:
                        papeis = GrupoPapel.objects.get(grupo__grupo_name=key).papeis.all()
                        papel = papeis.get(content_type__tipo=self.content, cod_name=self.permissao)
                        flag = True
                        break
                if flag:
                    return f(request, *args, **kwargs)                
                else:
                    return redirect(self.login_url+__path_to__(request))
            except:
                return redirect(self.login_url+__path_to__(request))
        return wrapped_f

class permission_notroot(object):
    def __init__(self, login_url='config'):
        self.login_url = login_url
    
    def __call__(self, f):
        def wrapped_f(request, *args, **kwargs):
            user = User.objects.filter(is_superuser=True)
            if not user:
                return f(request, *args, **kwargs)
            else:
                return redirect(self.login_url)
        return wrapped_f

class permission_root(object):
    def __init__(self, login_url='config'):
        self.login_url = login_url
    
    def __call__(self, f):
        def wrapped_f(request, *args, **kwargs):
            user = request.user
            if user.is_superuser:
                return f(request, *args, **kwargs)
            else:
                return redirect(self.login_url+__path_to__(request))
        return wrapped_f