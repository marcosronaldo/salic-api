from sqlalchemy import case, func, and_, or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import coalesce

from ..model_base import QueryBase
from ..serialization import listify_queryset
from ..shared_models import (
    Projeto, Interessado, Mecanismo, Situacao, Enquadramento, PreProjeto,
    Captacao, CertidoesNegativas, Verificacao, PlanoDistribuicao, Produto, Area,
    Segmento, Custos)
from ...utils.timer import timer


class ProjetoModelObject(QueryBase):
    #
    # SQL procedures
    #
    use_sql_procedures = False

    def _result(self, field, PRONAC):
        return self.sql_connector.session.query(
            getattr(Custos, field),
        ).filter(Custos.idProjeto == PRONAC).as_scalar()

    def valor_proposta(self, PRONAC):
        if self.use_sql_procedures:
            return func.sac.dbo.fnValorDaProposta(PRONAC)
        return self._result('valor_proposta', PRONAC)

    def valor_solicitado(self, PRONAC, sequencial):
        if self.use_sql_procedures:
            return func.sac.dbo.fnValorSolicitado(PRONAC, sequencial)
        return self._result('valor_solicitado', PRONAC)

    def valor_aprovado(self, PRONAC, sequencial):
        if self.use_sql_procedures:
            return func.sac.dbo.fnValorAprovado(PRONAC, sequencial)
        return self._result('valor_aprovado', PRONAC)

    def valor_aprovado_convenio(self, PRONAC, sequencial):
        if self.use_sql_procedures:
            return func.sac.dbo.fnValorAprovadoConvenio(PRONAC, sequencial)
        return self._result('valor_aprovado_convenio', PRONAC)

    def custo_projeto(self, PRONAC, sequencial):
        if self.use_sql_procedures:
            return func.sac.dbo.fnCustoProjeto(PRONAC, sequencial)
        return self._result('custo_projeto', PRONAC)

    def outras_fontes(self, PRONAC):
        if self.use_sql_procedures:
            return func.sac.dbo.fnOutrasFontes(PRONAC)
        return self._result('outras_fontes', PRONAC)

    #
    # Queries
    #
    def attached_documents(self, idPronac):
        query = text("""SAC.dbo.paDocumentos :idPronac""")
        return self.sql_connector.session.execute(query, {
            'idPronac': idPronac
        }).fetchall()

    def attached_brands(self, idPronac):

        query = text("""
                    SELECT a.idArquivo as id_arquivo, a.nmArquivo as nome_arquivo, a.dtEnvio as data_envio, d.idDocumento as id_documento, CAST(dsDocumento AS TEXT) AS descricao
                    FROM BDCORPORATIVO.scCorp.tbArquivoImagem AS ai
                    INNER JOIN BDCORPORATIVO.scCorp.tbArquivo AS a ON ai.idArquivo = a.idArquivo
                    INNER JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON a.idArquivo = d.idArquivo
                    INNER JOIN BDCORPORATIVO.scCorp.tbDocumentoProjeto AS dp ON dp.idDocumento = d.idDocumento
                    INNER JOIN SAC.dbo.Projetos AS p ON dp.idPronac = p.IdPRONAC WHERE (dp.idTipoDocumento = 1) AND (p.idPronac = :IdPRONAC)
        """)
        return self.sql_connector.session.execute(query, {
            'IdPRONAC': idPronac
        }).fetchall()

    def postpone_request(self, idPronac):

        query = text("""
                    SELECT a.DtPedido as data_pedido, a.DtInicio as data_inicio, a.DtFinal as data_final, a.Observacao as observacao, a.Atendimento as atendimento,
                        CASE
                            WHEN Atendimento = 'A'
                                THEN 'Em analise'
                            WHEN Atendimento = 'N'
                                THEN 'Deferido'
                            WHEN Atendimento = 'I'
                                THEN 'Indeferido'
                            WHEN Atendimento = 'S'
                                THEN 'Processado'
                            END as estado
                        , b.usu_nome AS usuario FROM prorrogacao AS a
                        LEFT JOIN TABELAS.dbo.Usuarios AS b ON a.Logon = b.usu_codigo WHERE (idPronac = :IdPRONAC)
        """)

        return self.sql_connector.session.execute(query, {
            'IdPRONAC': idPronac
        }).fetchall()

    def payments_listing(self, limit=None, offset=None, idPronac=None,
                         cgccpf=None):
        # Relação de pagamentos

        if idPronac != None:

            if limit == None:
                query = text("""
                        SELECT
                                d.Descricao as nome,
                                b.idComprovantePagamento as id_comprovante_pagamento,
                                a.idPlanilhaAprovacao as id_planilha_aprovacao,
                                g.CNPJCPF as cgccpf,
                                e.Descricao as nome_fornecedor,
                                b.DtPagamento as data_aprovacao,
                                CASE tpDocumento
                                    WHEN 1 THEN ('Boleto Bancario')
                                    WHEN 2 THEN ('Cupom Fiscal')
                                    WHEN 3 THEN ('Guia de Recolhimento')
                                    WHEN 4 THEN ('Nota Fiscal/Fatura')
                                    WHEN 5 THEN ('Recibo de Pagamento')
                                    WHEN 6 THEN ('RPA')
                                    ELSE ''
                                END as tipo_documento,
                                b.nrComprovante as nr_comprovante,
                                b.dtEmissao as data_pagamento,
                                CASE
                                  WHEN b.tpFormaDePagamento = '1'
                                     THEN 'Cheque'
                                  WHEN b.tpFormaDePagamento = '2'
                                     THEN 'Transferencia Bancaria'  WHEN b.tpFormaDePagamento = '3'
                                     THEN 'Saque/Dinheiro'
                                     ELSE ''
                                END as tipo_forma_pagamento,
                                b.nrDocumentoDePagamento nr_documento_pagamento,
                                a.vlComprovado as valor_pagamento,
                                b.idArquivo as id_arquivo,
                                b.dsJustificativa as justificativa,
                                f.nmArquivo as nm_arquivo FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (c.idPronac = :idPronac)

                                ORDER BY data_pagamento
                                """
                             )

            else:
                query = text("""
                        SELECT
                                d.Descricao as nome,
                                b.idComprovantePagamento as id_comprovante_pagamento,
                                a.idPlanilhaAprovacao as id_planilha_aprovacao,
                                g.CNPJCPF as cgccpf,
                                e.Descricao as nome_fornecedor,
                                b.DtPagamento as data_aprovacao,
                                CASE tpDocumento
                                    WHEN 1 THEN ('Boleto Bancario')
                                    WHEN 2 THEN ('Cupom Fiscal')
                                    WHEN 3 THEN ('Guia de Recolhimento')
                                    WHEN 4 THEN ('Nota Fiscal/Fatura')
                                    WHEN 5 THEN ('Recibo de Pagamento')
                                    WHEN 6 THEN ('RPA')
                                    ELSE ''
                                END as tipo_documento,
                                b.nrComprovante as nr_comprovante,
                                b.dtEmissao as data_pagamento,
                                CASE
                                  WHEN b.tpFormaDePagamento = '1'
                                     THEN 'Cheque'
                                  WHEN b.tpFormaDePagamento = '2'
                                     THEN 'Transferencia Bancaria'  WHEN b.tpFormaDePagamento = '3'
                                     THEN 'Saque/Dinheiro'
                                     ELSE ''
                                END as tipo_forma_pagamento,
                                b.nrDocumentoDePagamento nr_documento_pagamento,
                                a.vlComprovado as valor_pagamento,
                                b.idArquivo as id_arquivo,
                                b.dsJustificativa as justificativa,
                                f.nmArquivo as nm_arquivo FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (c.idPronac = :idPronac)

                                ORDER BY data_pagamento
                                OFFSET :offset ROWS
                                FETCH NEXT :limit ROWS ONLY;

                                """
                             )

            return self.sql_connector.session.execute(query, {
                'idPronac': idPronac, 'offset': offset, 'limit': limit
            }).fetchall()

        else:

            if limit == None:
                query = text("""
                        SELECT
                                d.Descricao as nome,
                                b.idComprovantePagamento as id_comprovante_pagamento,
                                a.idPlanilhaAprovacao as id_planilha_aprovacao,
                                g.CNPJCPF as cgccpf,
                                e.Descricao as nome_fornecedor,
                                b.DtPagamento as data_aprovacao,
                                Projetos.AnoProjeto + Projetos.Sequencial as PRONAC,
                                CASE tpDocumento
                                    WHEN 1 THEN ('Boleto Bancario')
                                    WHEN 2 THEN ('Cupom Fiscal')
                                    WHEN 3 THEN ('Guia de Recolhimento')
                                    WHEN 4 THEN ('Nota Fiscal/Fatura')
                                    WHEN 5 THEN ('Recibo de Pagamento')
                                    WHEN 6 THEN ('RPA')
                                    ELSE ''
                                END as tipo_documento,
                                b.nrComprovante as nr_comprovante,
                                b.dtEmissao as data_pagamento,
                                CASE
                                  WHEN b.tpFormaDePagamento = '1'
                                     THEN 'Cheque'
                                  WHEN b.tpFormaDePagamento = '2'
                                     THEN 'Transferencia Bancaria'  WHEN b.tpFormaDePagamento = '3'
                                     THEN 'Saque/Dinheiro'
                                     ELSE ''
                                END as tipo_forma_pagamento,
                                b.nrDocumentoDePagamento nr_documento_pagamento,
                                a.vlComprovado as valor_pagamento,
                                b.idArquivo as id_arquivo,
                                b.dsJustificativa as justificativa,
                                f.nmArquivo as nm_arquivo FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                JOIN SAC.dbo.Projetos AS Projetos ON c.idPronac = Projetos.IdPRONAC
                                LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (g.CNPJCPF LIKE :cgccpf)

                                ORDER BY data_pagamento

                                """
                             )

            else:
                query = text("""
                            SELECT
                                    d.Descricao as nome,
                                    b.idComprovantePagamento as id_comprovante_pagamento,
                                    a.idPlanilhaAprovacao as id_planilha_aprovacao,
                                    g.CNPJCPF as cgccpf,
                                    e.Descricao as nome_fornecedor,
                                    b.DtPagamento as data_aprovacao,
                                    Projetos.AnoProjeto + Projetos.Sequencial as PRONAC,
                                    CASE tpDocumento
                                        WHEN 1 THEN ('Boleto Bancario')
                                        WHEN 2 THEN ('Cupom Fiscal')
                                        WHEN 3 THEN ('Guia de Recolhimento')
                                        WHEN 4 THEN ('Nota Fiscal/Fatura')
                                        WHEN 5 THEN ('Recibo de Pagamento')
                                        WHEN 6 THEN ('RPA')
                                        ELSE ''
                                    END as tipo_documento,
                                    b.nrComprovante as nr_comprovante,
                                    b.dtEmissao as data_pagamento,
                                    CASE
                                      WHEN b.tpFormaDePagamento = '1'
                                         THEN 'Cheque'
                                      WHEN b.tpFormaDePagamento = '2'
                                         THEN 'Transferencia Bancaria'  WHEN b.tpFormaDePagamento = '3'
                                         THEN 'Saque/Dinheiro'
                                         ELSE ''
                                    END as tipo_forma_pagamento,
                                    b.nrDocumentoDePagamento nr_documento_pagamento,
                                    a.vlComprovado as valor_pagamento,
                                    b.idArquivo as id_arquivo,
                                    b.dsJustificativa as justificativa,
                                    f.nmArquivo as nm_arquivo FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                    INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                    LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                    LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                    LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                    LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                    JOIN SAC.dbo.Projetos AS Projetos ON c.idPronac = Projetos.IdPRONAC
                                    LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (g.CNPJCPF LIKE :cgccpf)

                                    ORDER BY data_pagamento
                                    OFFSET :offset ROWS
                                    FETCH NEXT :limit ROWS ONLY;

                                    """
                             )

            return self.sql_connector.session.execute(query, {
                'cgccpf': '%' + cgccpf + '%', 'offset': offset, 'limit': limit
            }).fetchall()

    def payments_listing_count(self, idPronac=None, cgccpf=None):
        # Número de pagamentos/produtos

        if idPronac != None:

            query = text("""
                        SELECT
                                COUNT(b.idArquivo) AS total

                                FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (c.idPronac = :idPronac)
                                """
                         )
            result = self.sql_connector.session.execute(
                query, {'idPronac': idPronac}).fetchall()

        else:
            query = text("""
                        SELECT
                                COUNT(b.idArquivo) AS total

                                FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                                INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                                LEFT JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                                LEFT JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                                LEFT JOIN Agentes.dbo.Nomes AS e ON b.idFornecedor = e.idAgente
                                LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS f ON b.idArquivo = f.idArquivo
                                JOIN SAC.dbo.Projetos AS Projetos ON c.idPronac = Projetos.IdPRONAC
                                LEFT JOIN Agentes.dbo.Agentes AS g ON b.idFornecedor = g.idAgente WHERE (g.CNPJCPF LIKE :cgccpf)
                                """
                         )

            result = self.sql_connector.session.execute(
                query, {'cgccpf': '%' + cgccpf + '%'}).fetchall()

        n_records = listify_queryset(result)

        return n_records[0]['total']

    def taxing_report(self, idPronac):
        # Relatório fisco

        query = text("""
                    SELECT
                    f.idPlanilhaEtapa as id_planilha_etapa,
                    f.Descricao AS etapa,
                    d.Descricao AS item,
                    g.Descricao AS unidade,
                    (c.qtItem*nrOcorrencia) AS qtd_programada,
                    (c.qtItem*nrOcorrencia*c.vlUnitario) AS valor_programado,

                        CASE c.qtItem*nrOcorrencia*c.vlUnitario
                            WHEN 0 then NULL
                            ELSE ROUND(sum(b.vlComprovacao) / (c.qtItem*nrOcorrencia*c.vlUnitario) * 100, 2)
                        END AS perc_executado,

                        CASE c.qtItem*nrOcorrencia*c.vlUnitario
                            WHEN 0 then NULL
                            ELSE ROUND(100 - (sum(b.vlComprovacao) / (c.qtItem*nrOcorrencia*c.vlUnitario) * 100), 2)
                        END AS perc_a_executar,

                    (sum(b.vlComprovacao)) AS valor_executado
                 FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                 INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                 INNER JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                 INNER JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                 INNER JOIN SAC.dbo.tbPlanilhaEtapa AS f ON c.idEtapa = f.idPlanilhaEtapa
                 INNER JOIN SAC.dbo.tbPlanilhaUnidade AS g ON c.idUnidade= g.idUnidade WHERE (c.idPronac = :IdPRONAC) GROUP BY c.idPronac,
                    f.Descricao,
                    d.Descricao,
                    g.Descricao,
                    c.qtItem,
                    nrOcorrencia,
                    c.vlUnitario,
                    f.idPlanilhaEtapa
                    """
                     )

        return self.sql_connector.session.execute(query, {
            'IdPRONAC': idPronac
        }).fetchall()

    def goods_capital_listing(self, idPronac):
        # Relação de bens de capital

        query = text("""
                    SELECT
                    CASE
                        WHEN tpDocumento = 1 THEN 'Boleto Bancario'
                        WHEN tpDocumento = 2 THEN 'Cupom Fiscal'
                        WHEN tpDocumento = 3 THEN 'Nota Fiscal / Fatura'
                        WHEN tpDocumento = 4 THEN 'Recibo de Pagamento'
                        WHEN tpDocumento = 5 THEN 'RPA'
                    END as Titulo,
                    b.nrComprovante,
                    d.Descricao as Item,
                    DtEmissao as dtPagamento,
                    dsItemDeCusto Especificacao,
                    dsMarca as Marca,
                    dsFabricante as Fabricante,
                    (c.qtItem*nrOcorrencia) as Qtde,
                    c.vlUnitario,
                    (c.qtItem*nrOcorrencia*c.vlUnitario) as vlTotal
                 FROM BDCORPORATIVO.scSAC.tbComprovantePagamentoxPlanilhaAprovacao AS a
                 INNER JOIN BDCORPORATIVO.scSAC.tbComprovantePagamento AS b ON a.idComprovantePagamento = b.idComprovantePagamento
                 INNER JOIN SAC.dbo.tbPlanilhaAprovacao AS c ON a.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                 INNER JOIN SAC.dbo.tbPlanilhaItens AS d ON c.idPlanilhaItem = d.idPlanilhaItens
                 INNER JOIN BDCORPORATIVO.scSAC.tbItemCusto AS e ON e.idPlanilhaAprovacao = c.idPlanilhaAprovacao
                 WHERE (c.idPronac = :IdPRONAC)
        """)

        return self.sql_connector.session.execute(query, {
            'IdPRONAC': idPronac
        }).fetchall()

    def all(self, limit, offset, PRONAC=None, nome=None, proponente=None,
            cgccpf=None, area=None, segmento=None,
            UF=None, municipio=None, data_inicio=None,
            data_inicio_min=None, data_inicio_max=None,
            data_termino=None, data_termino_min=None,
            data_termino_max=None, year=None, sort_field=None,
            sort_order=None):

        text_fields = (
            PreProjeto.Acessibilidade.label('acessibilidade'),
            PreProjeto.Objetivos.label('objetivos'),
            PreProjeto.Justificativa.label('justificativa'),
            PreProjeto.DemocratizacaoDeAcesso.label('democratizacao'),
            PreProjeto.EtapaDeTrabalho.label('etapa'),
            PreProjeto.FichaTecnica.label('ficha_tecnica'),
            PreProjeto.ResumoDoProjeto.label('resumo'),
            PreProjeto.Sinopse.label('sinopse'),
            PreProjeto.ImpactoAmbiental.label('impacto_ambiental'),
            PreProjeto.EspecificacaoTecnica.label('especificacao_tecnica'),
            PreProjeto.EstrategiadeExecucao.label('estrategia_execucao'),
            Projeto.ProvidenciaTomada.label('providencia'),
        )

        year = Projeto.AnoProjeto
        sequential = Projeto.Sequencial
        valor_solicitado = self.valor_solicitado(year, sequential)
        valor_proposta = self.valor_proposta(Projeto.idProjeto)
        outras_fontes = self.outras_fontes(Projeto.IdPRONAC)
        valor_proposta_case = coalesce(valor_proposta, valor_solicitado)
        valor_aprovado = self.valor_aprovado(year, sequential)
        valor_aprovado_convenio = self.valor_aprovado_convenio(year, sequential)
        custo_projeto = self.custo_projeto(year, sequential)

        # Human friendly values
        mecanismo = Projeto.Mecanismo
        mecanismos_convenio = or_(mecanismo == '2', mecanismo == '6')
        valor_aprovado_case = case(
            [(mecanismos_convenio, valor_aprovado_convenio)],
            else_=valor_aprovado,
        )
        valor_projeto = case(
            [(mecanismos_convenio, valor_aprovado_convenio)],
            else_=valor_aprovado + outras_fontes,
        )
        enquadramento = Enquadramento.Enquadramento
        enquadramento = case(
            [
                (enquadramento == '1', 'Artigo 26'),
                (enquadramento == '2', 'Artigo 18'),
            ],
            else_='Nao enquadrado',
        )

        sort_mapping_fields = {
            'valor_solicitado': valor_solicitado,
            'PRONAC': Projeto.PRONAC,
            'outras_fontes': outras_fontes,
            'valor_captado': custo_projeto,
            'valor_proposta': valor_proposta_case,
            'valor_aprovado_case': valor_aprovado_case,
            'valor_projeto': valor_projeto,
            'ano_projeto': year,
            'data_inicio': Projeto.DtInicioExecucao,
            'data_termino': Projeto.DtFimExecucao,
        }

        if sort_field is None:
            sort_field = 'ano_projeto'
        sort_order = 'desc'

        sort_field = sort_mapping_fields[sort_field]

        with timer(action='db query: projetos_list'):
            res = self.sql_connector.session.query(
                Projeto.NomeProjeto.label('nome'),
                Projeto.PRONAC.label('PRONAC'),
                year.label('ano_projeto'),
                Projeto.UfProjeto.label('UF'),
                Interessado.Cidade.label('municipio'),
                Projeto.DtInicioExecucao.label('data_inicio'),
                Projeto.DtFimExecucao.label('data_termino'),
                Projeto.IdPRONAC,
                Area.Descricao.label('area'),
                Segmento.Descricao.label('segmento'),
                Situacao.Descricao.label('situacao'),
                Interessado.Nome.label('proponente'),
                Interessado.CgcCpf.label('cgccpf'),
                Mecanismo.Descricao.label('mecanismo'),
                valor_solicitado.label('valor_solicitado'),
                outras_fontes.label('outras_fontes'),
                custo_projeto.label('valor_captado'),
                valor_proposta_case.label('valor_proposta'),
                valor_aprovado_case.label('valor_aprovado_case'),
                valor_projeto.label('valor_projeto'),
                enquadramento.label('enquadramento'),
                *text_fields
            )
        res = res.join(Area) \
            .join(Segmento) \
            .join(Situacao) \
            .join(Interessado) \
            .join(PreProjeto) \
            .join(Mecanismo) \
            .outerjoin(Enquadramento,
                       Enquadramento.IdPRONAC == Projeto.IdPRONAC)

        if PRONAC is not None:
            res = res.filter(Projeto.PRONAC == PRONAC)
        if area is not None:
            res = res.filter(Area.Codigo == area)
        if segmento is not None:
            res = res.filter(Segmento.Codigo == segmento)
        if proponente is not None:
            res = res.filter(Interessado.Nome.like('%' + proponente + '%'))
        if cgccpf is not None:
            res = res.filter(Interessado.CgcCpf.like('%' + cgccpf + '%'))
        if nome is not None:
            res = res.filter(Projeto.NomeProjeto.like('%' + nome + '%'))
        if UF is not None:
            res = res.filter(Interessado.Uf == UF)
        if municipio is not None:
            res = res.filter(Interessado.Cidade == municipio)

        # Filter data
        data_inicio_field = Projeto.DtInicioExecucao
        if data_inicio is not None:
            res = res \
                .filter(data_inicio_field >= data_inicio) \
                .filter(data_inicio_field <= data_inicio + ' 23:59:59')
        if data_inicio_min is not None:
            res = res.filter(data_inicio_field >= data_inicio_min)
        if data_inicio_max is not None:
            res = res.filter(data_inicio_field <= data_inicio_max + ' 23:59:59')

        data_fim_field = Projeto.DtFimExecucao
        if data_termino is not None:
            res = res \
                .filter(data_fim_field >= data_termino) \
                .filter(data_fim_field <= data_termino + ' 23:59:59')
        if data_termino_min is not None:
            res = res.filter(data_fim_field >= data_termino_min)
        if data_termino_max is not None:
            res = res.filter(data_fim_field <= data_termino_max + ' 23:59:59')

        if year is not None:
            res = res.filter(year == year)

        # order by descending
        if sort_order == 'desc':
            res = res.order_by(desc(sort_field))
        # order by ascending
        else:
            res = res.order_by(sort_field)

        # res = res.order_by("AnoProjeto")

        total_records = self.count(res)
        res = res.limit(limit).offset(offset)
        return res.all(), total_records


