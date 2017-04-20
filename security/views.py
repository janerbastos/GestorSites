# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from manage_main.models import UserSite, GrupoPapel


def _login(request):
    request.session['action'] = None
    template = 'security/login.html'
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        url_next = 'portais:login'
        if user:
            if user.is_active:
                login(request, user)
                contents = []
                permissoes={}
                try:
                    url_next = request.GET['next']
                    site_url = url_next.strip('/').split('/')[0]
                    permissoes['site'] = site_url
                    permissao_contents = UserSite.objects.filter(site__url=site_url).get(user=user)
                    permissao_contents = permissao_contents.grupo.all()
                    for g in permissao_contents:
                        grupo_papeis = GrupoPapel.objects.get(grupo=g)
                        contents = list(grupo_papeis.papeis.distinct().values_list('content_type__tipo', flat=True))
                        permissoes[g.grupo_name] = contents
                    request.session['permissao'] = permissoes
                except:
                    print 'Site não encontrado'
                    
                return redirect(url_next)
            else:
                messages.warning(request, 'Conta de usuário esta bloqueada para acessar o sistema.', 'alert-warning')
        else:
            messages.warning(request, 'Usuário ou senha invalida! Corrija e tente novamente.', 'alert-warning')
    return render(request, template, context)

@login_required(login_url='/security/login/')
def _logout(request):
    messages.warning(request, 'Sessão encerrada com sucesso.', 'alert-success')
    logout(request)
    try:
        _next = request.GET['next']
        return redirect(_next)
    except:
        return redirect('/security/login')