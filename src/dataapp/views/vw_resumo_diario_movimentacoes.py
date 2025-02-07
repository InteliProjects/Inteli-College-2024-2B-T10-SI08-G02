from prefect import task
from dataapp.config.connections import clickhouse_client

class ResumoMovimentacoes:
    def __init__(self):
        self.client = clickhouse_client()

    def criar_view(self):
        query = """
        CREATE OR REPLACE VIEW grupo2.resumo_diario_movimentacoes
        (
            `data_movimentacao` String,
            `cod_estruturado_produto` String,
            `descricao` String,
            `total_saida` Int64,
            `unidade_medida` String
        )
        AS SELECT
            JSONExtractString(data_linha, 'Data Mov.') AS data_movimentacao,
            JSONExtractString(data_linha, 'Cod. Estruturado Produto') AS cod_estruturado_produto,
            JSONExtractString(data_linha, 'Descricao') AS descricao,
            sum(JSONExtractInt(data_linha, 'Qtde Saida')) AS total_saida,
            JSONExtractString(data_linha, 'Unid. Medida') AS unidade_medida
        FROM grupo2.materiais AS m
        GROUP BY
            data_movimentacao,
            cod_estruturado_produto,
            descricao,
            unidade_medida;
        """
        self.client.command(query)
        return "View 'resumo diario de movimentacoes' criada com sucesso"

@task(name="Select All")
def create_view_resumo_diario_movimentacoes():
    resumo = ResumoMovimentacoes()
    return resumo.criar_view()