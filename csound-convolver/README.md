# csound-convolver

Convolver tool, applies an impulse response (IR) file to a stereo sound file.

## Installation

The tool consists of two files, convolve.py and convolver.csd; these files may be located wherever you like as long as they are both in the same directory. On a Linux system, I recommend:

1. make convolve.py executable: ```chmod +x convolve.py```
2. make a link to convolve.py called "convolve" and put it in a directory that's on the path, e.g. ```ln -s convolve.py ~/bin/convolve```

If you follow these steps, you should be able to execute the "convolve" command from any directory

## Usage

    usage: convolve.py [-h] -i SOUND_FILE_IN -o SOUND_FILE_OUT -r IR_FILE
                       [-g GAIN] [-s SR] [-v]

    Convolve a stereo audio file with a stereo IR

    optional arguments:
      -h, --help            show this help message and exit
      -i SOUND_FILE_IN, --in SOUND_FILE_IN
                            Pathname of input sound file
      -o SOUND_FILE_OUT, --out SOUND_FILE_OUT
                            Pathname of output sound file
      -1 IR_FILE1, --ir1 IR_FILE1
                            Pathname of IR file 1
      -2 IR_FILE2, --ir2 IR_FILE2
                            Pathname of IR file 2 (optional)
      -g GAIN, --gain GAIN  Gain multiplier applied to output (default: 1.0)
      -s SR, --sr SR        Sample rate (default: 48000)
      -v, --version         show program's version number and exit

Where:
- SOUND\_FILE\_IN is the name of the sound file to be convolved (assumed to be 48K/24-bit WAV)
- IR\_FILE1 is a sound file consisting of an impulse response recording (48K WAV file assumed), this will be applied to the left channel of the input file
- IR\_FILE2 is a second IR file, to be applied to the right channel of the input file; if not specified, IR\_FILE1 will be used
- GAIN is the amount by which the gain of the input file should be scaled (numeric, 0.1 means 10%)
- SOUND\_FILE\_OUT is the name of the output sound file (usually 48k/24-bit WAV)

Notes:
- You must have Csound installed and on the path.
- The IR input file should 48K.
- The GAIN parameter is used to reduce the level of the input file to avoid clipping; depending on the IR, convolution can add a lot of gain. I often find myself using a value of 0.1 to avoid clipping.
- The output soundfile is 100% wet, based on the assumption that you will take care of mixing it together with the original (dry) track.
- CAVEAT: the convolution always involves a very slight delay in the output file relative to the original file due to latency, usually on the order of a few hundredths of a second (e.g., 0.021354 seconds). Thus, when mixing the dry and wet tracks you should remove that amount from the beginning of the wet track before combining. The amount of latency is printed aspart of the output of the script, e.g. ```Convolving with a latency of 0.021354 seconds```.

## Prerequisites

Convolve.py requires the Csound script "convolver.csd", which must be located in the same directory as "convolve.py".

## Changelog

* v1.0
  * Initial version
* v1.1
  * Switch to Python 3
  * Convolve left and right channels of input file separately, then combine for output
  * Change ```-r/--ir``` option to ```-1/--ir1```, add ```-2/--ir2```
  * Default sample rate is now 48K

## Other info

For more information on Csound, see http://www.csounds.com.

~~A good source for free IR files is http://www.openairlib.net.~~ Sadly, this site appears to be offline.

Written by Dave Seidel, 2016 (revised 2019).

Copyright (c) Dave Seidel, 2016, 2019, some rights reserved. The contents of this repository are available under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported license (http://creativecommons.org/licenses/by-nc-sa/3.0/). You are welcome to fork this project as long as you abide by the licensing terms.
