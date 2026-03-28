import psycopg2

def get_connection():
  return psycopg2.connect(
    dbname='tontine_db',
    user='postgres',
    password='1234',
    host='localhost',
    port='5432'
  )

def execute_query(sql):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute(sql)
  rows = cursor.fetchall()
  columns = [col.name for col in cursor.description]
  results = [dict(zip(columns, row)) for row in rows]
  cursor.close()
  conn.close()
  return results