from flask_wtf import FlaskForm

from wtforms import SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from wtforms.form import Form
from app import app
from pathlib import Path


class imageSelector(FlaskForm):
    img_src_dir = Path(app.root_path) / 'static' / 'img' / 'src'
    img_src_pth = img_src_dir.glob('*.png')
    img_options = [ (p, p.name) for p in img_src_pth]

    pick_img = SelectField('pick image to detect',
                           choices=img_options, validators=[DataRequired()])
    pick_img_submit = SubmitField('Pick image')
