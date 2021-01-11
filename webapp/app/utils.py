from pathlib import Path
from app import app
from flask import url_for

def url_for_static(file_path):
    '''url_for() wrapper used to point to static files'''

    static_pth = Path(app.root_path) / 'static'
    file_pth = Path(file_path).absolute()

    rel_pth = file_pth.relative_to(static_pth)
    url = url_for('static', filename=rel_pth)
    return url


file_pth = 'app/static/img/cats1_det.png'
print(url_for_static(file_pth))

