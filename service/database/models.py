from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import relationship

from service.database.db import Base, engine


class Wall(Base):
    __tablename__ = 'walls'

    id = Column(Integer, primary_key=True)
    wall_id = Column(Integer)
    link = Column(String)
    last_post_id = Column(Integer)
    # posts = relationship('Post', lazy='joined', backref='walls')

    def __repr__(self):
        return f'Wall id: {self.id}, name: {self.name}'


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer)
    link = Column(String)
    wall_id = Column(Integer)
    author_id = Column(Integer)
    text = Column(String)
    created = Column(String)
    likes = Column(Integer)
    reposts = Column(Integer)
    comments = Column(Integer)
    views = Column(Integer)
    emotion = Column(ARRAY(String))

    # wall = relationship('Wall', lazy='joined', backref='posts')

    def __repr__(self):
        return f'Post id: {self.id}, text: {self.text}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
