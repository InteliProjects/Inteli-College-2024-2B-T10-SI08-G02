
# Teste de Criação de View no ClickHouse

Este projeto é responsável por testar a criação de uma View no banco de dados **ClickHouse**. A View `vw_history_frequency` utiliza dados de uma tabela para calcular a frequência de itens com base em condições específicas.

## Como Executar os Testes

Para executar o teste relacionado à criação da View, utilize o comando:

```bash
pytest src/tests/test_create_view_history_frequency.py
```

Este comando irá rodar o teste referente à criação da View `vw_history_frequency`, verificando se a SQL gerada corresponde à esperada.