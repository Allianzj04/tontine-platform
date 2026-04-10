# Tontine Platform

A web platform for managing tontines — a traditional savings system widely used in Burundi and across sub-Saharan Africa.

A tontine is a savings association where members contribute the same amount of money each cycle, and the full sum is given to the member whose turn it is. This project was built because tontines in Burundi are still managed manually — pen and paper. This platform solves a real local problem while covering a modern backend stack: Django, FastAPI, Pandas, and PostgreSQL.

---

## Live Demo

| Service | URL |
|---|---|
| Django Web App | https://tontine-platform.onrender.com |
| FastAPI REST API | https://tontine-api-l3bz.onrender.com/docs |

---

## Tech Stack

| Layer | Technology |
|---|---|
| Web Backend | Django 5 |
| REST API | FastAPI |
| Data & Analytics | Pandas, NumPy |
| Database | PostgreSQL |
| Authentication | Django Auth + JWT (python-jose) |
| Deployment | Render (two separate services) |
| Testing | pytest, httpx |

---

## Architecture

```
tontine-platform/
├── core/              # Django app — models, views, templates, signals
├── tontine/           # Django config — settings, urls, wsgi
├── api/               # FastAPI — independent REST API
│   ├── main.py        # Endpoints
│   ├── database.py    # PostgreSQL connection (psycopg2)
│   ├── auth.py        # JWT token creation and verification
│   └── test_main.py   # pytest test suite
├── seed.py            # Test data generation with Faker
└── Procfile           # Render deployment config
```

Two independent services share the same PostgreSQL database:
- **Django** handles the web interface, business logic, admin, and signals
- **FastAPI** exposes data as JSON for external consumers (mobile apps, frontends)

---

## Features

### Web Application (Django)
- Member registration and authentication
- Group creation and management
- Contribution cycle management with automatic contribution generation (Django signals)
- Payment tracking per member per cycle
- Analytics dashboard — participation rate, defaulters, financial summary per group

### REST API (FastAPI)
- `GET /members` — list all members
- `GET /members/{id}` — member detail
- `GET /contributions?status=paid` — contributions with optional filter
- `GET /groups/financial` — financial summary per group with SQL aggregation
- `POST /login` — JWT token generation
- All endpoints protected by OAuth2 Bearer token

### Data Pipeline (Pandas + psycopg2)
- ETL pipeline extracting data from PostgreSQL
- Participation rate per group
- Member reliability ranking
- Financial summary with expected vs paid vs missing amounts
- Direct psycopg2 pipeline independent of Django ORM

---

## Local Setup

### Prerequisites
- Python 3.13+
- PostgreSQL
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Allianzj04/tontine-platform.git
cd tontine-platform

# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file at the root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/tontine_db
DJANGO_SECRET_KEY=your-django-secret-key
FASTAPI_SECRET_KEY=your-fastapi-secret-key
DEBUG=True
```

### Database Setup

```bash
# Create the database in PostgreSQL
createdb tontine_db

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate with test data
python seed.py
```

### Run the Application

```bash
# Django (port 8000)
python manage.py runserver

# FastAPI (port 8001)
uvicorn api.main:app --reload --port 8001
```

---

## Tests

```bash
python -m pytest api/test_main.py -v
```

3 tests covering:
- Authenticated `GET /members` — happy path
- `POST /login` with invalid credentials — 401 response
- `GET /members/{id}` with non-existent ID — 404 response

---

## Data Model

```
Group (name, amount)
  └── Member (many-to-many)
  └── Cycle (status: active/completed)
        └── Contribution (status: paid/unpaid) ← auto-created by signal
        └── Round (beneficiary of the cycle)
```

---

## Payment Integration

Payment integration architecture designed for **Lumicash** and **eNoti** (Burundi mobile money providers). Awaiting merchant account credentials for production integration.

---

## Key Files

| File | Role |
|---|---|
| `core/models.py` | All Django models |
| `core/analytics.py` | Pandas ETL pipeline |
| `core/signals.py` | Auto-creates contributions on cycle creation |
| `api/main.py` | All FastAPI endpoints |
| `api/auth.py` | JWT logic |
| `api/database.py` | psycopg2 connection factory |
| `seed.py` | Faker-based test data generator |

---

## Author

Built by [@Allianzj04](https://github.com/Allianzj04) — L3 Software Engineering student, Burundi.  
Autodidact. This project is the centerpiece of my master's application in Data Engineering.
