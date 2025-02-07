import os
import pandas as pd
from io import BytesIO
from dotenv import load_dotenv
from dataapp.config.connections import s3_client
from prefect import task

load_dotenv()

class S3DataExtractor:
    def __init__(self, bucket_name=None):
        """
        Inicializa a instância do extrator com o cliente S3 e o nome do bucket.
        """
        self.s3 = s3_client()
        # self.bucket_name = os.getenv('S3_BUCKET_NAME')
        self.bucket_name = "gptm-two"
        
        if not self.bucket_name:
            raise ValueError("O nome do bucket deve ser fornecido ou definido na variável de ambiente S3_BUCKET_NAME.")

    def list_parquet_files(self):
        """
        Lista os arquivos `.parquet` no bucket S3.
        Retorna uma lista de chaves (caminhos) para os arquivos `.parquet`.
        """
        folder_prefix = "new_materiais/"

        objects = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=folder_prefix)
        return [
            obj['Key']
            for obj in objects.get('Contents', [])
            if obj['Key'].endswith('.parquet')
        ]

    def load_parquet_file(self, key):
        """
        Carrega um arquivo `.parquet` do bucket S3.
        Retorna o DataFrame pandas e o nome base do arquivo (sem extensão).
        """
        try:
            file_obj = self.s3.get_object(Bucket=self.bucket_name, Key=key)
            file_name = key.split('/')[-1].replace('.parquet', '')
            parquet_data = pd.read_parquet(BytesIO(file_obj['Body'].read()), engine='pyarrow')

            return parquet_data, file_name
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar o arquivo {key}: {e}")

    def extract_data_from_s3(self):
        """
        Gera os DataFrames e nomes dos arquivos para cada arquivo `.parquet` no bucket.
        """
        parquet_files = self.list_parquet_files()
        for key in parquet_files:
            try:
                yield self.load_parquet_file(key)
            except RuntimeError as e:
                print(e)

@task(name="Extract Data From S3 Bucket")
def extract_data_from_s3_task():
    extractor = S3DataExtractor()
    for parquet_data, file_name in extractor.extract_data_from_s3():
        yield parquet_data, file_name