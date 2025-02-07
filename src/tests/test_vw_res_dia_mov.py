import pytest
from unittest.mock import Mock
from prefect.testing.utilities import prefect_test_harness
from clickhouse_connect.driver.exceptions import DatabaseError

from dataapp.config.connections import clickhouse_client
from dataapp.views.vw_resumo_diario_movimentacoes import ResumoMovimentacoes, create_view_resumo_diario_movimentacoes

@pytest.fixture
def mock_clickhouse_client():
    return Mock()

# Cenário de teste positivo
def test_create_view_resumo_diario_movimentacoes_success(mocker, mock_clickhouse_client):
    mocker.patch('dataapp.views.vw_resumo_diario_movimentacoes.clickhouse_client', return_value=mock_clickhouse_client)

    with prefect_test_harness():
        result = create_view_resumo_diario_movimentacoes.fn()
    
    assert result == "View 'resumo diario de movimentacoes' criada com sucesso"
    mock_clickhouse_client.command.assert_called_once()

# Cenário de teste negativo
def test_create_view_resumo_diario_movimentacoes_already_exists(mocker, mock_clickhouse_client):
    mocker.patch('dataapp.views.vw_resumo_diario_movimentacoes.clickhouse_client', return_value=mock_clickhouse_client)
    mock_clickhouse_client.command.side_effect = DatabaseError("Table grupo2.resumo_diario_movimentacoes already exists")
    
    with prefect_test_harness():
        with pytest.raises(DatabaseError) as excinfo:
            create_view_resumo_diario_movimentacoes.fn()
    
    assert "Table grupo2.resumo_diario_movimentacoes already exists" in str(excinfo.value)