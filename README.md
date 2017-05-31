<p align="center"><img src="http://i.imgur.com/3mRpJay.jpg"></p>
<h1 align="center">Houdini Nodeshape Converter</h1>
<p align="center">Convert SVG paths to Houdini JSON nodeshapes.</p>

## Installation

    $ nppm install -g git+https://github.com/NiklasRosenstein/houdini-nodeshape-converter.git
    $ houdini-nodeshape-converter

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
      <img src="http://i.imgur.com/2zzr1ts.png">
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

![](http://i.imgur.com/clRCQ84.png)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100%" height="100%" viewBox="0 0 128 128" version="1.1" xml:space="preserve" style="fill-rule:evenodd;clip-rule:evenodd;stroke-linecap:round;stroke-linejoin:round;stroke-miterlimit:1.5;">
<path id="outline" d="M64,20.93c3.457,-7.902 11.347,-13.43 20.518,-13.43c12.354,0 22.384,10.03 22.384,22.384c0,12.353 -10.03,22.383 -22.384,22.383l0,47.877c0,11.324 -9.194,20.518 -20.518,20.518c-11.324,0 -20.518,-9.194 -20.518,-20.518l0,-47.877c-12.354,0 -22.384,-10.029 -22.384,-22.383c0,-12.354 10.03,-22.384 22.384,-22.384c9.171,0 17.061,5.528 20.518,13.43Z" style="fill:#ebebeb;"/>
<path id="flag3" d="M64,21.623c3.237,-8.264 11.285,-14.123 20.691,-14.123c12.258,0 22.211,9.953 22.211,22.212c0,12.258 -9.953,22.211 -22.211,22.211l0,-7.482c8.129,0 14.729,-6.6 14.729,-14.729c0,-8.13 -6.6,-14.73 -14.729,-14.73c-8.13,0 -14.73,6.6 -14.73,14.73l-5.961,0l0,-8.089Z" style="fill:#00a5ff;"/>
<path id="flag2" d="M78.144,100.063c-0.05,7.764 -6.368,14.052 -14.144,14.052l0,6.547c11.419,0 20.691,-9.271 20.691,-20.691l-6.547,0l0,0.092Z" style="fill:#ffa100;"/>
<path id="flag1" d="M49.856,100.063c0.05,7.764 6.368,14.052 14.144,14.052l0,6.547c-11.419,0 -20.691,-9.271 -20.691,-20.691l6.547,0l0,0.092" style="fill:#ce00ff;"/>
<path id="flag0" d="M64,29.712l-5.961,0c0,-8.13 -6.6,-14.73 -14.73,-14.73c-8.129,0 -14.729,6.6 -14.729,14.73c0,8.129 6.6,14.729 14.729,14.729l0,7.482c-12.258,0 -22.211,-9.953 -22.211,-22.211c0,-12.259 9.953,-22.212 22.211,-22.212c9.406,0 17.454,5.859 20.691,14.123l0,8.089Z" style="fill:#79d584;"/>
<rect id="icon" x="49.309" y="53.8" width="29.381" height="28.777" style="fill:#b3d2d3;"/>
<path id="inputs" d="M22.909,6.475c0,0 13.601,-3.975 41.091,-3.975c27.49,0 41.091,3.975 41.091,3.975" style="fill:none;stroke:#000;stroke-width:1px;"/>
<path id="outputs" d="M40.504,99.971c0,0 0.756,23.029 23.496,23.029c22.74,0 23.496,-23.029 23.496,-23.029" style="fill:none;stroke:#000;stroke-width:1px;"/>
</svg>
```

Pass this SVG file into `houdini-nodeshape-converter`. You can pipe the
output into a JSON file and copy that into your Houdini Nodeshape folder.

    $ houdini-nodeshape-converter myshape.svg
    {
      "icon": [
        ...

## Todo

- Clever way to determine angle of inputs and outputs (currently set to 0)
