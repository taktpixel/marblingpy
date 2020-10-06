marblingpy
==========

description
-----------

generate a randomized mathematical marbling image.

![logo.png](logo.png "logo.png")

usage
-----

```bash
marblingpy [-h] [--init INIT] [--save FILE] -m M [-W W] [-H H] [--seed SEED] [--count C]
  -h, --help                     show this help message and exit
  --version                      show program\'s version number and exit
  --init INIT                    if given, the distortion will start based from the image (png) file
  --save FILE                    write generating image to FILE
  -m M, --method M               the tool function that applies to the image; I=ink-drop, T=tine-line.
  -W W, --width W                the width in integer of generating image file (gif)
  -H H, --height H               the height in integer of generating image file (gif)
  --seed SEED                    input of an unsigned integer 0 or 2^32-1 to the algorithm that generates pseudo-random numbers throughout the program. the same seed produces the same result.
  --interpolation INTERPOLATION  pixel filling interpolation type
  --count C                      the total number of times that tool functions shall be applied to render an image
  -v, --verbose                  show verbose message
```

system environment
------------------
* Python >=3.7
* pip 20.2.3
* opencv-python 4.4.0.44

installation
-------------

**pip**
```bash
pip install --upgrade pip
```

**opencv-python**
```bash
pip install opencv-python
```

Licensing
---------

marblingpy is dual-licensed; You may use this software under either LGPLv3 or our commercial (proprietary) license. See the LICENSE files for details.
