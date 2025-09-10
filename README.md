#  Stock Trading Application

A scalable stock trading backend system built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Redis**, and **Celery**.  
A lightweight **Streamlit frontend** is included for easy interaction with the APIs.

---

##  Features
### Backend
-  User authentication with JWT (signup, login, role-based access).
-  Deposit and withdraw funds.
-  Add and list coins (only master/admin user can add).
-  Buy and sell coins with **Celery task queue**.
-  PostgreSQL as the main database.
-  Redis as a broker for Celery (task queue).

### Frontend (Streamlit)
- User login and signup forms.
- Display user info in a clean table.
- View wallets and coin information in tabular format.
- Update profile info (username, email, password — optional).
- Logout button to return to login page.
- Simple, interactive UI for all user operations.

---

## Tech Stack
- **FastAPI** (API framework)
- **SQLAlchemy** (ORM)
- **PostgreSQL** (Relational Database)
- **Redis** (In-memory DB / Celery broker)
- **Celery** (Background task processing)
- **Pydantic** (Data validation)
- **Streamlit** (Frontend UI)

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

### - Start Steamlit server
```bash
.streamlit run app.py
```

### This will start:

- FastAPI server → http://localhost:8000
- PostgreSQL → on port 5432
- Redis → on port 6379
- Celery worker → running in background
- Streamlit UI → http://localhost:8501
## API Endpoints

###  Auth
- `POST /login` → Login with username & password (returns JWT token)
- `POST /signup` → Create a new user  
### Users

 
- `GET /user/info` → Get my info  
- `GET /user/wallets` → Get my wallets  
- `GET /user/trade` → Get my trades
- `PUT /user/update` → Update my info  
- `DELETE /user/me` → Delete my account  
- `GET /all_users` → Get all users basic Info 

### Wallets
- `POST /wallet/recharge` → Recharge account balance  
- `POST /wallet/deposit` → Deposit into wallet using account balance 
- `POST /wallet/withdraw` → Withdraw from wallet and add to account balance

### Coins
- `GET /coin/available_coins` → Show all available coins  
- `POST /coin/add` → Add a coin (Admin only )  
- `POST /coins/buy` → Place a buy order (coin_id, quantity of coins, price of the coin)  
- `POST /coins/sell` → Place a sell order (coin_id, quantity of coins, price of the coin)   
- `GET /tasks/{task_id}` → Check status of buy/sell task  

