from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.handlers.django import django_pbkdf2_sha256
from api.database import execute_query
from api.auth import create_token, verify_token

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.get("/")
def root():
  return {"message": "Tontine API is running"}

@app.get("/members")
def get_members(token: str = Depends(oauth2_scheme)):
  username = verify_token(token)
  members = execute_query("SELECT id, first_name, last_name FROM core_member")
  return {"members": members}

@app.get("/groups/financial")
def get_financial(token: str = Depends(oauth2_scheme)):
  username = verify_token(token)
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
def get_member(member_id: int, token: str = Depends(oauth2_scheme)):
  username = verify_token(token)
  member = execute_query(
    "SELECT id, first_name, last_name FROM core_member WHERE id=%s", 
    (member_id,)
    )
  if member:
    return member[0]
  raise HTTPException(status_code=404, detail="Member not found")

@app.get("/contributions")
def get_contribution(status: str = None, token: str = Depends(oauth2_scheme)):
  username = verify_token(token)
  sql = """
      SELECT co.id, co.status, co.payment_date, cy.start_date, g.name, m.first_name, m.last_name
      FROM core_contribution co
      INNER JOIN core_cycle cy ON cy.id = co.cycle_id
      INNER JOIN core_group g ON g.id = cy.group_id
      INNER JOIN core_member m ON m.id = co.member_id
    """
  if status:
    sql += " WHERE co.status=%s"
    return execute_query(sql, (status,))
  return execute_query(sql)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
  user = execute_query("SELECT id, password FROM auth_user WHERE username=%s", (form_data.username,))
  if user:
    pwd = user[0]["password"]
    if django_pbkdf2_sha256.verify(form_data.password, pwd):
      token = create_token(form_data.username)
      return {"access_token": token, "token_type": "bearer"}
  raise HTTPException(status_code=401, detail="Invalid user or password")
  