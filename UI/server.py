import json
import os

import numpy
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

import wcloud
from classifier import SimpleClassifier
from make_db import MakingDB

app = Flask(__name__, static_url_path='', static_folder='')
app.config['UPLOAD_FOLDER'] = 'db/upload'


classifiers = {'clf_edu': SimpleClassifier()}
clf_names = {'sample_edu': 'Education', 'sample_sex': 'Sex', 'sample_age': 'Age'}


def classify(comment, sample_name):
    clf = SimpleClassifier()
    with open('../db/' + sample_name, 'r') as f:
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


@app.route('/', methods=['GET', 'POST'])
def index():
    print(request.url)
    if request.method == 'POST':
        print(request.files['file'])
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    else:
        with open('index.html', 'r') as f:
            return f.read()


@app.route('/results')
def results():
    with open('results.html', 'r') as f:
        return f.read()


@app.route('/req_comment', methods=['GET', 'POST'])
def req_comment():
    req = request.get_json()
    sample_name = 'sample'

    if req['groups'] != []:
        public_l = req['groups']
        print(public_l[:-1], int(public_l[len(public_l) - 1]))
        MakingDB().init(public_list=public_l[:-1]
                        , comments_amount=int(public_l[len(public_l) - 1])
                        , sample_name='sample1')
        sample_name = 'sample1'

    results = {}
    for clf in req['clfs']:
        results[clf] = classify(req['comments'], clf)
    else:
        res = ''
        wcloud.init()
        for estim in results.items():
            res += '<tr>'
            res += '<th>' + clf_names[estim[0]] + '</th>'
            res += '<th>' + estim[1] + '</th>'
            res += '</tr>'
        with open('db/results', 'w') as f:
            f.write(res)
        return 'OK'


@app.route('/upload_file', methods=['GET', 'POST'])
def handling_uploading():
    print(request.files)
    file=request.files['myfile']
    file.save('db/upload_file')
    return 'OK'


@app.route('/results_file')
def results_file():
    with open('db/results', 'r') as f:
        return f.read()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
