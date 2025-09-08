#  Stock Trading Backend

A scalable stock trading backend system built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Redis**, and **Celery**.  
This project demonstrates clean architecture, asynchronous task handling, and secure API development.

---

##  Features
-  User authentication with JWT (signup, login, role-based access).
-  Deposit and withdraw funds.
-  Add and list coins (only master/admin user can add).
-  Buy and sell coins with **Celery task queue**.
-  PostgreSQL as the main database.
-  Redis as a broker for Celery (task queue).

---

## Tech Stack
- **FastAPI** (API framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Relational Database)
- **Redis** (In-memory DB / Celery broker)
- **Celery** (Background task processing)
- **Pydantic** (Data validation)



---

## Setup & Installation

### 1️. Clone the repo
```bash
git clone https://github.com/mrmudasir05/stock-trading.git
cd stock-trading
```
### 2.  Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows

```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure .env
```aiignore
ADMIN_DB_NAME = "postgres" # admin database name
DB_USER = "postgres"  #username
DB_PASSWORD = "password"  # password
DB_HOST = "localhost"   # Host
DB_PORT = "5432"   #port
DB_NAME = "stocktrading"  # Database name if present otherwise create new with this name

REDIS_URL = "redis://localhost:6379/0"  # Redis URL
SECRET_KEY="change-this-to-a-strong-random-string"   # secret key for JWT

```

## Running the Project (Locally)
### - Start FastAPI server
```bash
uvicorn app.main:app --reload
```
### - Start Redis
```redis
redis-server
```

### - Start Celery worker
```bash
celery -A app.utils.tasks.celery_app worker --loglevel=info
```

### This will start:

- FastAPI server → http://localhost:8000
- PostgreSQL → on port 5432
- Redis → on port 6379
- Celery worker → running in background

## API Endpoints

###  Auth
- `POST /login` → Login with username & password (returns JWT token)

### Users
- `POST /signup` → Create a new user  
- `GET /users` → Get all users basic Info  
- `GET /user/info` → Get my info  
- `PUT /users/update` → Update my info  
- `DELETE /users/me` → Delete my account  

### Wallets & Balance
- `POST /user/recharge` → Recharge account balance  
- `POST /wallets/deposit` → Deposit into wallet using account balance 
- `POST /wallets/withdraw` → Withdraw from wallet and add to account balance
- `GET /user/wallets` → Get my wallets  

### Coins
- `GET /available_coins` → Show all available coins  
- `POST /coins/add` → Add a coin (Admin only )  

### Trading (Async with Celery)
- `POST /coins/buy` → Place a buy order (coin_id, quantity of coins, price of the coin)  
- `POST /coins/sell` → Place a sell order (coin_id, quantity of coins, price of the coin)   
- `GET /tasks/{task_id}` → Check status of buy/sell task  

---
