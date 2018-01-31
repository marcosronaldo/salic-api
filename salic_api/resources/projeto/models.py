import operator

from sqlalchemy import case, func, and_, or_
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql.functions import coalesce

from salic_api.resources.projeto.raw_sql import payments_listing_sql, normalize_sql
from salic_api.resources.query import filter_query, filter_query_like
from ..query import Query
from ..serialization import listify_queryset
from ..shared_models import (
    Projeto, Interessado, Situacao, Enquadramento, PreProjeto,
    Captacao, CertidoesNegativas, Verificacao, PlanoDistribuicao, Produto, Area,
    Segmento, Custos, Mecanismo)
from ...utils import timer

#
# SQL procedures
#
use_sql_procedures = False


def dummy(field, id_projeto, *args):
    return getattr(Custos, field)


ano_projeto = Projeto.AnoProjeto
sequencial = Projeto.Sequencial
id_projeto = Projeto.idProjeto
procs = func.sac.dbo

# Valores da proposta
if use_sql_procedures:
    valor_proposta_base = procs.fnValorDaProposta(id_projeto)
    valor_solicitado = procs.fnValorSolicitado(id_projeto, sequencial)
    valor_aprovado = procs.fnValorAprovado(id_projeto, sequencial)
    valor_aprovado_convenio = procs.fnValorAprovadoConvenio(id_projeto,
                                                            sequencial)
    custo_projeto = procs.fnCustoProjeto(id_projeto, sequencial)
    outras_fontes = procs.fnOutrasFontes(id_projeto)
else:
    valor_proposta_base = dummy('valor_proposta', id_projeto)
    valor_solicitado = dummy('valor_solicitado', id_projeto, sequencial)
    valor_aprovado = dummy('valor_aprovado', id_projeto, sequencial)
    valor_aprovado_convenio = dummy('valor_aprovado_convenio', id_projeto,
                                    sequencial)
    custo_projeto = dummy('custo_projeto', id_projeto, sequencial)
    outras_fontes = dummy('outras_fontes', id_projeto)

# Valores derivados
_mecanismo = Projeto.Mecanismo
_mecanismos_convenio = or_(_mecanismo == '2', _mecanismo == '6')

valor_aprovado = case(
    [(_mecanismos_convenio, valor_aprovado_convenio)],
    else_=valor_aprovado,
)

valor_projeto = case(
    [(_mecanismos_convenio, valor_aprovado_convenio)],
    else_=valor_aprovado + outras_fontes,
)

valor_proposta = coalesce(valor_proposta_base, valor_solicitado)


#
# Query classes
#


