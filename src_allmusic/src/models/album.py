from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base


class Album(Base):
    __tablename__ = 'albums'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'), name='artist_id', index=True, nullable=False)
    release_type_id = Column(
        Integer, ForeignKey('release_types.id'), name='release_type_id', index=True, nullable=False
    )
    title = Column(String(length=300), nullable=False)
    url = Column(String(length=500), nullable=False)
    year = Column(String(length=10))
    label = Column(String(length=50))
    cover_url = Column(String(length=300))
    music_rating = Column(String(length=10))
    avg_rating = Column(String(length=10))
    duration = Column(String(length=50))
    genre = Column(String(length=200))
    styles = Column(String(length=400))

    artist = relationship('Artist', backref='albums')

    def __repr__(self):
        return "<Album({id}, {t}, {y})>".format(id=self.id, t=self.title, y=self.year)

    def __str__(self):
        return "{title} {year}".format(title=self.title, year=self.year)
