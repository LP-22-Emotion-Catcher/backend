from flask import Flask, jsonify, request
import http, logging
import httpx

app = Flask(__name__)


@app.route("/api/v1/messages", methods = ['POST'])
def get_messages():
    data = request.json
    message = data['message']
    logging.info(message)
    return '', http.HTTPStatus.NO_CONTENT


@app.route("/api/v1/emotions", methods = ['POST'])
def get_emotions():
    data = request.json
    text = data['text']
    payload = {'text': text}
    emotion = httpx.post('http://127.0.0.1:5000/api/v1/predict', json = payload)
    logging.info('%s: %s\n\n', emotion.json()['emotions'], text)
    return '', http.HTTPStatus.NO_CONTENT


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=5001, debug=True)
