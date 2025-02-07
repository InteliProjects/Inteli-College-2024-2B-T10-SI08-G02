import pytest
import pandas as pd
from dataapp.etl.etl_bronze.transform import DataTransformer

@pytest.fixture
def sample_dataframe():
    """Cria um DataFrame de exemplo para os testes."""
    return pd.DataFrame({
        "col1": [1, 2],
        "col2": ["a", "b"]
    })

def test_add_data_ingestao(sample_dataframe):
    transformer = DataTransformer("test_file.csv")
    result = transformer.add_data_ingestao(sample_dataframe.copy())

    assert "data_ingestao" in result.columns
    assert result["data_ingestao"].dtype == "int64"

def test_add_data_linha(sample_dataframe):
    transformer = DataTransformer("test_file.csv")
    result = transformer.add_data_linha(sample_dataframe.copy())

    assert "data_linha" in result.columns
    assert all(result["data_linha"].apply(lambda x: isinstance(x, str)))

def test_add_data_tag(sample_dataframe):
    transformer = DataTransformer("test_file.csv")
    result = transformer.add_data_tag(sample_dataframe.copy())

    assert "data_tag" in result.columns
    assert all(result["data_tag"] == "test_file.csv")

def test_transform_data(sample_dataframe):
    transformer = DataTransformer("test_file.csv")
    result = transformer.transform_data(sample_dataframe.copy())

    # Verifica colunas e integridade
    assert list(result.columns) == ["data_ingestao", "data_linha", "data_tag"]
    assert result["data_tag"].iloc[0] == "test_file.csv"
    assert result["data_linha"].apply(lambda x: isinstance(x, str)).all()