class CaptacaoQuery(QueryBase):
    def all(self, PRONAC):
        res = self.sql_connector.session.query(
            Captacao.PRONAC,
            Captacao.CaptacaoReal.label('valor'),
            Captacao.DtRecibo.label('data_recibo'),
            Projeto.NomeProjeto.label('nome_projeto'),
            Captacao.CgcCpfMecena.label('cgccpf'),
            Interessado.Nome.label('nome_doador'),
        )
        res = res \
            .join(Projeto, Captacao.PRONAC == Projeto.PRONAC) \
            .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)

        if PRONAC is not None:
            res = res.filter(Captacao.PRONAC == PRONAC)
        return res.all()


class AreaQuery(QueryBase):
    def all(self):
        return self.sql_connector.session.query(
            Area.Descricao.label('nome'),
            Area.Codigo.label('codigo'),
        ).all()


class SegmentoQuery(QueryBase):
    def all(self):
        return self.sql_connector.session.query(
            Segmento.Descricao.label('nome'),
            Segmento.Codigo.label('codigo'),
        ).all()


class CertidoesNegativasModelObject(QueryBase):
    def __init__(self):
        super(CertidoesNegativasModelObject, self).__init__()

    def all(self, PRONAC=None, CgcCpf=None):

        code = CertidoesNegativas.CodigoCertidao
        descricao_case = case([
            (code == '49', 'Quitação de Tributos Federais'),
            (code == '51', 'FGTS'),
            (code == '52', 'INSS'),
            (code == '244', 'CADIN'),
        ])

        situacao_case = case(
            [(CertidoesNegativas.cdSituacaoCertidao == 0, 'Pendente')],
            else_='Não Pendente'
        )

        res = self.sql_connector.session.query(
            CertidoesNegativas.DtEmissao.label('data_emissao'),
            CertidoesNegativas.DtValidade.label('data_validade'),
            descricao_case.label('descricao'),
            situacao_case.label('situacao'),
        )

        if PRONAC is not None:
            res = res.filter(CertidoesNegativas.PRONAC == PRONAC)

        return res.all()


