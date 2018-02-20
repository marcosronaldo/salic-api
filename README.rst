.. image:: https://travis-ci.org/lappis-unb/salic-api.svg?branch=master
   :target: https://travis-ci.org/lappis-unb/salic-api
   :alt: Build status

.. image:: https://codecov.io/gh/lappis-unb/salic-api/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/lappis-unb/salic-api
   :alt: Code coverage

.. image:: https://media.readthedocs.org/static/projects/badges/passing.svg
   :target: http://salic-api.readthedocs.io/pt/latest/
   :alt: Documentation

.. image:: https://api.codeclimate.com/v1/badges/864270a3891b6750927e/maintainability
   :target: https://codeclimate.com/github/lappis-unb/salic-api/maintainability
   :alt: Maintainability


API aberta para o sistema
`SALIC <http://salic.cultura.gov.br/cidadao/consultar>`_. Tem por
objetivo expor os dados de projetos da lei Rouanet.

A documentação da API pode ser acessada
`aqui <http://api.salic.cultura.gov.br/doc/>`_.

O projeto ainda se encontra em fase de **homologação**, sujeito ainda a muitas
alterações, reformulações e atualizacões.


Requisitos
----------

A aplicação foi testada em ambientes LINUX com distribuições Debian, Archlinux e
Ubuntu. A implantação é feita utilizando Docker/Docker Compose ou Docker/Rancher.
O ambiente de desenvolvimento utiliza uma conexão com um banco de dados local
em Sqlite, onde podemos testar a aplicação com dados sintéticos.

A instância principal do Salic-API se conecta no banco de dados MS SQL Server
no Ministério da Cultura.


Instalação
----------

Recomendamos que o desenvolvimento seja feito no virtualenv.

Virtualenv
~~~~~~~~~~

Git clone + virtualenv + pip:

Instale o virtualenvwrapper::

    $ sudo apt-get install virtualenvwrapper
    $ virtualenvwrapper.sh
    $ source `which virtualenvwrapper.sh`
    $ mkvirtualenv -p /usr/bin/python3 salic-api
    $ workon salic-api

Clone o repositorio::

    $ git clone https://github.com/lappis-unb/salic-api

Instale as dependencias::

    $ python setup.py develop
    $ pip install -e ".[dev]"

Inicialize o banco de desenvolvimento antes de rodar a aplicação::

    $ inv db -f
    $ inv run

Não esqueça de rodar os testes com frequência::

    $ pytest --cov

Docker
~~~~~~

A implantação será feita em Docker. Para testar o ambiente de homologação execute
dentro do diretório do salic-api::

    $ docker built -t salic-api .
    $ docker run -it --name salic-api -p 5000:5000 -v $PWD:/app salic-api



Dependências básicas
~~~~~~~~~~~~~~~~~~~~

-  ``python-dev``
-  ``python-pip``
-  ``freetds-dev``
-  ``libxml2-dev``
-  ``libxslt1-dev``
-  ``libz-dev``


Configuração
------------

Edite o arquivo **salic-api/app/example_config.py** de acordo com seu
ambiente. Edite o arquivo **salic-api/app/general_config.py** apontando
o arquivo de configuração a ser usado.


Licença
-------

Licensed under the `GPL
License <http://www.gnu.org/licenses/gpl.html>`__.

.. |Open Source Love| image:: https://badges.frapsoft.com/os/v1/open-source.svg?v=102
   :target: https://github.com/ellerbrock/open-source-badge/
.. |Open Source Love| image:: https://badges.frapsoft.com/os/gpl/gpl.svg?v=102
   :target: http://www.gnu.org/licenses/gpl.html
