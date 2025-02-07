from flask import Flask, jsonify
from prefect import flow
from dataapp.config.connections import clickhouse_client
from dataapp.etl.etl_bronze.extract import S3DataExtractor
from dataapp.etl.etl_bronze.transform import DataTransformer
from dataapp.etl.etl_bronze.load import ClickhouseLoader
from prefect.cache_policies import NONE
from datetime import datetime
import logging


# Importar as views
from dataapp.views.vw_history_frequency import HistoryFrequencyView
from dataapp.views.vw_resumo_diario_movimentacoes import ResumoMovimentacoes
from dataapp.views.vw_data_mov_qtde_saida import DataMovQtdeSaidaView
from dataapp.views.vw_historico_qtde_saida import HistoricoQtdeSaidaView
from dataapp.views.vw_consumo_material_tempo import ConsumoMaterialTempoView
from dataapp.views.vw_materiais_estoque_zerado import MateriaisEstoqueZeradoView
from dataapp.views.vw_tempo_medio_entrega_por_produto import MediaTempoRequisicao
from dataapp.views.vw_materiais_mais_requisitados import MateriaisMaisRequisitadosView
from dataapp.views.vw_materiais_res75 import MateriaisRES75

# Start API
app = Flask(__name__)

# ETL Pipeline
@flow(name="ETL Pipeline")
def run_etl_pipeline():
    try:
        extractor = S3DataExtractor()
        transformer = DataTransformer(file_name="")
        loader = ClickhouseLoader(database="grupo2", table="materiais")

        for raw_data, file_name in extractor.extract_data_from_s3():
            print(f"Dados extraídos do arquivo {file_name}.parquet com sucesso.")


            transformer.file_name = file_name
            
            transformed_data = transformer.transform_data(raw_data, file_name)
            print("Dados transformados com sucesso.")
            

            loader.create_table()
            loader.load_data_to_clickhouse(transformed_data)
            print(f"Dados do arquivo {file_name}.parquet carregados com sucesso no ClickHouse.")
        
        return {"message": "ETL pipeline executado com sucesso"}
    
    except Exception as e:
        print(f"Erro no pipeline ETL: {e}")
        return {"message": "Erro no pipeline ETL", "error": str(e)}

# API Routes
@app.route('/run-etl', methods=['GET'])
def run_etl():
    result = run_etl_pipeline()
    return jsonify(result)

@app.route('/view_teste', methods= ['POST'])
@flow(name="View Consumo Materiais")
def example_flow_route():
    
    result = create_view_consumo_materiais()
    return jsonify({"message": result})

@app.route('/view-resumo-dia-mov', methods=['POST'])
@flow(name="View Resumo de Movimentações Diárias")
def insert_view_resumo_dia_mov():
    resumo = ResumoMovimentacoes()
    result = resumo.criar_view()
    return jsonify({"message": result})

@app.route('/view-tempo-medio-por-material', methods=['POST'])
@flow(name="View Tempo de Entrega Médio por Produto")
def insert_view_tempo_medio_por_material():
    resumo = MediaTempoRequisicao()
    result = resumo.criar_view()
    return jsonify({"message": result})

@app.route('/view-data-mov-qtde-saida', methods=['POST'])
@flow(name="View Data Movimento e Quantidade de Saída")
def insert_view_data_mov_qtde_saida():
    view = DataMovQtdeSaidaView()
    result = view.create_view()
    return jsonify({"message": result})

@app.route('/view-historico-qtde-saida', methods=['POST'])
@flow(name="View Histórico e Quantidade de Saída")
def insert_view_historico_qtde_saida():
    view = HistoricoQtdeSaidaView()
    result = view.create_view()
    return jsonify({"message": result})

@app.route('/view-materiais-estoque-zerado', methods=['POST'])
@flow(name="View Materiais com Estoque Zerado")
def insert_view_materiais_estoque_zerado():
    view = MateriaisEstoqueZeradoView()
    result = view.create_view()
    return jsonify({"message": result})

