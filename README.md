<p align="center"><img src="http://i.imgur.com/VWO2QFG.jpg"></p>
<h1 align="center">Houdini Nodeshape Converter</h1>
<p align="center">Convert SVG paths to Houdini JSON nodeshapes.</p>

## Installation

Via Node.py and NPPM:

    $ nppm install -g git+https://github.com/NiklasRosenstein/houdini-nodeshape-converter.git

Via Pip:

    $ pip install git+https://github.com/NiklasRosenstein/houdini-nodeshape-converter.git

## Synopsis

```
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
```

## Instructions

Export an SVG file with your favorite vector graphics application. In the
example below, I use **Affinity Designer**. Create paths with the following
names (the coloring is optional):

<table>
  <tr>
    <td>
      <img src="https://image.ibb.co/kFW30v/2017_05_31_23_01_10_Affinity_Designer.png">
    </td>
    <td>
      <ul>
        <li>outputs</li>
        <li>inputs</li>
        <li>icon [rectangle]</li>
        <li>flag0</li>
        <li>flag1</li>
        <li>flag2</li>
        <li>flag3</li>
        <li>outline</li>
      </ul>
    </td>
  </tr>
</table>

Then export the vector graphics as SVG file. It is important that the SVG
path preserves the path names as XML `id` attributes. Also, all path
coordinates should be absolute, that is why I chose "print" as the export
mode, since "export" can generate paths inside a transform node.

<p align="center"><img src="http://i.imgur.com/clRCQ84.png"></p>

Pass this SVG file into `houdini-nodeshape-converter`. You can pipe the
output into a JSON file and copy that into your Houdini Nodeshape folder.

    $ houdini-nodeshape-converter myshape.svg
    {
      "icon": [
        ...

## Todo

- Clever way to determine angle of inputs and outputs (currently set to 0)