class ProjetoQuery(Query):
    #
    # Global info
    #
    query_fields = (
        # Projeto
        Projeto.ProvidenciaTomada.label('providencia'),
        Projeto.NomeProjeto.label('nome'),
        Projeto.PRONAC.label('PRONAC'),
        Projeto.UfProjeto.label('UF'),
        Projeto.DtInicioExecucao.label('data_inicio'),
        Projeto.DtFimExecucao.label('data_termino'),
        Projeto.IdPRONAC,
        Projeto.AnoProjeto.label('ano_projeto'),

        # Pre-projeto
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

        # Interessado
        Interessado.Cidade.label('municipio'),
        Interessado.Nome.label('proponente'),
        Interessado.CgcCpf.label('cgccpf'),

        # Info
        Area.Descricao.label('area'),
        Segmento.Descricao.label('segmento'),
        Situacao.Descricao.label('situacao'),
        Mecanismo.Descricao.label('mecanismo'),

        # Derived info
        Enquadramento.enquadramento,
        valor_solicitado.label('valor_solicitado'),
        outras_fontes.label('outras_fontes'),
        custo_projeto.label('valor_captado'),
        valor_proposta.label('valor_proposta'),
        valor_aprovado.label('valor_aprovado'),
        valor_projeto.label('valor_projeto'),
    )

    #
    # Queries
    #
    def query(self, limit=1, offset=0, PRONAC=None, nome=None, proponente=None,
              cgccpf=None, area=None, segmento=None,
              UF=None, municipio=None, data_inicio=None,
              data_inicio_min=None, data_inicio_max=None,
              data_termino=None, data_termino_min=None,
              data_termino_max=None, year=None, sort_field=None,
              sort_order=None):

        with timer('query projetos_list'):
            # Prepare query
            query = self.raw_query(*self.query_fields)
            query = (
                query
                    .join(PreProjeto)
                    .join(Interessado)
                    .join(Area)
                    .join(Segmento)
                    .join(Situacao)
                    .join(Mecanismo,
                          Mecanismo.Codigo == Projeto.Mecanismo)
                    .outerjoin(Enquadramento,
                               Enquadramento.IdPRONAC == Projeto.IdPRONAC)
            )
            if not use_sql_procedures:
                query = query.join(Custos,
                                   Custos.IdPRONAC == Projeto.IdPRONAC)

            # Filter query by specified fields and dates
            query = filter_query(query, {
                Projeto.PRONAC: PRONAC,
                Area.Codigo: area,
                Segmento.Codigo: segmento,
                Interessado.Uf: UF,
                Interessado.Cidade: municipio,
                Projeto.AnoProjeto: year,
            })
            query = filter_query_like(query, {
                Interessado.Nome: proponente,
                Interessado.CgcCpf: cgccpf,
                Projeto.NomeProjeto: nome,
            })

            # Filter query by dates
            end_of_day = (lambda x: None if x is None else x + '23:59:59')
            query = filter_query(query, {
                Projeto.DtInicioExecucao: data_inicio or data_inicio_min,
                Projeto.DtFimExecucao: data_termino or data_termino_min,
            }, op=operator.ge)

            query = filter_query(query, [
                (Projeto.DtInicioExecucao, end_of_day(data_inicio)),
                (Projeto.DtInicioExecucao, end_of_day(data_inicio_max)),
                (Projeto.DtFimExecucao, end_of_day(data_termino)),
                (Projeto.DtFimExecucao, end_of_day(data_termino_max)),
            ], op=operator.le)

            # Sort result
            sort_field = self.sort_field(sort_field)
            if sort_order == 'desc':
                query = query.order_by(desc(sort_field))
            else:
                query = query.order_by(sort_field)
            return query

    def sort_field(self, sort_field=None):
        sorting_fields = {
            'valor_solicitado': valor_solicitado,
            'PRONAC': Projeto.PRONAC,
            'outras_fontes': outras_fontes,
            'valor_captado': custo_projeto,
            'valor_proposta': valor_proposta,
            'valor_aprovado_case': valor_aprovado,
            'valor_projeto': valor_projeto,
            'ano_projeto': ano_projeto,
            'data_inicio': Projeto.DtInicioExecucao,
            'data_termino': Projeto.DtFimExecucao,
        }
        return sorting_fields[sort_field or 'ano_projeto']

    # FIXME: using SQL procedure SAC.dbo.paDocumentos
    def attached_documents(self, pronac_id):
        if use_sql_procedures:
            query = text('SAC.dbo.paDocumentos :idPronac')
            return self.execute_query(query, {'idPronac': pronac_id}).fetchall()
        else:
            return []

    # FIXME: ???
    def attached_brands(self, idPronac):
        query = text(normalize_sql("""
                SELECT a.idArquivo as id_arquivo
                    FROM BDCORPORATIVO.scCorp.tbArquivoImagem AS ai
                    INNER JOIN BDCORPORATIVO.scCorp.tbArquivo AS a ON ai.idArquivo = a.idArquivo
                    INNER JOIN BDCORPORATIVO.scCorp.tbDocumento AS d ON a.idArquivo = d.idArquivo
                    INNER JOIN BDCORPORATIVO.scCorp.tbDocumentoProjeto AS dp ON dp.idDocumento = d.idDocumento
                    INNER JOIN SAC.dbo.Projetos AS p ON dp.idPronac = p.IdPRONAC WHERE (dp.idTipoDocumento = 1) AND (p.idPronac = :IdPRONAC)
            """))
        return self.execute_query(query, {'IdPRONAC': idPronac}).fetchall()

    def postpone_request(self, idPronac):
        return []
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
        return self.execute_query(query, {'IdPRONAC': idPronac}).fetchall()

    def payments_listing(self, limit=None, offset=None, idPronac=None,
                         cgccpf=None):
        params = {'offset': offset, 'limit': limit}
        if idPronac:
            params['idPronac'] = idPronac
        else:
            params['cgccpf'] = '%{}%'.format(cgccpf)
        query = payments_listing_sql(idPronac, limit is not None)
        return self.execute_query(query, params).fetchall()

    def payments_listing_count(self, idPronac=None, cgccpf=None):
        return []  # FIXME

        if idPronac is not None:
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
                    """)
            params = {'idPronac': idPronac}
            result = self.execute_query(query, params).fetchall()

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
                    """)

            params = {'cgccpf': '%' + cgccpf + '%'}
            result = self.execute_query(query, params).fetchall()

        n_records = listify_queryset(result)
        return n_records[0]['total']

    def taxing_report(self, idPronac):
        return []  # FIXME

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
                """)
        return self.fetch(query, {'IdPRONAC': idPronac})

    def goods_capital_listing(self, idPronac):
        return []  # FIXME
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
        return self.fetch(query, {'IdPRONAC': idPronac})


class CaptacaoQuery(Query):
    def query(self, PRONAC):
        query = self.raw_query(
            Captacao.PRONAC,
            Captacao.CaptacaoReal.label('valor'),
            Captacao.DtRecibo.label('data_recibo'),
            Captacao.CgcCpfMecena.label('cgccpf'),
            Projeto.NomeProjeto.label('nome_projeto'),
            Interessado.Nome.label('nome_doador'),
        )
        query = (
            query
                .join(Projeto, Captacao.PRONAC == Projeto.PRONAC)
                .join(Interessado, Captacao.CgcCpfMecena == Interessado.CgcCpf)
        )
        return filter_query(query, {Captacao.PRONAC: PRONAC})


class AreaQuery(Query):
    def query(self):
        return self.select_as(Area, Descricao='nome', Codigo='codigo')


class SegmentoQuery(Query):
    def query(self):
        return self.select_as(Segmento, Descricao='nome', Codigo='codigo')


class CertidoesNegativasQuery(Query):
    @property
    def descricao(self):
        code = CertidoesNegativas.CodigoCertidao
        return case([
            (code == '49', 'Quitação de Tributos Federais'),
            (code == '51', 'FGTS'),
            (code == '52', 'INSS'),
            (code == '244', 'CADIN'),
        ])

    @property
    def situacao(self):
        return case(
            [(CertidoesNegativas.cdSituacaoCertidao == 0, 'Pendente')],
            else_='Não Pendente'
        )

    def query(self, PRONAC=None, CgcCpf=None):
        query = self.raw_query(
            CertidoesNegativas.DtEmissao.label('data_emissao'),
            CertidoesNegativas.DtValidade.label('data_validade'),
            self.descricao.label('descricao'),
            self.situacao.label('situacao'),
        )
        return filter_query(query, {CertidoesNegativas.PRONAC: PRONAC})


class DivulgacaoQuery(Query):
    # V1 = aliased(Verificacao)
    # V2 = aliased(Verificacao)

    def query(self, IdPRONAC):
        stmt = text(normalize_sql("""
            SELECT v1.Descricao as peca,v2.Descricao as veiculo
                FROM sac.dbo.PlanoDeDivulgacao d
                INNEr JOIN sac.dbo.Projetos p on (d.idProjeto = p.idProjeto)
                INNER JOIN sac.dbo.Verificacao v1 on (d.idPeca = v1.idVerificacao)
                INNER JOIN sac.dbo.Verificacao v2 on (d.idVeiculo = v2.idVerificacao)
                WHERE p.IdPRONAC=:IdPRONAC AND d.stPlanoDivulgacao = 1
            """))
        return self.execute_query(stmt, {'IdPRONAC': IdPRONAC})


class DescolamentoQuery(Query):
    def query(self, IdPRONAC):
        return []  # FIXME

        stmt = text("""
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
            """)
        return self.execute_query(stmt, {'IdPRONAC': IdPRONAC})


class DistribuicaoQuery(Query):
    def query(self, IdPRONAC):
        return (
            self.raw_query(
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
        )


class ReadequacaoQuery(Query):
    def query(self, IdPRONAC):
        return []  # FIXME

        stmt = text("""
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
            """)
        return self.execute_query(stmt, {'IdPRONAC': IdPRONAC}).fetchall()


class AdequacoesPedidoQuery(Query):
    def query(self, IdPRONAC):
        return []  # FIXME

        stmt = text("""
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
            """)
        return self.execute_query(stmt, {'IdPRONAC': IdPRONAC})


class AdequacoesParecerQuery(Query):
    def query(self, IdPRONAC):
        return []  # FIXME

        stmt = text("""
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
        """)
        return self.execute_query(stmt, {'IdPRONAC': IdPRONAC})
