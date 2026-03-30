import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine.settings')
django.setup()

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_members():
  response_login = client.post("/login", data={"username": "dshea", "password": "password123"})
  token = response_login.json()["access_token"]
  response_get = client.get("/members", headers={"Authorization": "Bearer " + token})

  assert response_login.status_code == 200
  assert response_get.status_code == 200 
  assert "members" in response_get.json()

def test_login_invalid_credentials():
  response_login = client.post("/login", data={"username": "dshea", "password": "aaa"})
  
  assert response_login.status_code == 401

def test_get_member_not_found():
  response_login = client.post("/login", data={"username": "dshea", "password": "password123"})
  token = response_login.json()["access_token"]
  response_get = client.get("/member/9999", headers={"Authorization": "Bearer " + token})

  assert response_login.status_code == 200
  assert response_get.status_code == 404