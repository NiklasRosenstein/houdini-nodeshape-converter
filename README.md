## Houdini NodeShape Converter

A small [Node.py] + [Flask] application that provides a simple REST-Api to
convert SVG files to Houdini NodeShape JSON files. To allow using the Api
from JavaScript in the browser, it allows cross-origin requests by default.

An instance of this Api is deployed on Azure under http://houdini-nodeshape-converter.herokuapp.com/.  
This form can be found at https://www.niklasrosenstein.com/post/2017-06-13-houdini-nodeshape-converter/.

  [Node.py]: https://nodepy.org
  [Flask]: http://flask.pocoo.org/
  [Flask-RESTful]: https://flask-restful.readthedocs.io/

![](https://i.imgur.com/1znnsnh.png)

## REST-Api

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

## Command-line Tool

    $ nodepy-pm install git+https://github.com/NiklasRosenstein/houdini-nodeshape-converter.git --global
    $ houdini-nodeshape-converter --help
    Usage: houdini-nodeshape-converter [OPTIONS] SVGFILE [INPUTDIM]

      Houdini Nodeshape Converter -- Convert SVG paths to Houdini JSON
      nodeshapes.

      With SVGFILE you must specify an SVG file that contains the following
      elements from which a Houdini Nodeshape can be generated:

      * <path id="outline"/>
      * <path id="outputs"/>
      * <path id="inputs"/>
      * <path id="flag0"/>
      * <path id="flag1"/>
      * <path id="flag2"/>
      * <path id="flag3"/>
      * <rect id="icon"/>

      The INPUTDIM must be of the format `WxH` where W and H specify the width
      and height of the input SVG file. If the parameter is omitted, the
      bounding box of all paths in the SVG file is used instead to normalize the
      shape size to 0..1 range.

      Outputs the JSON Nodeshape to stdout.

    Options:
      -n, --name TEXT              Name of the shape in the JSON file. Default:
                                  SVGFILE basename
      -s, --cubic-samples INTEGER  Number of samples for cubic curves. Default: 10
      --help                       Show this message and exit.

## Flask Blueprint

To embedd the REST-Api into your existing Flask application:

```python
import flask
import {make_api} from '@NiklasRosenstein/houdini-nodeshape-converter'

app = flask.Flask(__name__)
make_api(app, url_prefix='/houdini-nodeshape-converter/')
```
