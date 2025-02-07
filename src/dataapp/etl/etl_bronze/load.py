import os
from dotenv import load_dotenv
from dataapp.config.connections import clickhouse_client
from prefect import task

load_dotenv()

class ClickhouseLoader:
    """
    Classe responsável por carregar dados em uma tabela ClickHouse.
    """
    def __init__(self, database, table):
        """
        Inicializa o cliente ClickHouse e define o banco de dados e tabela.
        """
        self.client = clickhouse_client()
        self.database = database
        self.table = table

    def create_table(self):
        """
        Cria a tabela no ClickHouse se ela ainda não existir.
        """
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self.database}.{self.table} (
            data_ingestao UInt32,
            data_linha String,
            data_tag String
        ) ENGINE = MergeTree()
        ORDER BY data_ingestao;
        """
        try:
            self.client.command(create_table_query)
            print(f"Tabela {self.database}.{self.table} criada ou já existente.")
        except Exception as e:
            raise RuntimeError(f"Erro ao criar a tabela {self.database}.{self.table}: {e}")

    def insert_data(self, df):
        """
        Insere dados de um DataFrame na tabela ClickHouse.
        """
        data_tuples = [tuple(row) for row in df.itertuples(index=False, name=None)]
        try:
            self.client.insert(
                f"{self.database}.{self.table}",
                data_tuples,
                column_names=df.columns.tolist()
            )
            print("Dados carregados com sucesso no ClickHouse.")
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar dados no ClickHouse: {e}")

@task(name="Load Data to Clickhouse")
def load_data_to_clickhouse_task(df):
    loader = ClickhouseLoader(database="grupo2", table="materiais")
    loader.create_table()
    loader.insert_data(df)
