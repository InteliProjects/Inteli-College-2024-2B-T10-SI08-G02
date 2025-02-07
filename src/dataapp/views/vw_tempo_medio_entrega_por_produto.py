from prefect import task
from dataapp.config.connections import clickhouse_client

class MediaTempoRequisicao:
    def __init__(self):
        self.client = clickhouse_client()

    def criar_view(self):
        query = """
        CREATE OR REPLACE VIEW grupo2.media_tempo_requisicao
        (
            `codigo_produto` String,
            `media_tempo_dias` Float64
        )
        AS SELECT
            JSONExtractString(data_linha, 'PRODCODESTR') AS codigo_produto,
            avg(abs(dateDiff('day',
                toDateTime(JSONExtractInt(data_linha, 'REQMATDATA')),
                toDateTime(JSONExtractInt(data_linha, 'REQMATDATAENTREGA'))
            ))) AS media_tempo_dias
        FROM grupo2.materiais
        GROUP BY
            codigo_produto;
        """
        self.client.command(query)
        return "View 'media_tempo_requisicao' criada com sucesso"

@task(name="Create Media Tempo View")
def create_media_tempo_view():
    media_tempo = MediaTempoRequisicao()
    return media_tempo.criar_view()
