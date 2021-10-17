# from config import postgres_user, postgres_pass, db_url, postgres_db

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session


#   engine = create_engine(f'postgresql://{postgres_user}:{postgres_pass}@{db_url}:5432/{postgres_db}')
engine = create_engine("postgresql://emorec:emorec@localhost:5432/posts")
db_session = scoped_session(sessionmaker(bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()
