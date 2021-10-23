from service.database.db import db_session
from service.database.models import Post, Wall
from dataclasses import dataclass


def get_last_post_id(wall_id):
    last_post_id = db_session.query(Wall.last_post_id).filter(Wall.wall_id == wall_id).first()
    if last_post_id:
        return str(last_post_id)
    else:
        return None


@dataclass
class WallConfig:
    uid: int
    wall_id: int
    link: str
    last_post_id: int


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


# Old way, currently not using
def get_last_post_id2(wall_id):
    last_post_id = db_session.query(Post.uid).filter(Post.group == wall_id).order_by(Post.created.desc()).first()[0]
    if last_post_id:
        return str(last_post_id)
    else:
        return None


def check_wall_exists(wall_id):
    wall_exists = db_session.query(Wall.name).filter(Wall.name == int(wall_id))
    if wall_exists:
        return True
    return False
