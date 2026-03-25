import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine.settings')
django.setup()

import psycopg2, pandas as pd

conn = psycopg2.connect(
  dbname='tontine_db',
  user='postgres',
  password='1234',
  host='localhost',
  port='5432'
)

cursor = conn.cursor()
cursor.execute("SELECT id, status, payment_date FROM core_contribution")
rows = cursor.fetchall()
# print(rows)
# print(cursor.description)

columns = [col.name for col in cursor.description]
df = pd.DataFrame(rows, columns=columns)
# df.to_csv("fff.csv", index=False)

cursor.close()
conn.close()

