import pandas as pd
import json
import time
from prefect import task

class DataTransformer:
    """
    Classe responsável por transformar um DataFrame em um formato específico.
    """
    def __init__(self, file_name):
        """
        Inicializa a instância do transformador com o nome do arquivo.
        """
        self.file_name = file_name

    def add_data_ingestao(self, df):
        """
        Adiciona a coluna `data_ingestao` ao DataFrame com o timestamp atual.
        """
        df['data_ingestao'] = int(time.time())
        return df

    def add_data_linha(self, df):
        """
        Adiciona a coluna `data_linha`, convertendo cada linha em JSON.
        """
        df['data_linha'] = df.apply(lambda row: json.dumps(row.to_dict()), axis=1)
        return df

    def add_data_tag(self, df):
        """
        Adiciona a coluna `data_tag` com o nome do arquivo.
        """
        df['data_tag'] = self.file_name
        return df

    def transform_data(self, df):
        """
        Aplica as transformações ao DataFrame.
        """
        df = self.add_data_ingestao(df)
        df = self.add_data_linha(df)
        df = self.add_data_tag(df)
        return df[['data_ingestao', 'data_linha', 'data_tag']]

@task(name="Transform Data to JSON")
def transform_data_task(df, file_name):
    transformer = DataTransformer(file_name)
    return transformer.transform_data(df)
