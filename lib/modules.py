from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Define the connections table for the many-to-many relationship
connections = Table(
    'connections',
    Base.metadata,
    Column('individual1_id', Integer, ForeignKey('people.id'), nullable=False),
    Column('individual2_id', Integer, ForeignKey('people.id'), nullable=False),
    Column('relationship_id', Integer, ForeignKey('relationships.id'), primary_key=True),
    Column('users_id', Integer, ForeignKey('users.id'), primary_key=True)
)


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_relashionship= Column(String)

    # Define the many-to-many relationship with Relationship
    relationships = relationship(
        'Relationship',
        secondary=connections,
        primaryjoin=(connections.c.individual1_id == id),
        secondaryjoin=(connections.c.relationship_id == id),
        back_populates='people'
    )


class Relationship(Base):
    __tablename__ = "relationships"

    id = Column(Integer, primary_key=True)
    type_of_relationship = Column(String, index=True)

    # Define the many-to-many relationship with Person
    people = relationship(
        'Person',
        secondary=connections,
        primaryjoin=(connections.c.relationship_id == id),
        secondaryjoin=(connections.c.individual2_id == id),
        back_populates='relationships'
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    user_relashionship= Column(String)

    # Define the one-to-many relationship with Person
    family = relationship('Person', backref=backref('users'))
