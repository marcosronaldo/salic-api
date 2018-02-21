Changelog
=========

0.1.0
-----

Refatoração massiva com relação à versão anterior utilizada no MinC. Primeira
versão do LAPPIS.

* Converteu projeto para o Python 3.
* Atualizou para a última versão do Flask
* Conecta em banco de dados Sqlite durante desenvolvimento
* Refatoração para evitar duplicação de código
* Adotou esquema de versionamento semver
* Alterações de código e melhorias de estilo
* Suite de testes baseada no Pytest
* Documentação no Sphinx
* Integração contínua para monitoramento de testes (travis-ci.org), monitoramento de
  cobertura (codecov.io), métricas de qualidade de código (codeclimate.com) e
  geração automática de documentação (readthedocs.org)
* Docker e Docker compose para implantação utilizando NGNIX + GUnicorn
* Converteu parte das strings de SQL para o ORM do SQL Alchemy
