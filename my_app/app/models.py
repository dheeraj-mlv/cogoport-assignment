from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Configuration(Base):
    __tablename__ = 'configurations'
    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, unique=True, index=True, nullable=False)
    requirements = Column(JSON, nullable=False)
