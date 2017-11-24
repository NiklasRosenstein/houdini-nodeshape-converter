import flask
import nodepy

app = flask.Flask('houdini-nodeshape-converter')
hnc = nodepy.require('@NiklasRosenstein/houdini-nodeshape-converter')
hnc.make_api(app)

