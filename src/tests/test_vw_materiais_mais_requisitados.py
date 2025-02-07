import pytest
from unittest.mock import Mock, patch
from dataapp.views.vw_materiais_mais_requisitados import MateriaisMaisRequisitadosView

@pytest.fixture
def mock_clickhouse_client():
    with patch('dataapp.views.vw_materiais_mais_requisitados.clickhouse_client') as mock_client:
        yield mock_client

def test_criar_view_materiais_mais_requisitados(mock_clickhouse_client):
    # Arrange
    mock_client = Mock()
    mock_clickhouse_client.return_value = mock_client
    view = MateriaisMaisRequisitadosView()

    # Act
    result = view.criar_view()

    # Assert
    assert result == "View 'Materiais Mais Requisitados' criada com sucesso"
    mock_client.command.assert_called_once()
    
    # Verificar se a query SQL está correta
    sql_query = mock_client.command.call_args[0][0]
    assert "CREATE VIEW IF NOT EXISTS grupo2.vw_materiais_mais_requisitados" in sql_query
    assert "SELECT" in sql_query
    assert "FROM grupo2.materiais" in sql_query
    assert "GROUP BY" in sql_query
    assert "ORDER BY" in sql_query
    assert "LIMIT 15" in sql_query
