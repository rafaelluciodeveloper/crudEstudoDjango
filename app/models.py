# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.datetime_safe import datetime


class Carro(models.Model):
    nome_propietario = models.CharField(max_length=100, null=False)
    modelo = models.CharField(max_length=50,null=False)
    marca = models.CharField(max_length=50, null=False)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(2000)], null=False)
    valor = models.FloatField(null=False)
    data_cadastro = models.DateTimeField(default=datetime.now(), null=False)
