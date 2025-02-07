import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from dataapp.etl.etl_bronze.load import ClickhouseLoader

@pytest.fixture
def sample_dataframe():
    """Cria um DataFrame de exemplo para os testes."""
    return pd.DataFrame({
        "data_ingestao": [1690000000, 1690000001],
        "data_linha": ['{"col1": 1, "col2": "a"}', '{"col1": 2, "col2": "b"}'],
        "data_tag": ["test_file.csv", "test_file.csv"]
    })

@patch("dataapp.etl.etl_bronze.load.clickhouse_client")
def test_create_table(mock_clickhouse_client):
    # Arrange
    mock_client = MagicMock()
    mock_clickhouse_client.return_value = mock_client
    loader = ClickhouseLoader(database="test_db", table="test_table")

    # Act
    loader.create_table()

    # Assert
    mock_client.command.assert_called_once_with(
        """
        CREATE TABLE IF NOT EXISTS test_db.test_table (
            data_ingestao UInt32,
            data_linha String,
            data_tag String
        ) ENGINE = MergeTree()
        ORDER BY data_ingestao;
        """
    )

@patch("dataapp.etl.etl_bronze.load.clickhouse_client")
def test_insert_data(mock_clickhouse_client, sample_dataframe):
    # Arrange
    mock_client = MagicMock()
    mock_clickhouse_client.return_value = mock_client
    loader = ClickhouseLoader(database="test_db", table="test_table")
    df = sample_dataframe

    # Act
    loader.insert_data(df)

    # Assert
    mock_client.insert.assert_called_once_with(
        "test_db.test_table",
        [
            (1690000000, '{"col1": 1, "col2": "a"}', "test_file.csv"),
            (1690000001, '{"col1": 2, "col2": "b"}', "test_file.csv"),
        ],
        column_names=["data_ingestao", "data_linha", "data_tag"]
    )
