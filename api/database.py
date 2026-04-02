import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
  return psycopg2.connect(
    dbname='tontine_db',
    user='postgres',
    password=os.getenv("DB_PASSWORD"),
    host='localhost',
    port='5432'
  )

def execute_query(sql, params=None):
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute(sql, params)
  rows = cursor.fetchall()
  columns = [col.name for col in cursor.description]
  results = [dict(zip(columns, row)) for row in rows]
  cursor.close()
  conn.close()
  return results