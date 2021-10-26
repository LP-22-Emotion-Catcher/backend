import http
import httpx
import logging

from flask import Flask, request, jsonify, abort
from pydantic import ValidationError
from service.config import emotion_url

from service.database.loader import save_wall, save_post, update_last_post_id, save_comment
from service.database import queries

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/api/v1/messages", methods=['POST'])
def process_message():
    try:
        data = request.json
    except ValidationError as e:
        abort(400, str(e))
    text = data['text']
    payload = {'text': text}

    try:
        emotion = httpx.post(emotion_url, json=payload)
    except httpx.ConnectError:
        logger.debug('can\'t connect with emotion service')

    logging.info('%s: %s\n\n', emotion.json()['emotions'], text)
    data['emotion'] = emotion.json()['emotions']

    save_post(data)
    update_last_post_id(wall_id=data['wall'], post_id=data['uid'])
    return '', http.HTTPStatus.CREATED


@app.route('/api/v1/walls', methods=['POST'])
def add_wall():
    try:
        data = request.json
    except ValidationError as e:
        abort(400, str(e))

    save_wall(data)
    return '', http.HTTPStatus.CREATED


@app.route("/api/v1/walls/<uid>", methods=['GET'])
def process_wall(uid):
    return queries.get_last_post_id(uid)


@app.route("/api/v1/walls/", methods=['GET'])
def get_walls():
    walls = queries.get_walls()
    return jsonify(walls), http.HTTPStatus.OK


@app.route('/api/v1/walls/<uid>/posts/', methods=['GET'])
def get_posts(uid):
    emotion = request.args.get('emotion')
    posts = queries.get_posts(uid, emotion)
    return jsonify(posts), http.HTTPStatus.OK


@app.route("/api/v1/comments", methods=['POST'])
def process_comment():
    try:
        data = request.json
    except ValidationError as e:
        abort(400, str(e))

    save_comment(data)
    return '', http.HTTPStatus.CREATED


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5001, debug=True)
