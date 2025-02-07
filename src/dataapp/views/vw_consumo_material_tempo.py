from dataapp.config.connections import clickhouse_client

class ConsumoMaterialTempoView:
    def __init__(self):
        self.client = clickhouse_client()

    def criar_view(self):
        query = """
        CREATE VIEW IF NOT EXISTS grupo2.vw_consumo_material_tempo
        (
            `data_movimentacao` Date,
            `quantidade_total_consumida` Float64
        )
        AS
        SELECT
            toDate(FROM_UNIXTIME(JSONExtractInt(data_linha, 'Data Mov.'))) AS data_movimentacao,
            sum(JSONExtractFloat(data_linha, 'Qtde Saida')) AS quantidade_total_consumida
        FROM grupo2.materiais
        WHERE 
            JSONExtractString(data_linha, 'Data Mov.') IS NOT NULL
            AND data_tag = 'consumo_materiais'
        GROUP BY data_movimentacao
        ORDER BY data_movimentacao ASC;
        
        """
        self.client.command(query)
        return "View 'Consumo ao Longo do Tempo' criada com sucesso"

    def consultar_dados(self):
        sql = """
        SELECT
            data_movimentacao AS movement_date,
            quantidade_total_consumida AS total_consumed
        FROM grupo2.vw_consumo_material_tempo
        ORDER BY movement_date ASC
        LIMIT 100;
        """
        return self.client.query(sql).result_rows
