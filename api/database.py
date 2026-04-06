import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def get_connection():
  url = urlparse(os.getenv("DATABASE_URL"))
  conn = psycopg2.connect(
    dbname=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
  )
  return conn

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