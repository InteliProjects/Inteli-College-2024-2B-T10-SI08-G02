import sys
import os

# Adiciona o diretório `src` ao sys.path para permitir a importação de módulos do projeto
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src"))
sys.path.insert(0, src_path)

# Importa os módulos necessários para conexão e execução de comandos no ClickHouse
try:
    from dataapp.config.connections import clickhouse_client  # Cliente para conexão com o ClickHouse
except ModuleNotFoundError as e:
    # Caso o módulo não seja encontrado, exibe uma mensagem de erro
    print(f"Erro ao importar o módulo: {e}")

from prefect import task  # Biblioteca Prefect para definir tarefas

# Define a tarefa de criação da View com Prefect
@task(name="Criar View: Histórico de Frequência")
def create_view_history_frequency():
    """
    Cria uma View no banco de dados ClickHouse.

    A View utiliza dados de uma tabela para calcular a frequência de itens com base em condições específicas,
    como status ativo. A criação inclui agrupamento e ordenação para retornar os itens mais frequentes.

    Returns:
        str: Mensagem indicando o status da operação.
    """
    try:
        # Inicializa o cliente ClickHouse para comunicação com o banco
        client = clickhouse_client()

        # Executa o comando SQL para criar a View no ClickHouse
        client.command(
            """
            CREATE VIEW grupo2.vw_history_frequency
            (
                `item` String,          -- Nome do item, extraído como string do JSON
                `frequency` Int64       -- Contagem da frequência de ocorrência do item
            )
            AS SELECT
                JSONExtractString(data_linha, 'Item') AS item,  -- Extrai o campo 'Item' do JSON
                count(*) AS frequency                         -- Calcula a contagem total de ocorrências
            FROM grupo2.materiais
            WHERE JSONExtractString(data_linha, 'Status') = 'active'  -- Filtra registros com status 'active'
            GROUP BY item                                     -- Agrupa os resultados pelo campo 'item'
            ORDER BY frequency DESC                          -- Ordena os resultados pela frequência em ordem decrescente
            LIMIT 20;                                         -- Limita os resultados a 20 registros
            """
        )
        return "View criada com sucesso."
    except Exception as e:
        # Em caso de erro, exibe a mensagem correspondente
        print(f"Erro ao criar a View: {e}")
        return "Falha ao criar a View."

if __name__ == "__main__":
    try:
        # Executa a criação da View e exibe o resultado
        result = create_view_history_frequency()
        print(result)
    except Exception as e:
        # Captura qualquer erro durante a execução principal
        print(f"Erro na execução principal: {e}")
