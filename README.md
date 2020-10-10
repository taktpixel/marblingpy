# marblingpy

## Description

generate a randomized mathematical marbling image.

![logo.png](logo.png "logo.png")

## Usage

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

## Example

To operate "ink-drop" method 10 times.
```
$ marblingpy --save output.png --method I --width 256 --height 256 --count 10 --verbose
Current seed: 1602334135
drop circle (0/10) : (x, y, r) = (194, 224, 52)
drop circle (1/10) : (x, y, r) = (147, 165, 86)
drop circle (2/10) : (x, y, r) = (184, 9, 42)
drop circle (3/10) : (x, y, r) = (98, 245, 58)
drop circle (4/10) : (x, y, r) = (155, 26, 30)
drop circle (5/10) : (x, y, r) = (195, 95, 10)
drop circle (6/10) : (x, y, r) = (185, 37, 87)
drop circle (7/10) : (x, y, r) = (82, 215, 70)
drop circle (8/10) : (x, y, r) = (233, 123, 29)
drop circle (9/10) : (x, y, r) = (51, 186, 41)
```

To set initial image, and use "tine-line" method 3 times.
```
$ marblingpy --init output.png --save output.png --method T --width 256 --height 256 --count 3 --verbose
Current seed: 1602334273
tine line (0/3) : (x1, y1), (x2, y2), shift, sharpness = (202, 44), (62, 177), 54, 27
tine line (1/3) : (x1, y1), (x2, y2), shift, sharpness = (23, 245), (76, 234), 146, 28
tine line (2/3) : (x1, y1), (x2, y2), shift, sharpness = (25, 23), (12, 127), 66, 7
```

![example.png](example.png "example.png")


## System environment

* Python >=3.7
* pip 20.2.3
* opencv-python 4.4.0.44

## Installation

## pip

```bash
pip install git+https://github.com/taktpixel/marblingpy
```

### for development
```
git clone https://github.com/taktpixel/marblingpy.git
cd marblingpy
pip install -e .
```

# Note

## Authors

 - [Shinobu Yokoyama](https://github.com/cohom) <cohomolg@gmail.com>
 - [Teppei Tamaki](https://github.com/leetmikeal/)

## Licensing

marblingpy is dual-licensed; You may use this software under either LGPLv3 or our commercial (proprietary) license. See the LICENSE files for details.

 - [Commercial](LICENSE.Commercial)
 - [Non-commercial LGPLv3](LICENSE.LGPLv3)

## References

1. Lu, Shufang, Aubrey Jaffer, Xiaogang Jin, Hanli Zhao, and Xiaoyang Mao. "Mathematical marbling." IEEE computer graphics and applications 32, no. 6 (2011): 26-35.
