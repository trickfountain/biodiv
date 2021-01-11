from app.forms import imageSelector

from flask.helpers import flash, get_root_path
from app import app
from flask import url_for, render_template
from pathlib import Path
## TODO: sort relative imports for docker version.

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'biodiv'))
from biodiv.detection import V1, draw_ROI
import cv2


@app.route('/')
@app.route('/index')
def index():
    img_dir = Path(app.root_path) / 'static' / 'img'

    images = img_dir.glob('*')
    img_name_and_url = [(p.name,  url_for_static(p)) for p in images]

    # test dict: values used in troubleshooting
    app_instance_path = app.instance_path
    test_dict = {
        'app_root_path': app.root_path,
        'app_instance_path': app_instance_path,
        'img_dir': img_dir,
        'images': list(img_dir.glob('*')),
        'img_name_and_url': img_name_and_url,
        'secret_key': app.config['SECRET_KEY']
    }

    return render_template('main.html',
                           test_dict=test_dict,
                           imd_dir=img_dir,
                           img_name_and_url=img_name_and_url)


def url_for_static(file_path):
    '''url_for() wrapper used to point to static files'''

    static_pth = Path(app.root_path) / 'static'
    file_pth = Path(file_path).absolute()

    rel_pth = file_pth.relative_to(static_pth)
    url = url_for('static', filename=rel_pth)
    return url

# d: faster way to get to url during development


@app.route('/d', methods=['GET', 'POST'])
@app.route('/detection', methods=['GET', 'POST'])
def detection():
    form = imageSelector()
    src_url = None
    det_url = None
    test_dict = {}
## TODO: refactor, very messy.
    if form.validate_on_submit():
        src = form.pick_img.data
        src_url = url_for_static(src)

    if src_url is not None:
        src_pth = Path(src)
        src_name = src_pth.name
        det_name = src_name.split('.')[0] + '_det.png'
        det_pth = src_pth.parent.parent.joinpath(f'detected/{det_name}')

        if det_pth.is_file():
            det_url = url_for_static(det_pth)
        ## TODO: Add trigger/submit button to detect.
        ## TODO: add delete detected option
        else:
            res_img, ROIs = V1(str(src_pth))
            out = draw_ROI(res_img.copy(), ROIs)
            cv2.imwrite(str(det_pth), out)
            det_url = url_for_static(det_pth)

    test_dict = {
        'src_pth': src_pth,
        'src_name': src_name,
        'det_name': det_name,
        'det_pth': det_pth
    }

    return render_template('detection.html',
     form=form, src_url=src_url, det_url=det_url, test_dict=test_dict)
