# coding=utf-8
from salic_api.models import Usuarios


def usuarios_example():
    return [Usuarios(
        usu_codigo=1,
        usu_nome='nome',
    )]