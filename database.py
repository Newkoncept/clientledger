from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
from dotenv import load_dotenv

# Load variables from .env into the system environment
load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DB_CONNECTION")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("Missing DB_CONNECTION environment variable")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()