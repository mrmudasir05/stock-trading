import os

from sqlalchemy import create_engine,text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_DB_NAME = os.getenv("ADMIN_DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

ADMIN_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{ADMIN_DB_NAME}"
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# First connect to 'postgres'
admin_engine = create_engine(ADMIN_URL, isolation_level="AUTOCOMMIT")

try:
    with admin_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE {DB_NAME} ENCODING 'utf8' TEMPLATE template1;"))
        print(f"Database {DB_NAME} created")
except ProgrammingError:
    print(f"Database {DB_NAME} already exists")

# Now connect to your actual app DB
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass