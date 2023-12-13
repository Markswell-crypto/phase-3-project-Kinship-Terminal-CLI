from faker import  Faker
import random


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.modules import Person, connections, Relationship, User

if __name__ == '__main__':
    engine = create_engine('sqlite:///lib/family.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    session.query(Person).delete()
    session.query(connections).delete()
    # session.query(Relationship).delete()
    
    # session.add(Relationship(type_of_relationship='Parent'))
    # session.add(Relationship(type_of_relationship='Spouse'))
    # session.add(Relationship(type_of_relationship='Child'))
    # session.commit()

    fake = Faker()

    # ------------------------ Populate customer table --------------------------
    people = []
    for i in range(10):
        person = Person(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            user_id = 5,
        )
        session.add(person)
        session.commit()
        people.append(person)

    user1 = []
    for i in range(10):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
           
        )
        session.add(user)
        session.commit()
        user1.append(user)