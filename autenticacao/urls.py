from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^registrar_usuario/$', registrar_usuario, name='registrar_usuario'),
    url(r'^listar_usuario/$', listar_usuario,name='listar_usuario'),
    url(r'^remover_usuario/(?P<pk>[0-9]+)', remover_usuario, name='remover_usuario'),
    url(r'^logar/$', logar, name='logar'),
    url(r'^deslogar/$', deslogar, name='deslogar')

]