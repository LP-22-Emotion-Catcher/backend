import http
import httpx
import logging

from flask import Flask, request
from service.config import emotion_url

app = Flask(__name__)


@app.route("/api/v1/messages", methods=['POST'])
def process_message():
    data = request.json
    print(data)
    text = data['text']
    payload = {'text': text}
    emotion = httpx.post(emotion_url, json=payload)
    logging.info('%s: %s\n\n', emotion.json()['emotions'], text)

    # TODO: save result and message to database
    return '', http.HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5001, debug=True)
