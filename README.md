marblingpy
===================

description
-----------

generate a randomized mathematical marbling image.

![logo.png](logo.png "logo.png")

usage
-----

```bash
gen_marbling.py [-h] [--save FILE] [--width W] [--height H] [--count C]
  --save FILE  write generating image to FILE
  --width W    the width in integer of generating image file (gif)
  --height H   the height in integer of generating image file (gif)
  --count C    the total number of times that tool functions shall be applied to render an image
```

system environment
------------------
* Python 2.7.16
* pip 20.2.3
* opencv-python 4.2.0.32

installation
-------------

**pip**
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# may need adding `/.local/bin` to the PATH environment variable
pip install --upgrade pip
```

**opencv-python**
```bash
pip install opencv-python==4.2.0.32
```
The version `4.2.0.32` is not arbitrary of `opencv-python` variant, at least in python 2.7.x environment. Consult the reference below for more detail:

> Python 2.7 is not supported anymore in opencv-python-4.3.0.38 the support was dropped since 4.3.0.36, see this issue.
>The workaround I found was to install opencv-python version 4.2.0.32 (which is the latest supported for Python 2.7, see this for all releases) like this:

ref. [installing-opencv-via-pip-virtual-environment](https://stackoverflow.com/questions/63346648/python-2-7-installing-opencv-via-pip-virtual-environment).
