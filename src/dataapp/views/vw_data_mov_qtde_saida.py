from prefect import task
from dataapp.config.connections import clickhouse_client

class DataMovQtdeSaidaView:
    def __init__(self):
        self.client = clickhouse_client()

    @task(name="View: Data Movimento e Quantidade de Saída")
    def create_view(self):
        """
        Cria a view grupo2.vw_data_mov_qtde_saida no ClickHouse.
        A view retorna a quantidade total de saída agrupada por data de movimento.
        """
        self.client.command(
            """
            CREATE VIEW IF NOT EXISTS grupo2.vw_data_mov_qtde_saida
            (
                `data_movimento` Date,
                `quantidade_saida` Float64
            )
            AS
            SELECT
                toDate(FROM_UNIXTIME(JSONExtractInt(data_linha, 'Data Mov.'))) AS data_movimento,
                sum(JSONExtractFloat(data_linha, 'Qtde Saida')) AS quantidade_saida
            FROM grupo2.materiais
            WHERE 
                JSONExtractString(data_linha, 'Data Mov.') IS NOT NULL
            GROUP BY data_movimento
            ORDER BY data_movimento ASC;
            """
        )
        return "View 'vw_data_mov_qtde_saida' criada com sucesso"