from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DB_USERNAME = os.environ['DB_USERNAME']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
DB_HOST = os.environ['DB_HOST']
print(DB_NAME, DB_PASSWORD, DB_USERNAME)
engine = create_engine(
    'mysql+pymysql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME))
Session = sessionmaker(bind=engine)
session = Session()
