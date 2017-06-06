<h1 align="center">Houdini NodeShape Converter</h1>
<p align="center">Convert SVG to Houdini NodeShape JSON files.</p>

  [0]: https://stuff.niklasrosenstein.com/houdini-nodeshape-converter

A [Node.py] application that uses [Flask] and [Flask-RESTful] to provide
a simple API to convert SVG to Houdini NodeShape JSON files. It allows
cross-origin access by default. The API is described below.

  [Node.py]: https://nodepy.org
  [Flask]: http://flask.pocoo.org/
  [Flask-RESTful]: https://flask-restful.readthedocs.io/

There is also a command-line tool that can be installed via

    $ nppm install -g git+https://github.com/NiklasRosenstein/houdini-nodeshape-converter.git
    $ houdini-nodeshape-converter --help

To embedd the API in your flask Application, use

```python
import flask
import {make_api} from '@NiklasRosenstein/houdini-nodeshape-converter'

app = flask.Flask(__name__)
make_api(app, url_prefix='/houdini-nodeshape-converter/')
```

## Api

### POST `/`

__Parameters__

* `name`: The name of the created shape. This name will be contained in the
  resulting JSON object. If not specified, the file's name is used.
* `xres`: X resolution of the SVG image. If omitted, will be determined from
  the bounding box of all paths that are converted into the Houdini NodeShape.
* `yres`: See `xres`
* `file`: An SVG image file that must contain all elements necessary to
  generate a Houdini NodeShape.

__Returns__

* `status`: `"ok"`
* `shape`: A string formatted as JSON data of the generated Houdini
  NodeShape file.
* `name`: The name that was specified via the `name` parameter. If the
  parameter was omitted, the name of the uploaded file will be here.
* `id`: The shape will be saved to a storage location on the server for
  future extension where we may want to display the shapes that have
  already been created.
