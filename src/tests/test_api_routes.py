import pytest
from flask import json
from dataapp.api import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_run_etl(client):
    response = client.get('/run-etl')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "message" in data

def test_get_resumo_diario_movimentacoes(client):
    response = client.get('/get-resumo-diario-movimentacoes?start_date=2024-01-01&end_date=2024-12-31&description=Test')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data

def test_get_materiais_mais_requisitados(client):
    response = client.get('/get-materiais-mais-requisitados?produto=Test&min_quantidade=10')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data

def test_get_consumo_material_tempo(client):
    response = client.get('/get-consumo-material-tempo?start_date=2024-01-01&end_date=2024-12-31&min_consumed=5')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data

def test_get_data_mov_qtde_saida(client):
    response = client.get('/get-data-mov-qtde-saida?start_date=2024-01-01&end_date=2024-12-31&min_output=5')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data

def test_get_historico_qtde_saida(client):
    response = client.get('/get-historico-qtde-saida?historico=Test&min_quantidade=5')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data

def test_get_frequencia_historico(client):
    response = client.get('/get-frequencia-historico?description=Test&min_frequency=5')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "data" in data
