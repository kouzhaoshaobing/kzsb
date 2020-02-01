import json
import requests
from flask import Flask
from flask import request
from flask.json import jsonify
from utils import save_backup, load_backup
from flask import render_template


app = Flask(__name__)


@app.route('/<string:route>')
def shimo_handler(route):
    doc_id = get_doc_id(route)
    resp_data = get_content(doc_id)
    return render_template('base.html', **resp_data)


@app.route('/')
def main_page():
    doc_id = get_doc_id('')
    resp_data = get_content(doc_id)
    return render_template('base.html', **resp_data)


def get_content(doc_id):
    r = requests.get('https://api.shimo.im/files/{}?html=true'.format(doc_id))
    r = json.loads(r.content)
    if not r:
        r = load_backup(doc_id)
    save_backup(doc_id, r)
    name = r.get('name', '')
    content = r.get('content', {})
    updated = r.get('updated_at', '')
    resp_data = dict(
        name=name,
        content=content,
        updated=updated
    )
    return resp_data


def get_doc_id(route):
    mapping = {
        'about': 'qkRQgTcHT6yrq6xQ',
        'help': '8cKJRcwvcDGCD3tJ',
        'qa': 'd6qDkhhGV3WVCWcW',
        'manga': '9HrtJTWCP8xtr86g',
        'friends': 'p6KrJhdWVTpvvJwV'
    }
    return mapping.get(route, 'Cqc3T3cxVGCpDtJQ')
