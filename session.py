from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def session():
   engine = create_engine('sqlite:///lib/family.db')
   Session = sessionmaker(bind=engine)
   session = Session()
   return session


