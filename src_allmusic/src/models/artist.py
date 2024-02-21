from sqlalchemy import Column, Integer, String, DateTime, func

from database.database import Base


class Artist(Base):
    __tablename__ = 'artists'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(length=50), unique=True, nullable=False)
    url = Column(String(length=100), nullable=False)
    genres = Column(String(length=100), nullable=True, default='')
    decades = Column(String(length=100), nullable=True, default='')
    date_created = Column(DateTime,  default=func.current_timestamp())
    date_modified = Column(DateTime, default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return "<Artist({id}, {n})>".format(id=self.id, n=self.name)

    def __str__(self):
        return "{name}".format(name=self.name)
