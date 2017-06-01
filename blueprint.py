# Copyright (c) 2017 Niklas Rosenstein
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import datetime
from flask import abort, current_app as app, render_template, request
from flask_restful import reqparse
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import IntegerField, StringField
from wtforms.validators import Optional
from werkzeug.utils import secure_filename

import flask
import io
import os
import {convert} from './convert'

blueprint = flask.Blueprint(
  'houdini_nodeshape_converter', __name__,
  template_folder=os.path.join(__directory__, 'templates')
)


def storage_dir():
  """
  Returns the directory where generated nodeshapes are stored.
  """
  return app.config.get('HOUDINI_NODESHAPE_CONVERTER_STOREAGEDIR',
    os.path.join(__directory__, '_storage'))


def stored_shapes():
  """
  Returns a list of all stored shapes.
  """
  dirname = storage_dir()
  if not os.path.isdir(dirname): return []
  result = []
  for name in os.listdir(dirname):
    if name.endswith('.json'):
      result.append(name[:-5])
  result.sort()
  return result


def create_shape(name, svgdata, xres=None, yres=None):
  if bool(xres) != bool(yres):
    raise ValueError('Both of X Res and Y Res must be specified.')
  inputdim = (int(xres), int(yres)) if xres else None
  data = convert(io.BytesIO(svgdata), inputdim=inputdim, name=name)
  dirname = storage_dir()
  if not os.path.isdir(dirname):
    os.makedirs(dirname)
  basename = secure_filename(datetime.now().strftime('%Y%m%d%H%M%S_' + name))
  filename = os.path.join(dirname, basename)
  with open(filename + '.svg', 'wb') as fp:
    fp.write(svgdata)
  with open(filename + '.json', 'w') as fp:
    fp.write(data)
  return basename, data


class ConvertForm(FlaskForm):
  name = StringField('Name')
  xres = IntegerField('X Resolution', validators=[Optional()])
  yres = IntegerField('Y Resolution', validators=[Optional()])
  svg_file = FileField('SVG File', validators=[FileRequired()])


@blueprint.route('/', methods=['GET', 'POST'])
def index():
  """
  GET: Show the Houdini NodeShape Converter form.
  POST: Convert an SVG file to a Houdini JSON NodeShape.
  """

  form = ConvertForm()
  if request.method == 'POST' and form.validate_on_submit():
    shape, data = create_shape(form.name.data, form.svg_file.data.read(),
      form.xres.data, form.yres.data)
    cdisp = 'attachment; filename="{}.json"'.format(form.name.data)
    return flask.Response(data, mimetype='text/json',
      headers={'Content-Disposition': cdisp})

  return flask.render_template(
    'houdini-nodeshape-converter/index.html',
    form = form,
    shapes = stored_shapes()[:20]
  )


@blueprint.route('/shape/<shape>.json')
def shape_json(shape):
  return flask.send_from_directory(storage_dir(), shape + '.json')


@blueprint.route('/shape/<shape>.svg')
def shape_svg(shape):
  return flask.send_from_directory(storage_dir(), shape + '.svg')


def main():
  app = flask.Flask(__name__)
  app.config['SECRET_KEY'] = 'foobar'
  app.register_blueprint(blueprint)
  app.run(debug=True)


if ('require' in globals() and require.main == module) or __name__ == '__main__':
  main()
