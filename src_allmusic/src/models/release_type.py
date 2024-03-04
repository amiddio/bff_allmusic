from sqlalchemy import Column, Integer, String

from database.database import Base


class ReleaseType(Base):
    """
    Модель типа релиза альбома
    """

    __tablename__ = 'release_types'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type = Column(String(length=50), unique=True, nullable=False)
    name = Column(String(length=50), nullable=False)

    def __repr__(self):
        return "<ReleaseType({id}, {type}, {name})>".format(id=self.id, type=self.type, name=self.name)

    def __str__(self):
        return "{name}".format(name=self.name)
