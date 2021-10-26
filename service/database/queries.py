from service.database.db import db_session
from service.database.models import Post, Wall
from dataclasses import dataclass


@dataclass
class WallConfig:
    uid: int
    wall_id: int
    link: str
    last_post_id: int


@dataclass
class PostConfig:
    post_id: int
    text: str
    emotion: str


def get_last_post_id(wall_id):
    last_post_id = db_session.query(Wall.last_post_id).filter(Wall.wall_id == wall_id).first()
    if last_post_id:
        return str(last_post_id)
    else:
        return None


def get_walls():
    walls = Wall.query.all()
    return [
        WallConfig(
            uid=wall.id,
            wall_id=wall.wall_id,
            link=wall.link,
            last_post_id=wall.last_post_id,
        )
        for wall in walls
    ]


def get_posts(uid, emotion):
    posts = Post.query.filter(Post.wall_id == uid).filter(Post.emotion == emotion).all()
    return [
        PostConfig(
            post_id=post.post_id,
            text=post.text,
            emotion=post.emotion,
        )
        for post in posts
    ]
