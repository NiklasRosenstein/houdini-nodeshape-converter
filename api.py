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
from flask import request, make_response, current_app as app
from flask_restful import abort, reqparse, Api, Resource
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import flask
import io
import json
import os
import werkzeug
import {convert} from './convert'


def storage_dir():
  return app.config.get('HOUDINI_NODESHAPE_CONVERTER_STOREAGEDIR',
    os.path.join(str(module.directory), '_storage'))


def int_or_empty(value):
  if not value:
    return None
  return int(value)


class HoudiniNodeshapeConverter(Resource):

  parser = reqparse.RequestParser()
  parser.add_argument('name', required=False)
  parser.add_argument('xres', type=int_or_empty, required=False)
  parser.add_argument('yres', type=int_or_empty, required=False)
  parser.add_argument('file', type=FileStorage, location='files')

  get_parser = reqparse.RequestParser()
  get_parser.add_argument('shape_id', required=True)
  get_parser.add_argument('filename', required=False)

  def get(self):
    args = self.get_parser.parse_args()
    if not args.shape_id:
      abort(404, message='No shape ID')
    try:
      return flask.send_from_directory(storage_dir(), args.shape_id + '.json',
        as_attachment=True, attachment_filename=(args.filename or None))
    except werkzeug.exceptions.NotFound as exc:
      abort(404, message='Shape does not exist.')

  def post(self):
    args = self.parser.parse_args()
    if not args.file:
      abort(400, message={'file': 'parameter is required'})
    if (args.xres is None) != (args.yres is None):
      a, b = ('xres', 'yres') if args.yres is None else ('yres', 'xres')
      abort(400, message={a: "can not stand alone without {} being set".format(b)})

    if not args.name:
      args.name = os.path.basename(os.path.splitext(args.file.filename)[0])

    inputdim = (args.xres, args.yres) if args.xres else None
    svgdata = args.file.read()
    try:
      data = convert(io.BytesIO(svgdata), inputdim=inputdim, name=args.name)
      data = json.dumps(data, indent=2, sort_keys=True)
    except Exception as exc:
      abort(400, message={'file': str(exc)})

    # Save the shape.
    dirname = storage_dir()
    if not os.path.isdir(dirname):
      os.makedirs(dirname)
    basename = secure_filename(datetime.now().strftime('%Y%m%d%H%M%S_' + args.name))
    filename = os.path.join(dirname, basename)
    with open(filename + '.svg', 'wb') as fp:
      fp.write(svgdata)
    with open(filename + '.json', 'w') as fp:
      fp.write(data)

    return {'status': 'ok', 'name': args.name, 'id': basename}


def json_representation(data, code, headers=None):
    resp = make_response(json.dumps(data), code)
    resp.headers.extend(headers or {})
    resp.headers.setdefault('Access-Control-Allow-Origin', '*')
    return resp


def make_api(app, url_prefix='/'):
  api = Api(app)
  api.representation('application/json')(json_representation)
  api.add_resource(HoudiniNodeshapeConverter, url_prefix)
  return api


def main():
  app = flask.Flask(__name__)
  app.config['ERROR_404_HELP'] = False
  make_api(app)
  app.run(debug=True)


if ('require' in globals() and require.main == module) or __name__ == '__main__':
  main()