@app.route('/view-materiais-mais-requisitados', methods=['POST'])
@flow(name="View Materiais Mais Requisitados")
def criar_view_materiais_mais_requisitados():
    try:
        view = MateriaisMaisRequisitadosView()
        result = view.criar_view()
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/view-consumo-material-tempo', methods=['POST'])
@flow(name="View Consumo Material ao Longo do Tempo")
def criar_view_consumo_material_tempo():
    try:
        view = ConsumoMaterialTempoView()
        result = view.create_view()
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/view-history-frequency', methods=['POST'])
@flow(name="View Frequência Histórico")
def criar_view_history_frequency():
    try:
        view = HistoryFrequencyView()
        result = view.criar_view()
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/view-materiais-res75', methods=['POST'])
@flow(name="View Materiais RES75")
def criar_view_materiais_res75():
    try:
        view = MateriaisRES75()
        result = view.create_view()
        return jsonify({"message": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# consumo materiais 
from flask import request

@app.route('/get-resumo-diario-movimentacoes', methods=['GET']) #INTEGRADO STREAMLIT: OK
def get_view_resumo_diario_movimentacoes():
    try:
        # Obtendo os filtros da query string
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        description = request.args.get('description')
        
        client = clickhouse_client()
        
        sql = """
        SELECT 
            data_movimentacao AS date, 
            descricao AS description, 
            total_saida AS total_output, 
            unidade_medida AS unit 
        FROM grupo2.resumo_diario_movimentacoes
        WHERE 1=1
        """
        
        # Adicionando filtros à consulta SQL
        if start_date and end_date:
            sql += f" AND data_movimentacao BETWEEN '{start_date}' AND '{end_date}'"
        
        if description:
            sql += f" AND descricao LIKE '%{description}%'"
        
        sql += " ORDER BY data_movimentacao DESC LIMIT 10"
        
        rows = client.query(sql).result_rows
        
        data = [
            {
                "date": row[0],
                "description": row[1],
                "total_output": row[2],
                "unit": row[3]
            } for row in rows
        ]
        
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# req_materiais
@app.route('/get-materiais-mais-requisitados', methods=['GET']) 
def get_view_materiais_mais_requisitados():
    try:
        # Obtendo os filtros da query string
        produto = request.args.get('produto')
        min_quantidade = request.args.get('min_quantidade', type=float)
        
        client = clickhouse_client()
        
        sql = """
        SELECT 
            PRODCODESTR AS produto, 
            ITREQMATQTD AS quantidade, 
            ITREQMATUNIDMEDCOD AS unidade_medida 
        FROM grupo2.vw_materiais_mais_requisitados
        WHERE 1=1
        """
        
        # Adicionando filtros à consulta SQL
        if produto:
            sql += f" AND PRODCODESTR LIKE '%{produto}%'"
        
        if min_quantidade is not None:
            sql += f" AND ITREQMATQTD >= {min_quantidade}"
        
        sql += " ORDER BY ITREQMATQTD DESC"
        
        rows = client.query(sql).result_rows
        
        data = [
            {
                "produto": row[0],
                "quantidade": float(row[1]),
                "unidade_medida": row[2]
            } for row in rows
        ]
        
        return jsonify({"data": data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
# consumo materiais 2019 - 2024    
@app.route('/get-consumo-material-tempo', methods=['GET'])
def get_view_consumo_material_tempo():
    try:
        app.logger.info("Iniciando get_view_consumo_material_tempo")
        
        client = clickhouse_client()
        if not client:
            raise Exception("Falha ao inicializar o cliente ClickHouse")
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_consumed = request.args.get('min_consumed', type=float)

        sql = """
        SELECT
            toUnixTimestamp(data_movimentacao) AS movement_date,
            quantidade_total_consumida AS total_consumed
        FROM grupo2.vw_consumo_material_tempo
        WHERE 1=1
        """

        if start_date and end_date:
            sql += f" AND data_movimentacao BETWEEN '{start_date}' AND '{end_date}'"

        if min_consumed is not None:
            sql += f" AND quantidade_total_consumida >= {min_consumed}"

        sql += " ORDER BY data_movimentacao ASC LIMIT 100"

        app.logger.debug(f"SQL query: {sql}")

        rows = client.query(sql).result_rows

        data = [
            {
                "movement_date": datetime.utcfromtimestamp(row[0]).strftime('%Y-%m-%d %H:%M:%S'),
                "total_consumed": row[1]
            }
            for row in rows
        ]

        app.logger.info(f"Dados recuperados com sucesso. Total de registros: {len(data)}")
        return jsonify({"data": data}), 200

    except Exception as e:
        app.logger.error(f"Erro em get_view_consumo_material_tempo: {str(e)}", exc_info=True)
        return jsonify({"error": "Erro interno do servidor. Por favor, tente novamente mais tarde."}), 500

@app.route('/get-data-mov-qtde-saida', methods=['GET']) 
def get_view_data_mov_qtde_saida():
    try:
        client = clickhouse_client()
        
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        min_output = request.args.get('min_output', type=float)

        sql = """
        SELECT
            data_movimento AS movement_date,
            quantidade_saida AS total_output
        FROM grupo2.vw_data_mov_qtde_saida
        WHERE 1=1
        """

        # Adicionando filtros à consulta SQL
        if start_date and end_date:
            sql += f" AND movement_date BETWEEN '{start_date}' AND '{end_date}'"

        if min_output is not None:
            sql += f" AND quantidade_saida >= {min_output}"

        sql += " ORDER BY movement_date ASC LIMIT 100"

        rows = client.query(sql).result_rows

        data = [
            {
                "movement_date": datetime.strptime(str(row[0]), '%Y-%m-%d').strftime('%Y-%m-%d'),
                "total_output": float(row[1])
            }
            for row in rows
        ]

        logging.info(f"Dados a serem retornados: {data}")
        return data

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-historico-qtde-saida', methods=['GET']) #INTEGRADO STREAMLIT: OK
def get_view_historico_qtde_saida():
    try:
        client = clickhouse_client()
        
        # Obtendo os filtros da query string
        historico = request.args.get('historico')
        min_quantidade = request.args.get('min_quantidade', type=float)

        sql = """
        SELECT
            historico,
            quantidade_saida
        FROM grupo2.vw_historico_qtde_saida
        WHERE 1=1
        """

        # Adicionando filtros à consulta SQL
        if historico:
            sql += f" AND historico LIKE '%{historico}%'"

        if min_quantidade is not None:
            sql += f" AND quantidade_saida >= {min_quantidade}"

        sql += " ORDER BY quantidade_saida DESC LIMIT 100"

        rows = client.query(sql).result_rows

        data = [
            {
                "historico": row[0],
                "quantidade_saida": row[1]
            }
            for row in rows
        ]

        return jsonify({"data": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route('/get-frequencia-historico', methods=['GET']) #INTEGRADO STREAMLIT: OK
def get_view_frequencia_historico():
    try:
        client = clickhouse_client()
        
        # Obtendo os filtros da query string
        description = request.args.get('description')
        min_frequency = request.args.get('min_frequency', type=float)

        sql = """
        SELECT
            historico AS description,
            frequencia AS frequency
        FROM grupo2.vw_frequencia_historico
        WHERE 1=1
        """

        # Adicionando filtros à consulta SQL
        if description:
            sql += f" AND historico LIKE '%{description}%'"

        if min_frequency is not None:
            sql += f" AND frequencia >= {min_frequency}"

        sql += " ORDER BY frequencia DESC LIMIT 100"

        rows = client.query(sql).result_rows

        data = [
            {
                "description": row[0],
                "frequency": row[1]
            }
            for row in rows
        ]

        return jsonify({"data": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-materiais-estoque-zerado', methods=['GET']) #INTEGRADO STREAMLIT: OK
def get_view_materiais_estoque_zerado():
    try:
        client = clickhouse_client()
        
        # Obtendo os filtros da query string
        product = request.args.get('product')
        min_days = request.args.get('min_days', type=int)
        max_days = request.args.get('max_days', type=int)

        sql = """
        SELECT
            produto_estruturado AS product,
            dias_estoque_zerado AS days_out_of_stock
        FROM grupo2.vw_materiais_estoque_zerado
        WHERE 1=1
        """

        # Adicionando filtros à consulta SQL
        if product:
            sql += f" AND produto_estruturado LIKE '%{product}%'"

        if min_days is not None:
            sql += f" AND dias_estoque_zerado >= {min_days}"

        if max_days is not None:
            sql += f" AND dias_estoque_zerado <= {max_days}"

        sql += " ORDER BY dias_estoque_zerado DESC LIMIT 100"

        rows = client.query(sql).result_rows

        data = [
            {
                "product": row[0],
                "days_out_of_stock": row[1]
            }
            for row in rows
        ]

        return jsonify({"data": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# tempo medio de entrega
@app.route('/get-media-tempo-requisicao', methods=['GET']) #INTEGRADO STREAMLIT: OK
def get_view_media_tempo_requisicao():
    try:
        client = clickhouse_client()
        
        # Obtendo os filtros da query string
        product_code = request.args.get('codigo_produto')
        min_days = request.args.get('min_days', type=float)
        max_days = request.args.get('max_days', type=float)

        sql = """
        SELECT
            codigo_produto AS product_code,
            media_tempo_dias AS average_days
        FROM grupo2.media_tempo_requisicao
        WHERE 1=1
        """

        # Adicionando filtros à consulta SQL
        if product_code:
            sql += f" AND codigo_produto LIKE '%{product_code}%'"

        if min_days is not None:
            sql += f" AND media_tempo_dias >= {min_days}"

        if max_days is not None:
            sql += f" AND media_tempo_dias <= {max_days}"

        sql += " ORDER BY media_tempo_dias ASC LIMIT 100"

        rows = client.query(sql).result_rows

        data = [
            {
                "product_code": row[0],
                "average_days": row[1]
            }
            for row in rows
        ]

        return jsonify({"data": data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# materiais res75 - pegar todos os dados da view
@app.route('/get-materiais-res75', methods=['GET']) #INTEGRADO STREAMLIT: OK
def get_view_materiais_res75():
    try:
        client = clickhouse_client()
        
        # Obtendo os filtros da query string
        pcan = request.args.get('pcan')
        centro_controle = request.args.get('centro_controle')
        produto = request.args.get('produto')
        codigo_cptm = request.args.get('codigo_cptm')
        codigo_bec = request.args.get('codigo_bec')
        descricao = request.args.get('descricao')
        unid_medida = request.args.get('unid_medida')
        utilizacao = request.args.get('utilizacao')
        status = request.args.get('status')
        especificacao_tecnica = request.args.get('especificacao_tecnica')
        qtde_pcan = request.args.get('qtde_pcan', type=int)
        qtde_pcan_reestruturacao = request.args.get('qtde_pcan_reestruturacao', type=int)
        qtde_estoque = request.args.get('qtde_estoque', type=int)
        dias_estoque_zerado = request.args.get('dias_estoque_zerado', type=int)
        ano_2023 = request.args.get('ano_2023')
        ano_2024 = request.args.get('ano_2024')

        sql = """
        SELECT
            PCAN AS pcan,
            Centro_de_Controle AS centro_controle,
            Produto_Estruturado AS produto,
            Codigo_CPTM AS codigo_cptm,
            Codigo_BEC AS codigo_bec,
            Descricao AS descricao,
            Unid_Medida_Principal AS unid_medida,
            Utilizacao AS utilizacao,
            Status AS status,
            Especificacao_Tecnica AS especificacao_tecnica,
            Qtde_PCAN AS qtde_pcan,
            Qtde_PCAN_Reestruturacao AS qtde_pcan_reestruturacao,
            Qtde_Estoque AS qtde_estoque,
            Dias_Estoque_Zerado AS dias_estoque_zerado,
            Ano_2023 AS ano_2023,
            Ano_2024 AS ano_2024
        FROM grupo2.vw_materiais_res75
        WHERE 1=1
        """

        # Adicionando filtros à consulta SQL
        if pcan:
            sql += f" AND PCAN LIKE '%{pcan}%'"

        if centro_controle:
            sql += f" AND Centro_de_Controle LIKE '%{centro_controle}%'"

        if produto:
            sql += f" AND Produto_Estruturado LIKE '%{produto}%'"

        if codigo_cptm:
            sql += f" AND Codigo_CPTM = {codigo_cptm}"

        if codigo_bec:
            sql += f" AND Codigo_BEC LIKE '%{codigo_bec}%'"

        if descricao:
            sql += f" AND Descricao LIKE '%{descricao}%'"

        if unid_medida:
            sql += f" AND Unid_Medida_Principal LIKE '%{unid_medida}%'"
        
        if utilizacao:
            sql += f" AND Utilizacao LIKE '%{utilizacao}%'"

        if status:
            sql += f" AND Status LIKE '%{status}%'"

        if especificacao_tecnica:
            sql += f" AND Especificacao_Tecnica LIKE '%{especificacao_tecnica}%'"

        if qtde_pcan is not None:
            sql += f" AND Qtde_PCAN = {qtde_pcan}"

        if qtde_pcan_reestruturacao is not None:
            sql += f" AND Qtde_PCAN_Reestruturacao = {qtde_pcan_reestruturacao}"

        if qtde_estoque is not None:
            sql += f" AND Qtde_Estoque = {qtde_estoque}"

        if dias_estoque_zerado is not None:
            sql += f" AND Dias_Estoque_Zerado = {dias_estoque_zerado}"

        if ano_2023:
            sql += f" AND Ano_2023 LIKE '%{ano_2023}%'"

        if ano_2024:
            sql += f" AND Ano_2024 LIKE '%{ano_2024}%'"

        sql += " LIMIT 100"

        rows = client.query(sql).result_rows

        data = [
            {
                "pcan": row[0],
                "centro_controle": row[1],
                "produto": row[2],
                "codigo_cptm": row[3],
                "codigo_bec": row[4],
                "descricao": row[5],
                "unid_medida": row[6],
                "utilizacao": row[7],
                "status": row[8],
                "especificacao_tecnica": row[9],
                "qtde_pcan": row[10],
                "qtde_pcan_reestruturacao": row[11],
                "qtde_estoque": row[12],
                "dias_estoque_zerado": row[13],
                "ano_2023": row[14],
                "ano_2024": row[15]
            }
            for row in rows
        ]

        return jsonify({"data": data}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    
    app.run(debug=True)