# Gravity Fringes repository

Package to read webcam input data and perform real time visualizations to display gravity fringes and other possible projections for the exhibit prototype of the scicommhack at CERN (13-15 Nov. 2020).

## What the package can do
At the moment, it converts the image colour space to gray scale and it applies a LUT to the webcam or a video. The LUT converts the highlights into shades of red.

## How to do that
Just execute the main file to use the default webcam of your machine:

`python3 gravityfringes.py`.

To leave the program press the Esc key.

To specify the threshold on the gray scale above which the red shades are applied, use the option `-t` followed by a number between 0 (black, the whole picture is turned to shades of red) and 255 (white, only pure white is turned into pure red):

`python3 gravityfringes.py -t=180`.

The default threshold is 100.

To read from a different webcam, you can specify its channel `n` in your machine with the `-w` option:

`python3 gravityfringes.py -w=n`.

To read from a video on your machine, you can specify its location with the `-v` option:

`python3 gravityfringes.py -v=path-to-my-film`.

## Requirements

Any Python3 version should suffice. It requires the numpy and opencv packages.

At the moment of writing, the package runs on a machine with:
- Python 3.8.5
- numpy 1.18.4
- OpenCV 4.2.0