class DivulgacaoModelObject(QueryBase):
    V1 = aliased(Verificacao)
    V2 = aliased(Verificacao)

    def __init__(self):
        super(DivulgacaoModelObject, self).__init__()

    def all(self, IdPRONAC):
        stmt = text(
            """
                        SELECT v1.Descricao as peca,v2.Descricao as veiculo
                        FROM sac.dbo.PlanoDeDivulgacao d
                        INNEr JOIN sac.dbo.Projetos p on (d.idProjeto = p.idProjeto)
                        INNER JOIN sac.dbo.Verificacao v1 on (d.idPeca = v1.idVerificacao)
                        INNER JOIN sac.dbo.Verificacao v2 on (d.idVeiculo = v2.idVerificacao)
                        WHERE p.IdPRONAC=:IdPRONAC AND d.stPlanoDivulgacao = 1
                    """
        )

        return self.sql_connector.session.execute(stmt, {
            'IdPRONAC': IdPRONAC
        }).fetchall()


class DescolamentoModelObject(QueryBase):
    def __init__(self):
        super(DescolamentoModelObject, self).__init__()

    def all(self, IdPRONAC):
        stmt = text(
            """
                        SELECT
                            idDeslocamento,
                            d.idProjeto,
                            p.Descricao as PaisOrigem,
                            u.Descricao as UFOrigem,
                            m.Descricao as MunicipioOrigem,
                            p2.Descricao as PaisDestino,
                            u2.Descricao as UFDestino,
                            m2.Descricao as MunicipioDestino,
                            Qtde
                FROM
                   Sac.dbo.tbDeslocamento d
                INNER JOIN Sac.dbo.Projetos y on (d.idProjeto = y.idProjeto)
                INNER JOIN Agentes..Pais p on (d.idPaisOrigem = p.idPais)
                INNER JOIN Agentes..uf u on (d.idUFOrigem = u.iduf)
                INNER JOIN Agentes..Municipios m on (d.idMunicipioOrigem = m.idMunicipioIBGE)
                INNER JOIN Agentes..Pais p2 on (d.idPaisDestino = p2.idPais)
                INNER JOIN Agentes..uf u2 on (d.idUFDestino = u2.iduf)
                INNER JOIN Agentes..Municipios m2 on (d.idMunicipioDestino = m2.idMunicipioIBGE)
                WHERE y.idPRONAC = :IdPRONAC
                    """
        )

        return self.sql_connector.session.execute(stmt, {
            'IdPRONAC': IdPRONAC
        }).fetchall()


