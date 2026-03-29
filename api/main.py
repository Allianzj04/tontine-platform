from fastapi import FastAPI, HTTPException
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

@app.get("/members/{member_id}")
def get_member(member_id: int):
  member = execute_query(
    "SELECT id, first_name, last_name FROM core_member WHERE id=%s", 
    (member_id,)
    )
  if member:
    return member[0]
  raise HTTPException(status_code=404, detail="Member not found")
