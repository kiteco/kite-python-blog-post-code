import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# We will add classes here
class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    genre = Column(String(250))

    @property
    def serialize(self):
        return {
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'id': self.id,
        }


# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///books-collection.db')
Base.metadata.create_all(engine)
