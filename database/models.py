from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base, engine


class Wall(Base):
    __tablename__ = 'walls'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    link = Column(String)
    posts = relationship('Post', lazy='joined', backref='walls')

    def __repr__(self):
        return f'Wall id: {self.id}, name: {self.name}'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    wall_id = Column(Integer, ForeignKey(Wall.id), index=True, nullable=False)

    uid = Column(Integer)
    link = Column(String)
    author = Column(Integer)
    text = Column(String)
    created = Column(Date)
    likes = Column(Integer)
    reposts = Column(Integer)
    comments = Column(Integer)
    views = Column(Integer)
    emotion = Column(String)

    wall = relationship('Wall', lazy='joined', backref='posts')

    def __repr__(self):
        return f'Post id: {self.id}, text: {self.text}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
