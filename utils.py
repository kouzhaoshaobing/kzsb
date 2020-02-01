import json
import os
BASE_PATH = 'backup/'


def ensure_path(path):
    if os.path.exists(path):
        return
    os.mkdir(path)
    return


def save_backup(name, content):
    content = json.dumps(content)
    ensure_path(BASE_PATH)
    path = os.path.join('backup/', '{}.json'.format(name))
    if os.path.exists(path):
        with open(path, 'r') as f:
            if f.read() == content:
                return
    with open(path, 'w+') as f:
        f.write(content)
    return


def load_backup(name):
    path = os.path.join(BASE_PATH, name)
    if not os.path.exists(path):
        return {}
    with open(path, 'r') as f:
        return f.read()
