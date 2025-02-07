import pytest
import boto3
import clickhouse_connect
import psycopg2
from unittest.mock import patch, MagicMock, ANY
from dataapp.config.connections import s3_client, clickhouse_client, postgres_connection
from botocore.exceptions import ClientError

# Teste para s3_client
def test_s3_client():
    with patch('boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        
        client = s3_client()
        
        mock_client.assert_called_once_with(
            's3',
            aws_access_key_id=ANY,
            aws_secret_access_key=ANY,
            aws_session_token=ANY,
            region_name=ANY
        )
        assert client == mock_s3

def test_s3_client_error():
    with patch('boto3.client', side_effect=ClientError({'Error': {'Code': '400', 'Message': 'Mocked error'}}, 'operation_name')):
        with pytest.raises(ClientError):
            s3_client()

# Teste para clickhouse_client
def test_clickhouse_client():
    with patch('clickhouse_connect.get_client') as mock_get_client:
        mock_clickhouse = MagicMock()
        mock_get_client.return_value = mock_clickhouse
        
        client = clickhouse_client()
        
        mock_get_client.assert_called_once_with(
            host=ANY,
            port=ANY,
            username=ANY,
            password=ANY,
            database='grupo2',
            connect_timeout=30
        )
        assert client == mock_clickhouse

def test_clickhouse_client_error():
    with patch('clickhouse_connect.get_client', side_effect=clickhouse_connect.driver.exceptions.ClickHouseError):
        with pytest.raises(clickhouse_connect.driver.exceptions.ClickHouseError):
            clickhouse_client()

# Teste para postgres_connection
def test_postgres_connection():
    with patch('psycopg2.connect') as mock_connect:
        mock_postgres = MagicMock()
        mock_connect.return_value = mock_postgres
        
        conn = postgres_connection()
        
        mock_connect.assert_called_once_with(
            dbname=ANY,
            user=ANY,
            password=ANY,
            host=ANY,
            port=ANY
        )
        assert conn == mock_postgres

def test_postgres_connection_error():
    with patch('psycopg2.connect', side_effect=psycopg2.OperationalError):
        with pytest.raises(psycopg2.OperationalError):
            postgres_connection()
