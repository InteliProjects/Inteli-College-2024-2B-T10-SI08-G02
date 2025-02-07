from prefect import task
from dataapp.config.connections import clickhouse_client

class MateriaisRES75:
    def __init__(self):
        self.client = clickhouse_client()

    @task(name="View: Materiais RES75")
    def create_view(self):
        """
        Cria a view grupo2.vw_materiais_res75 no ClickHouse.
        A view retorna a quantidade total de saída agrupada por data de movimento.
        """
        self.client.command(
            """
            CREATE OR REPLACE VIEW grupo2.vw_materiais_res75
            (

                `PCAN` String,

                `Centro_de_Controle` String,

                `Produto_Estruturado` String,

                `Codigo_CPTM` Int64,

                `Codigo_BEC` String,

                `Descricao` String,

                `Unid_Medida_Principal` String,

                `Utilizacao` String,

                `Status` String,

                `Especificacao_Tecnica` String,

                `Qtde_PCAN` Int64,

                `Qtde_PCAN_Reestruturacao` Int64,

                `Qtde_Estoque` Int64,

                `Dias_Estoque_Zerado` Int64,

                `Ano_2023` String,

                `Ano_2024` String
            )
            AS SELECT
                JSONExtractString(data_linha,
            'PCAN') AS PCAN,

                JSONExtractString(data_linha,
            'Centro de Controle') AS Centro_de_Controle,

                JSONExtractString(data_linha,
            'Produto Estruturado') AS Produto_Estruturado,

                JSONExtractInt(data_linha,
            'Código CPTM') AS Codigo_CPTM,

                JSONExtractString(data_linha,
            'Código BEC') AS Codigo_BEC,

                JSONExtractString(data_linha,
            'Descrição') AS Descricao,

                JSONExtractString(data_linha,
            'Unid. Medida Principal') AS Unid_Medida_Principal,

                JSONExtractString(data_linha,
            'Utilização') AS Utilizacao,

                JSONExtractString(data_linha,
            'Status') AS Status,

                JSONExtractString(data_linha,
            'Especificação Técnica') AS Especificacao_Tecnica,

                JSONExtractInt(data_linha,
            'Qtde PCAN') AS Qtde_PCAN,

                JSONExtractInt(data_linha,
            'Qtde PCAN Reestruturação') AS Qtde_PCAN_Reestruturacao,

                JSONExtractInt(data_linha,
            'Qtde Estoque') AS Qtde_Estoque,

                JSONExtractInt(data_linha,
            'Dias Estoque Zerado') AS Dias_Estoque_Zerado,

                JSONExtractString(data_linha,
            '2023') AS Ano_2023,

                JSONExtractString(data_linha,
            '2024') AS Ano_2024
            FROM grupo2.materiais
            WHERE data_tag = 'Materiais_RES75';
            """
        )

        return "View 'vw_materiais_res75' criada com sucesso"