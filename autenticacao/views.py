from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect


@login_required
def registrar_usuario(request, template_name="usuario_form.html"):
    user = request.user
    if user.is_staff:
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            tipo = request.POST['tipo_usuario']
            if tipo == "administrador":
                    user = User.objects.create_user(username, email, password)
                    user.is_staff = True
                    user.save()
            else:
                    user = User.objects.create_user (username, email, password)
            return redirect('listar_usuario')
    else:
        messages.error(request, 'Permisão Negada')
        return redirect('/listar_usuario/')
    return render(request, template_name, {})

@login_required
def listar_usuario(request, template_name='usuario_list.html'):
    query = request.GET.get('busca')
    if query:
        usuario = User.objects.filter(username__icontains=query)
    else:
        usuario = User.objects.all()
    usuarios = {'lista': usuario}
    return render(request, template_name, usuarios)

@login_required
def remover_usuario(request, pk, template_name='usuario_delete.html'):
    user = request.user
    if user.has_perm('user.delete_user'):
        try:
            usuario = User.objects.get(pk = pk)
            if request.method == "POST":
                usuario.delete()
                return redirect('/listar_usuario/')
        except:
            messages.error(request, 'Usuario Não Encontrado')
            return redirect('/listar_usuario/')
    else:
        messages.error(request, 'Permisão Negada')
        return redirect('/listar_usuario/')
    return render(request,template_name,{'usuario':usuario})


def logar(request, template_name="login.html"):
    next = request.GET.get('next', '/listar_usuario/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(next)
        else:
            messages.error(request,'Usuário ou Senha Incorretos')
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request,template_name, {'redirect_to': next})


def deslogar(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)
