from database.db import db_session
from database.models import Wall, Post


def save_wall(data):
    walls = []
    wall = {'name': data['uid'],
            'link': data['link']
            }
    walls.append(wall)

    db_session.bulk_insert_mappings(Wall, walls, return_defaults=True)
    db_session.commit()
    return walls


def save_post(data):
    posts = []
    post = {'uid': data['uid'],
            'link': data['link'],
            'author': data['author'],
            'text': data['text'],
            'likes': data['likes'],
            'reposts': data['reposts'],
            'comments': data['comments'],
            'views': data['views'],
            'emotion': data['emotion'],
            'created': data['created'],
            }
    posts.append(post)

    db_session.bulk_insert_mappings(Post, posts, return_defaults=True)
    db_session.commit()
    return posts
