from fastapi import FastAPI
from api.database import get_connection

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Tontine API is running"}

@app.get("/members")
def get_members():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("SELECT id, first_name, last_name FROM core_member")
  rows = cursor.fetchall()
  columns = [col.name for col in cursor.description]
  members = [dict(zip(columns, row)) for row in rows]
  return {"members": members}

