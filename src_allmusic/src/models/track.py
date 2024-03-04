from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Track(Base):
    """
    Модель трека/песни
    """

    __tablename__ = 'tracks'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    album_id = Column(Integer, ForeignKey('albums.id'), name='album_id', index=True, nullable=False)
    num = Column(String(length=3))
    title = Column(String(length=300), nullable=False)
    disc = Column(String(length=10))
    duration = Column(String(length=10))
    composers = Column(String(length=300))
    performers = Column(String(length=300))

    album = relationship('Album', backref='tracks')

    def __repr__(self):
        return "<Track({id}, {n}, {t})>".format(id=self.id, n=self.num, t=self.title)
