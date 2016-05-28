import json

import numpy
from flask import Flask, request, send_from_directory

from classifier import SimpleClassifier

app = Flask(__name__, static_url_path='', static_folder='')
classifiers = {'clf_edu': SimpleClassifier()}


def classify(comment, clf):
    with open('../db/sample', 'r') as f:
        data = json.load(f)

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


@app.route('/', methods=['GET', 'POST'])
def index():
    with open('index.html', 'r') as f:
        return f.read()


@app.route('/results')
def results():
    with open('results.html', 'r') as f:
        return f.read()


@app.route('/words_cloud')
def w_cloud():
    print('here')
    with open('db/words_cloud.png') as f:
        return f.read()


@app.route('/req_comment', methods=['GET', 'POST'])
def req_comment():
    req = request.get_json()
        # MakingDB().init(public_list=req['groups'])
    print(req)
    results = {}
    for clf in req['clfs']:
        results[clf] = classify(req['comments'], classifiers[clf])
    else:
        res = ''
        for estim in results.items():
            res += '<tr>'
            res += '<th>' + estim[0] + '</th>'
            res += '<th>' + estim[1] + '</th>'
            res += '</tr>'
        with open('db/results', 'w') as f:
            f.write(res)
        return 'OK' # jsonify(results)


@app.route('/results_file')
def results_file():
    with open('db/results', 'r') as f:
        return f.read()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
