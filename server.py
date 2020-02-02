import json
import requests
from flask import Flask
from flask import request
from flask.json import jsonify
from utils import save_backup, load_backup
from flask import render_template
import re
import os


app = Flask(__name__ , static_folder='assets', static_url_path='/kzsb/assets')



@app.errorhandler(404)
def page_miss(e):
    return '<h1>PAGE 404 ! </h1>Yuan is the best!'

@app.errorhandler(500)
def page_error(e):
    return '<h1>PAGE 500 ! </h1>Yuan is the best!'


@app.route('/kzsb/<string:route>/')
def shimo_handler(route):
    # doc_id = get_doc_id(route)
    resp_data = get_html(route)
    return render_template('text.html', **resp_data)


@app.route('/kzsb/')
def main_page():
    route = 'home'
    # resp_data = dict(
    #     page=route,
    #     content='<img src="/kzsb/assets/images/homeimg.jpg" />'
    # )
    resp_data = get_html(route)
    return render_template('text.html', **resp_data)
    # return doc_id

@app.route('/kzsb/test/')
def test():
    return 'ok'


def get_html(route):
    headers = {
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive',
    }
    doc_id = route if len(route) == 16 else get_doc_id(route)
    url = 'https://shimo.im/docs/{}/read'.format(doc_id)
    r = requests.get(url, headers= headers)
    r = r.content.decode('utf-8') if r else ''

    name = re.findall(r'<title>(.*?)</title>', r)
    content = re.findall(r'<div class="ql-editor">(.*?)</div>', r)
    # content = re.sub(r'<img.*?src.*?>', '', content[0]) if content else content
    if content:
        content = content[0]
        imgs = re.findall(r'https://uploader.shimo.im/f/.*?!thumbnail', content)
        for img in imgs:
            content = content.replace(img, save_img(img))
        content = re.sub('https://shimo.im/docs/', '/kzsb/', content)
        content = re.sub('_blank', '_self', content)
    reads = re.findall(r'<div id="file-page-footer"><div class=".*?"><span.*?>(.*?)<', r)
    # save_backup(doc_id, r)
    resp_data = dict(
        page=route,
        name=name[0] if content else '404',
        content=content if content else '<p>您查看的页面不存在！</p>',
        reads=reads[0] + ' 阅读' if reads else 'Page 404!',
        url=url
    )
    return resp_data

def save_img(url):
    name = url.replace('https://uploader.shimo.im/f/', 'assets/images/').replace('!thumbnail', '')
    if not os.path.exists(name):
        r = requests.get(url,stream=True)
        with open(name, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)
    return '/kzsb/'+name


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
        'home': 'Cqc3T3cxVGCpDtJQ',
        'handbook': 'TXWgjPCDyXkrqWrX',
        'about': 'qkRQgTcHT6yrq6xQ',
        'help': '8cKJRcwvcDGCD3tJ',
        'qa': 'd6qDkhhGV3WVCWcW',
        'manga': '9HrtJTWCP8xtr86g',
        'friends': 'p6KrJhdWVTpvvJwV'
    }
    return mapping.get(route, 'Cqc3T3cxVGCpDtJQ')


if __name__ == "__main__":
    # app.run(debug=True, auto_reload=True)
    app.run(debug=True)