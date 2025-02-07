
# Documentação de Testes com Pytest

Esta documentação é referente aos testes apresentados na pasta 'teste' que, por sua vez, testam os métodos dos arquivos:

- test_api_routes.py
- src/tests/test_api.py
- src/tests/test_app.py
- src/tests/test_connections.py
- src/tests/test_etl_bronze.py
- src/tests/test_etl_prata.py
- src/tests/test_extract.py
- src/tests/test_history_frequency_view.py
- src/tests/test_load.py
- src/tests/test_transform.py
- src/tests/test_vw_analise_local_armazenamento.py
- src/tests/test_vw_materiais_mais_requisitados.py
- test_vw_res_dia_mov.py
- test_vw_tempo_medio_entrega_produto.py


> É importante ressaltar que todos os testes acima foram realizados e que o arquivo que mostra a atual cobertura dos testes pode ser acessado [aqui]().

## 👨🏽‍💻 Como executar os testes?

Para iniciar o processo, você precisa estar dentro deste repositório. O primeiro passo é entrar na pasta *'src'*, onde estão as funções que desejamos testar e o arquivo de teste em si.


```
cd .\src\
```

Para realizar o passo a seguir é necessário ter o poetry instalado, caso não tenha, instale-o primeiro e depois retome o tutorial. Agora, ative a máquina virtual do *poetry* utilizando o comando abaixo:

````
poetry shell
````

Caso você não tenha instalado as bibliotecas necessária para realizar os testes e saber suas respectivas coberturas (que são *pytest* e *pytest-cov*), rode o seguinte comando:


````
poetry add pytest pytest-cov pytest-mock --group dev
````

Com as dependências já instaladas, agora inicie o teste ao rodar o seguinte comando:

````
poetry run pytest --verbose
````

Opa, agora os testes já começaram a rodar! Caso você tabém deseje saber a cobertura dos testes e gerar um relatório disso, rode o seguinte comando:

````
pytest --cov=(caminho do arquivo a ser testado) tests/(nome do arquivo de teste a ser executado) --cov-report=html
````
> ⚠️ Não se esqueça de alterar os caminhos no comando acima de acordo com os arquivos que você deseja testar.

Com isso, será gerada uma pasta chamada 'html-cov' na pasta 'src'. Nela, você encontrará um arquivo 'index.html', ao acessá-lo através de seu navegador, você terá acesso a um relatório sobre a cobertura dos testes que você realizou.


## 🛠️ Exemplo prático de teste 

Aqui será realizado um exeplo prático de teste do arquivo "vw_resumo_diario_movimentacoes.py". Este pacote cria uma visualização no data warehouse, através de uma querie SQL do tipo CREATE VIEW. O objetivo desta visualização é entender o total de saida diário de cada item do estoque.

### Preparação do ambiente

Para executar os testes, é necessário realizar o seguinte no terminal:

````python
# Inicializar o ambiente virtual
>> poetry shell

# Instalar as dependências
>> poetry add pytest prefect clickhouse_connect

# Executar testes
>> pytest
````
### Estrutura dos testes

Os testes foram criados a partir da estrutura de Testes Unitários AAA (Arrange, Act, Assert). Eles foram divididos em duas frentes: teste de um cenário positivo, teste de um cenário negativo. A seguir, está a estrutura dos testes:

````python
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
````
O cenário positivo contempla uma situação na qual a visualização ainda não existe no datawarehouse. Nesse sentido, essa visualização pode ser criada com sucesso, gerando um status "OK 200".

Enquanto isso, o teste negativo se refere a um cenário em que a visualização já foi criada, o que resulta em um status "ERRO 500".

Após executar os comandos ``pytest`` - como exemplificado anteriormente - no terminal, deve-se visualizar o seguinte output:

<div align="center">
Imagem 01 - Output Pytest
<img src="https://res.cloudinary.com/dajxsyf98/image/upload/v1733151550/Captura_de_tela_2024-12-02_115844_bhrqxa.png" ref="output_pytest">
Fonte: Autoria própria.
</div>

Após realizar estas etapas, o teste estará concluído.