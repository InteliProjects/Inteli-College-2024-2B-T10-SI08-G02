from prefect import task
from dataapp.config.connections import clickhouse_client

class HistoricoQtdeSaidaView:
    def __init__(self):
        self.client = clickhouse_client()

    @task(name="View: Histórico e Quantidade de Saída")
    def create_view(self):
        """
        Cria a view grupo2.vw_historico_qtde_saida no ClickHouse.
        A view retorna a quantidade total de saída agrupada por histórico.
        """
        self.client.command(
            """
            CREATE OR REPLACE VIEW grupo2.vw_historico_qtde_saida (
                `historico` String,
                `quantidade_saida` Float64
            )
            AS 
            SELECT
                JSONExtractString(data_linha, 'Historico') AS historico,
                SUM(JSONExtractFloat(data_linha, 'Qtde Saida')) AS quantidade_saida
            FROM grupo2.materiais
            WHERE JSONExtractString(data_linha, 'Historico') IS NOT NULL
            GROUP BY historico
            ORDER BY quantidade_saida DESC;
            """
        )
        return "View 'vw_historico_qtde_saida' criada com sucesso"