class DistribuicaoModelObject(QueryBase):
    def __init__(self):
        super(DistribuicaoModelObject, self).__init__()

    def all(self, IdPRONAC):
        return (
            self.sql_connector.session.query(
                PlanoDistribuicao.idPlanoDistribuicao,
                PlanoDistribuicao.QtdeVendaNormal,
                PlanoDistribuicao.QtdeVendaPromocional,
                PlanoDistribuicao.PrecoUnitarioNormal,
                PlanoDistribuicao.PrecoUnitarioPromocional,
                PlanoDistribuicao.QtdeOutros,
                PlanoDistribuicao.QtdeProponente,
                PlanoDistribuicao.QtdeProduzida,
                PlanoDistribuicao.QtdePatrocinador,
                Area.Descricao.label('area'),
                Segmento.Descricao.label('segmento'),
                Produto.Descricao.label('produto'),
                Verificacao.Descricao.label('posicao_logo'),
                Projeto.Localizacao,
            )
                .join(Projeto)
                .join(Produto)
                .join(Area, Area.Codigo == PlanoDistribuicao.Area)
                .join(Segmento, Segmento.Codigo == PlanoDistribuicao.Segmento)
                .join(Verificacao)
                .filter(and_(Projeto.IdPRONAC == IdPRONAC,
                             PlanoDistribuicao.stPlanoDistribuicaoProduto == 1))
                .all()
        )


