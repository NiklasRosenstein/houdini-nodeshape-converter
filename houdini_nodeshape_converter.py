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

import click
import itertools
import json
import numpy as np
import os
import svgpathtools
import sys
import xml.dom.minidom as minidom

from xml.parsers.expat import ExpatError


def cboundingbox(points):
  p = next(points)
  xmin, xmax, ymin, ymax = p.real, p.real, p.imag, p.imag
  for p in points:
    if p.real < xmin: xmin = p.real
    if p.real > xmax: xmax = p.real
    if p.imag < ymin: ymin = p.imag
    if p.imag > ymax: ymax = p.imag
  return xmin, xmax, ymin, ymax


def ctuples(points, third=None):
  points = [complex(p.real, 1.0 - p.imag) for p in points]
  if third is None:
    return [(p.real, p.imag) for p in points]
  else:
    return [(p.real, p.imag, third) for p in points]


def get_icon_path(rect):
  x, y, w, h = map(float, [rect.getAttribute(n) for n in 'x y width height'.split()])
  return [complex(x, y+h), complex(x+w, y)]


def convert(fp, inputdim=None, name=None, cubic_samples=10):
  doc = minidom.parse(fp)
  paths = doc.getElementsByTagName('path')
  rects = doc.getElementsByTagName('rect')
  if len(paths) != 7:
    ctx.fail('expected 7 <path/>, got {}'.format(len(paths)))
  if len(rects) != 1:
    ctx.fail('expected 1 <rect/>, got {}'.format(len(rects)))

  # Sample all paths.
  results = {}
  for node in paths:
    path = svgpathtools.parse_path(node.getAttribute('d'))
    points = []
    for comp in path:
      # TODO: Skip duplicate start/end points.
      if isinstance(comp, svgpathtools.Line):
        points.append(comp.start)
        points.append(comp.end)
      else:
        for x in np.linspace(0, 1, cubic_samples):
          points.append(comp.point(x))
    results[node.getAttribute('id')] = points

  # Convert the icon rectangle to a line for houdini.
  results['icon'] = get_icon_path(rects[0])

  # If no input dimension is specified, determine the bounding box
  # of the whole shape.
  if not inputdim:
    bbox = cboundingbox(itertools.chain(*results.values()))
    inputdim = (bbox[1] - bbox[0], bbox[3] - bbox[2])
    offset = complex(bbox[0], bbox[2])
  else:
    offset = 0+0j

  # Determine the factor by which the paths need to be scaled in order
  # to fit on a 1x1 tile.
  scalar = 1.0 / (inputdim[0] if inputdim[0] > inputdim[1] else inputdim[1])

  # Transform all to fit on a 1x1 tile.
  for path in results.values():
    path[:] = [(p - offset) * scalar for p in path]

  # Generate the output JSON.
  data = {
    'name': name,
    'flags': {
      '0': { 'outline': ctuples(results['flag0']) },
      '1': { 'outline': ctuples(results['flag1']) },
      '2': { 'outline': ctuples(results['flag2']) },
      '3': { 'outline': ctuples(results['flag3']) }
    },
    'outline': ctuples(results['outline']),
    'inputs': ctuples(results['inputs'], 0.0),
    'outputs': ctuples(results['outputs'], 0.0),
    'icon': ctuples(results['icon'])
  }
  return json.dumps(data, indent=2, sort_keys=True)


@click.command()
@click.argument('svgfile')
@click.argument('inputdim', required=False)
@click.option('-n', '--name',
    help='Name of the shape in the JSON file. Default: SVGFILE basename')
@click.option('-s', '--cubic-samples', type=int, default=10,
    help='Number of samples for cubic curves. Default: 10')
@click.pass_context
def main(ctx, svgfile, inputdim, name, cubic_samples):
  """
  Houdini Nodeshape Converter -- Convert SVG paths to Houdini JSON nodeshapes.

  With SVGFILE you must specify an SVG file that contains the following
  elements from which a Houdini Nodeshape can be generated:

  \b
  * <path id="outline"/>
  * <path id="outputs"/>
  * <path id="inputs"/>
  * <path id="flag0"/>
  * <path id="flag1"/>
  * <path id="flag2"/>
  * <path id="flag3"/>
  * <rect id="icon"/>

  The INPUTDIM must be of the format `WxH` where W and H specify the width
  and height of the input SVG file. If the parameter is omitted, the bounding
  box of all paths in the SVG file is used instead to normalize the shape
  size to 0..1 range.

  Outputs the JSON Nodeshape to stdout.
  """

  if not name:
    name = os.path.splitext(os.path.basename(svgfile))[0]

  if inputdim:
    try:
      inputdim = map(int, inputdim.split('x'))
      if len(inputdim) != 2:
        raise ValueError
    except (IndexError, ValueError):
      ctx.fail('invalid INPUTDIM: {!r}'.format(inputdim))

  with open(svgfile) as fp:
    print(convert(fp, inputdim, name, cubic_samples))


if ('require' in globals() and require.main == module) or __name__ == '__main__':
  main()
