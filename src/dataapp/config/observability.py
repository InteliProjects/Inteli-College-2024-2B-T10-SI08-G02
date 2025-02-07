# # Registro de métricas de execução no PostgreSQL
from config.connections import postgres_connection

def log_table(start_time, end_time):
     conn = postgres_connection()
     cursor = conn.cursor()

     # Criando a tabela se ela não existir
     cursor.execute('''
         CREATE TABLE IF NOT EXISTS public.observability_g2 (
             id SERIAL PRIMARY KEY,
             start_time TIMESTAMP,
             end_time TIMESTAMP,
             duration INTERVAL,
         );
     ''')

     duration = end_time - start_time

     cursor.execute('''
     INSERT INTO modulo8si.observability_g2 (start_time, end_time, duration)
         VALUES (%s, %s, %s);
     ''', (start_time, end_time, duration))

     conn.commit()
     cursor.close()
     conn.close()

#import sqs from connections

#gravar na fila o seguinte padrão:

#{

#}