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

from flask import request
import flask
import houdini_nodeshape_converter
import io

bp = flask.Blueprint('houdini_nodeshape_converter', __name__,
  template_folder='flask_templates')

@bp.route('/', methods=['GET', 'POST'])
def index():
  errmsg = None
  json = None
  if request.method == 'POST':
    try:
      xres = request.form.get('xres')
      yres = request.form.get('yres')
      if xres or yres:
        try:
          xres = int(xres)
        except ValueError as exc:
          raise ValueError('xres: {}'.format(exc))
        try:
          yres = int(yres)
        except ValueError as exc:
          raise ValueError('yres: {}'.format(exc))
        inputdim = (xres, yres)
      else:
        inputdim = None
      name = request.form.get('name')
      svgstring = request.form.get('svgstring').strip()
      svgfile = request.files.get('svgfile')
      if bool(svgstring) == bool(svgfile):
        raise ValueError('specify either SVG String or SVG File')
    except ValueError as exc:
      errmsg = str(exc)
    else:
      if svgstring:
        svgfile = io.StringIO(svgstring)
      try:
        json = houdini_nodeshape_converter.convert(svgfile, inputdim, name=name)
      except houdini_nodeshape_converter.ExpatError as exc:
        errmsg = str(exc)
  return flask.render_template('houdini-nodeshape-converter/index.html',
    errmsg=errmsg, shape_json=json)

def main():
  app = flask.Flask(__name__)
  app.register_blueprint(bp)
  app.run(debug=True)

if __name__ == '__main__':
  main()
