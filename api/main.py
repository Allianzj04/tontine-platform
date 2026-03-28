from fastapi import FastAPI
from api.database import execute_query

app = FastAPI()

@app.get("/")
def root():
  return {"message": "Tontine API is running"}

@app.get("/members")
def get_members():
  members = execute_query("SELECT id, first_name, last_name FROM core_member")
  return {"members": members}

@app.get("/groups/financial")
def get_financial():
  financial_by_group = execute_query("""
SELECT
  g.name,
  SUM(g.amount) AS amount_expected,
  SUM(CASE WHEN co.status = 'paid' THEN g.amount ELSE 0 END) AS amount_paid
FROM core_group g
INNER JOIN core_cycle cy ON cy.group_id = g.id
INNER JOIN core_contribution co ON co.cycle_id = cy.id
GROUP BY g.name;
""")
  return {"financial": financial_by_group}
