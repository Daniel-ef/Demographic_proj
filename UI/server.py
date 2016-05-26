import json

import numpy
from flask import Flask, request, send_from_directory, jsonify

from classifier import SimpleClassifier

app = Flask(__name__, static_url_path='')


def classify(comment):
    with open('../db/sample', 'r') as f:
        data = json.load(f)
    clf = SimpleClassifier()

    x = []
    y = []

    for group in data['comments-class']:
        for com_label in group.items():
            x.append(com_label[0])
            y.append(com_label[1])
    x, y = numpy.array(x), numpy.array(y)
    clf.fit(x, y)
    result = data['class_names'][str(clf.predict(numpy.array([comment]))[0])]
    return result


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route('/')
def index():
    with open('index.html', 'r') as f:
        return f.read()


@app.route('/req_comment', methods=['GET', 'POST'])
def req_comment():
    prediction = classify(request.data)
    return jsonify(result={"status": 200, "prediction": prediction})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
