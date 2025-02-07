from prefect import task
from dataapp.config.connections import clickhouse_client

class HistoryFrequencyView:
    def __init__(self):
        self.client = clickhouse_client()

    @task(name='Histórico de Frequência')
    def criar_view(self):
        query = """
        CREATE VIEW IF NOT EXISTS grupo2.vw_frequencia_historico
        (
            `historico` String,
            `frequencia` UInt64
        )
        AS SELECT
            JSONExtractString(data_linha, 'Historico') AS historico,
            COUNT(*) AS frequencia
        FROM grupo2.materiais
        GROUP BY historico
        ORDER BY frequencia DESC
        """
        self.client.command(query)
        return "View 'Histórico de Frequência' criada com sucesso"

    def consultar_dados(self):
        sql = """
        SELECT 
            historico AS description,
            frequencia AS frequency
        FROM grupo2.vw_frequencia_historico
        ORDER BY frequency DESC
        """
        return self.client.command(sql)