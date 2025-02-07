from prefect import task
from dataapp.config.connections import clickhouse_client

class MateriaisEstoqueZeradoView:
    def __init__(self):
        self.client = clickhouse_client()

    @task(name="Materiais com Estoque Zerado")
    def create_view(self):
        """
        Cria a view grupo2.vw_materiais_estoque_zerado no ClickHouse.
        A view retorna os materiais com estoque zerado e seus respectivos dias.
        """
        self.client.command(
            """
            CREATE OR REPLACE VIEW grupo2.vw_materiais_estoque_zerado AS
            SELECT
                JSONExtractString(data_linha, 'Produto Estruturado') AS produto_estruturado,
                JSONExtractUInt(data_linha, 'Dias Estoque Zerado') AS dias_estoque_zerado
            FROM grupo2.materiais
            WHERE JSONExtractUInt(data_linha, 'Dias Estoque Zerado') IS NOT NULL
              AND JSONExtractUInt(data_linha, 'Dias Estoque Zerado') < 720
            ORDER BY dias_estoque_zerado DESC;
            """
        )
        return "View 'Materiais com Estoque Zerado' criada com sucesso"