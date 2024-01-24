import credentials
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://{credentials.username}:" \
               f"{credentials.password}@{credentials.host}/{credentials.database_name}"

# create an engine
engine = create_engine(DATABASE_URL)

# create a session
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()
