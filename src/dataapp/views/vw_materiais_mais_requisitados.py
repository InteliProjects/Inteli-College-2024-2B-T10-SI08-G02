from prefect import task
from dataapp.config.connections import clickhouse_client

class MateriaisMaisRequisitadosView:
    def __init__(self):
        self.client = clickhouse_client()

    def criar_view(self):
        query = """
        -- grupo2.vw_materiais_mais_requisitados
        CREATE VIEW IF NOT EXISTS grupo2.vw_materiais_mais_requisitados
        (
            `PRODCODESTR` String,
            `ITREQMATQTD` Float64,
            `ITREQMATUNIDMEDCOD` String
        )
        AS
        SELECT
            JSONExtractString(data_linha, 'PRODCODESTR') AS PRODCODESTR,
            SUM(JSONExtractFloat(data_linha, 'ITREQMATQTD')) AS ITREQMATQTD,
            JSONExtractString(data_linha, 'ITREQMATUNIDMEDCOD') AS ITREQMATUNIDMEDCOD
        FROM grupo2.materiais
        WHERE JSONExtractString(data_linha, 'PRODCODESTR') IS NOT NULL
        GROUP BY
            PRODCODESTR,
            ITREQMATUNIDMEDCOD
        ORDER BY
            ITREQMATQTD DESC
        LIMIT 15;
        """
        self.client.command(query)
        return "View 'Materiais Mais Requisitados' criada com sucesso"
