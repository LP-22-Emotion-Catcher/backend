import http
import httpx
import logging

from flask import Flask, request, jsonify
from service.config import emotion_url

from service.database.loader import save_wall, save_post, update_last_post_id
from service.database import queries

app = Flask(__name__)


@app.route("/api/v1/messages", methods=['POST'])
def process_message():
    data = request.json
    text = data['text']
    payload = {'text': text}
    emotion = httpx.post(emotion_url, json=payload)
    logging.info('%s: %s\n\n', emotion.json()['emotions'], text)
    data['emotion'] = emotion.json()['emotions']
    save_post(data)
    update_last_post_id(wall_id=data['wall'], post_id=data['uid'])
    return '', http.HTTPStatus.CREATED


@app.route('/api/v1/walls', methods=['POST'])
def add_wall():
    data = request.json
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


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5001, debug=True)
