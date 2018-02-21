# coding=utf-8
from salic_api.models import Usuarios


def usuarios_example(size=1):
    return [Usuarios(
        usu_codigo=i,
        usu_nome='nome%s' %i,)
        for i in range(1, size+1)
    ]