class ReadequacaoModelObject(QueryBase):
    def __init__(self):
        super(ReadequacaoModelObject, self).__init__()

    def all(self, IdPRONAC):
        stmt = text(
            """
            SELECT
                a.idReadequacao as id_readequacao,
                a.dtSolicitacao as data_solicitacao,
                CAST(a.dsSolicitacao AS TEXT) AS descricao_solicitacao,
                CAST(a.dsJustificativa AS TEXT) AS descricao_justificativa,
                a.idSolicitante AS id_solicitante,
                a.idAvaliador AS id_avaliador,
                a.dtAvaliador AS data_avaliador,
                CAST(a.dsAvaliacao AS TEXT) AS descricao_avaliacao,
                a.idTipoReadequacao AS id_tipo_readequacao,
                CAST(c.dsReadequacao AS TEXT) AS descricao_readequacao,
                a.stAtendimento AS st_atendimento,
                a.siEncaminhamento AS si_encaminhamento,
                CAST(b.dsEncaminhamento AS TEXT) AS descricao_encaminhamento,
                a.stEstado AS st_estado,
                e.idArquivo AS is_arquivo,
                e.nmArquivo AS nome_arquivo
             FROM SAC.dbo.tbReadequacao AS a
             INNER JOIN SAC.dbo.tbTipoEncaminhamento AS b ON a.siEncaminhamento = b.idTipoEncaminhamento INNER JOIN SAC.dbo.tbTipoReadequacao AS c ON c.idTipoReadequacao = a.idTipoReadequacao
             LEFT JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON d.idDocumento = a.idDocumento
             LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS e ON e.idArquivo = d.idArquivo WHERE (a.idPronac = :IdPRONAC) AND (a.siEncaminhamento <> 12)
                    """
        )

        return self.sql_connector.session.execute(stmt, {
            'IdPRONAC': IdPRONAC
        }).fetchall()


