Resources
---------

.. automodule:: salic_api.resources
    :members:

* Fornecedor

  .. autoclass:: salic_api.resources.FornecedorDetail
      :members:
  .. autoclass:: salic_api.resources.FornecedorList
      :members:
  .. autoclass:: salic_api.resources.ProdutoDetail
      :members:
  .. autoclass:: salic_api.resources.Produto
      :members:

* Incentivador

  .. autoclass:: salic_api.resources.Doacao
    :members:

  .. autoclass:: salic_api.resources.IncentivadorDetail
    :members:

  .. autoclass:: salic_api.resources.IncentivadorList
    :members:

  .. autoclass:: salic_api.resources.IncentivadorQuery
    :members:

  .. autoclass:: salic_api.resources.DoacaoQuery
    :members:

* Pre Projeto

* Projeto

* Proponente

* format_utils

  .. automethod:: salic_api.resources.format_utils.cgccpf_mask

  .. automethod:: salic_api.resources.format_utils.sanitize

* query

  .. autoclass:: salic_api.resources.Query
    :members:

* resource

  .. autoclass:: salic_api.resources.SalicResource
    :members:

  .. autoclass:: salic_api.resources.ListResource
    :members:

  .. autoclass:: salic_api.resources.DetailResource
    :members:

  .. autoclass:: salic_api.resources.InvalidResult
    :members:

* serialization

  .. automethod:: salic_api.resources.serialization.listify_queryset

  .. automethod:: salic_api.resources.serialization.serialize

  .. automethod:: salic_api.resources.serialization.convert_atom

  .. automethod:: salic_api.resources.serialization.convert_object

  .. automethod:: salic_api.resources.serialization.to_xml

  .. automethod:: salic_api.resources.serialization.to_json

  .. automethod:: salic_api.resources.serialization.to_csv

* test_resource

  .. autoclass:: salic_api.resources.TestResource
    :members:
