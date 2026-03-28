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
  cursor.close()
  conn.close()
  return {"members": members}

@app.get("/groups/financial")
def get_financial():
  conn = get_connection()
  cursor = conn.cursor()
  cursor.execute("""
SELECT
  g.name,
  SUM(g.amount) AS amount_expected,
  SUM(CASE WHEN co.status = 'paid' THEN g.amount ELSE 0 END) AS amount_paid
FROM core_group g
INNER JOIN core_cycle cy ON cy.group_id = g.id
INNER JOIN core_contribution co ON co.cycle_id = cy.id
GROUP BY g.name;
""")
  rows = cursor.fetchall()
  columns = [col.name for col in cursor.description]
  financial_by_group = [dict(zip(columns, row)) for row in rows]
  cursor.close()
  conn.close()
  return {"financial": financial_by_group}
