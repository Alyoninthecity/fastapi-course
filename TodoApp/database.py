from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

#SQLALCHEMY_DATABASE_URL= 'sqlite:///./todosapp.db' #Per SQLite3

load_dotenv() # .env

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL") # SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:<password>@localhost/TodoApplicationDatabase'


engine = create_engine(SQLALCHEMY_DATABASE_URL\
    #, connect_args={'check_same_thread':False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()