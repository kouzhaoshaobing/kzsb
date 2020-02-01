import json
import requests
from flask import Flask
from flask import request
from flask.json import jsonify
from utils import save_backup, load_backup


app = Flask(__name__)


@app.route('/')
def shimo_handler():
    doc_id = request.args.get('docId', 'TXWgjPCDyXkrqWrX')
    r = requests.get('https://api.shimo.im/files/{}?html=true'.format(doc_id))
    r = json.loads(r.content)
    if not r:
        r = load_backup(doc_id)
    save_backup(doc_id, r)
    name = r.get('name', '')
    content = r.get('content', {})
    resp = dict(
        name=name,
        content=content
    )
    return jsonify(resp)