class AdequacoesPedidoModelObject(QueryBase):
    def __init__(self):
        super(AdequacoesPedidoModelObject, self).__init__()

    def all(self, IdPRONAC):
        stmt = text(
            """
                    SELECT
                a.idReadequacao,
                a.idPronac,
                a.dtSolicitacao,
                CAST(a.dsSolicitacao AS TEXT) AS dsSolicitacao,
                CAST(a.dsJustificativa AS TEXT) AS dsJustificativa,
                a.idSolicitante,
                a.idAvaliador,
                a.dtAvaliador,
                CAST(a.dsAvaliacao AS TEXT) AS dsAvaliacao,
                a.idTipoReadequacao,
                CAST(c.dsReadequacao AS TEXT) AS dsReadequacao,
                a.stAtendimento,
                a.siEncaminhamento,
                CAST(b.dsEncaminhamento AS TEXT) AS dsEncaminhamento,
                a.stEstado,
                e.idArquivo,
                e.nmArquivo
             FROM SAC.dbo.tbReadequacao AS a
             INNER JOIN SAC.dbo.tbTipoEncaminhamento AS b ON a.siEncaminhamento = b.idTipoEncaminhamento INNER JOIN SAC.dbo.tbTipoReadequacao AS c ON c.idTipoReadequacao = a.idTipoReadequacao
             LEFT JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON d.idDocumento = a.idDocumento
             LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS e ON e.idArquivo = d.idArquivo WHERE (a.idPronac = :IdPRONAC) AND (a.siEncaminhamento <> 12)
                    """
        )

        return self.sql_connector.session.execute(stmt, {
            'IdPRONAC': IdPRONAC
        }).fetchall()


