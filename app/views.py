# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import *


class CarroForm(ModelForm):
    class Meta:
        model = Carro
        fields = ['nome_propietario', 'modelo', 'marca', 'ano', 'valor', 'data_cadastro']

@login_required
def cadastrar_carro(request, template_name='carro_form.html'):
    user = request.user
    if user.is_staff :
        form = CarroForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect('listar_carro')
    else:
        messages.error(request,'Permisão Negada')
        return redirect('/listar_carro/')
    return render(request, template_name, {'form': form})

@login_required
def listar_carro(request, template_name='carro_list.html'):
    query = request.GET.get('busca')
    if query:
        carro = Carro.objects.filter(modelo__icontains=query)
    else:
        carro = Carro.objects.all()
    carros = {'lista': carro}
    return render(request, template_name, carros)

@login_required
def editar_carro(request,pk,template_name='carro_form.html'):
    user = request.user
    if user.is_staff :
        carro = get_object_or_404(Carro, pk=pk)
        if request.method == "POST":
            form = CarroForm(request.POST, instance = carro)
            if form.is_valid():
                form.save()
                return redirect('listar_carro')
            else:
                form = CarroForm(instance=carro)
    else:
        messages.error(request,'Permisão Negada')
        return redirect('/listar_carro/')
    return render(request,template_name, {'form': form})

@login_required
def remover_carro(request,pk,template_name='carro_delete.html'):
    user = request.user
    if user.has_perm('user.delete_user'):
        try:
            carro = Carro.objects.get(pk=pk)
            if request.method == "POST":
                carro.delete()
                return redirect('listar_carro')
        except:
            messages.error(request, 'Usuário Não Encontrado')
            return redirect('/listar_carro/')
    else:
        messages.error(request, 'Permissão Negada')
        return redirect('/listar_carro/')
    return render(request,template_name,{'carro':carro})