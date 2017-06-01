<p align="center"><img src="http://i.imgur.com/VWO2QFG.jpg"></p>
<h1 align="center"><a href="https://stuff.niklasrosenstein.com/houdini-nodeshape-converter">Houdini NodeShape Converter</a></h1>
<p align="center">Convert SVG paths to Houdini JSON nodeshapes.</p>

  [0]: https://stuff.niklasrosenstein.com/houdini-nodeshape-converter

## Creating a Houdini NodeShape

1. Use your favorite vector graphics application (eg. Affinity Designer, Adobe Illustrator, Inkscape)  
   *Note: That application must support SVG export that preserves layer names and
   absolute coordinates.*

2. Create your shape and make sure the layer names are correct (see image below).

   ![](https://image.ibb.co/kFW30v/2017_05_31_23_01_10_Affinity_Designer.png)

3. Save the file in SVG format (eg. in "for web" mode which reduces the
   complexity of the file and converts relative to absolute coordinates).

4. Go to the [Houdini Nodeshape Converter][0] website and paste the content
   of the exported SVG file and press "Convert". It will automatically download
   the generated JSON file.

5. Put the JSON file in your Houdini application folder under
   `houdini/config/NodeShapes` and restart Houdini. If you don't see the
   shape in the node editor, please [Report an Issue][1] and attach your
   input SVG and output JSON file.

[0]: https://stuff.niklasrosenstein.com/houdini-nodeshape-converter
[1]: https://github.com/NiklasRosenstein/houdini-nodeshape-converter/issues

## Deployment

- Make sure you specify a `SECRET_KEY` configuration value in the Flask app