class AdequacoesParecerModelObject(QueryBase):
    def __init__(self):
        super(AdequacoesParecerModelObject, self).__init__()

    def all(self, IdPRONAC):
        stmt = text(
            """
                    SELECT
                                    a.idReadequacao,
                                    a.idPronac,
                                    a.dtSolicitacao,
                                    CAST(a.dsSolicitacao AS TEXT) AS dsSolicitacao,
                                    CAST(a.dsJustificativa AS TEXT) AS dsJustificativa,
                                    a.idSolicitante,
                                    a.idAvaliador,
                                    a.dtAvaliador,
                                    CAST(a.dsAvaliacao AS TEXT) AS dsAvaliacao,
                                    a.idTipoReadequacao,
                                    CAST(c.dsReadequacao AS TEXT) AS dsReadequacao,
                                    a.stAtendimento,
                                    a.siEncaminhamento,
                                    CAST(b.dsEncaminhamento AS TEXT) AS dsEncaminhamento,
                                    a.stEstado,
                                    e.idArquivo,
                                    e.nmArquivo
                                 FROM tbReadequacao AS a
                     INNER JOIN SAC.dbo.tbTipoEncaminhamento AS b ON a.siEncaminhamento = b.idTipoEncaminhamento
                     INNER JOIN SAC.dbo.tbTipoReadequacao AS c ON c.idTipoReadequacao = a.idTipoReadequacao
                     LEFT JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON d.idDocumento = a.idDocumento
                     LEFT JOIN BDCORPORATIVO.scCorp.tbArquivo AS e ON e.idArquivo = d.idArquivo WHERE (a.idPronac = :IdPRONAC) AND (a.siEncaminhamento <> 12)
                    """
        )

        return self.sql_connector.session.execute(stmt, {
            'IdPRONAC': IdPRONAC
        }).fetchall()
