from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer

Base = declarative_base()


class Keys(Base):
    __tablename__ = 'keys'
    id = Column(Integer, primary_key=True)
    key_name = Column(String(32), unique=True)
    key_value = Column(String(64), unique=True)
    description = Column(String(64))

    def __init__(self, id, key_name, key_value, descriptiom):
        self.id = id
        self.key_name = key_name
        self.key_value = key_value
        self.description = descriptiom
