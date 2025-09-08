from sqlalchemy import create_engine,text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "stocktrading"

ADMIN_URL = f"postgresql+psycopg2://postgres:password@{DB_HOST}:{DB_PORT}/postgres"
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
class Base(DeclarativeBase):
    pass