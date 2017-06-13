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

## Example Form

![](http://i.imgur.com/1znnsnh.png)

## Api

### GET `/`

__Parameters__

* `?shape_id=`: The ID of the shape to download the JSON file for. The shape
  ID is returned after converting an SVG file with the **POST `/`** API.

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
* `name`: The name that was specified via the `name` parameter. If the
  parameter was omitted, the name of the uploaded file will be here.
* `id`: The ID of the shape. Use the **GET `/`** API to download the JSON file.
