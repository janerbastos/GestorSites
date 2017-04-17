# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render


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
                try:
                    url_next = request.GET['next']
                except:
                    pass
                return redirect(url_next)
            else:
                messages.warning(request, 'Conta de usuário esta bloqueada para acessar ao sistema.', 'alert-success')
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