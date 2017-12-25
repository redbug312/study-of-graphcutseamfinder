# Study of GraphCutSeamFinder

This is the demo part of team 11 presentation, on the course Image Processing (National Taiwan University, 2017 Fall).
> [slides](http://slides.com/redbug312/graphcutseamfinder)

- `main.py` builds a primitive `GraphCutSeamFinder` in Python. External libraries including [OpenCV](https://opencv.org/), [Numpy](http://www.numpy.org/), [PyMaxflow](https://github.com/pmneila/PyMaxflow) are needed.
- `opencv/main.cpp` shows how to pass parameters to `GraphCutSeamFinder` function of OpenCV. Noted that the result sucks.

## Credits
- [**Graphcut Textures: Image and Video Synthesis Using Graph Cuts**](https://www.cc.gatech.edu/cpl/projects/graphcuttextures): the referenced paper of `GraphCutSeamFinder()`.
- [OpenCV](https://opencv.org/), the open source computer vision library.
- [Numpy](http://www.numpy.org/), the fundamental package for scientific computing with Python.
- [PyMaxflow](https://github.com/pmneila/PyMaxflow), Python library for creating flow networks and computing the maxflow/mincut
