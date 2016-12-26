csound-convolver
================

Convolver tool, applies an impulse respone (IR) file to a sound file.

    usage: convolve.py [-h] -i SOUND_FILE_IN -o SOUND_FILE_OUT -r IR_FILE
                       [-g GAIN] [-s SR] [-v]

    Convolve a stereo audio file with a stereo IR

    optional arguments:
      -h, --help            show this help message and exit
      -i SOUND_FILE_IN, --in SOUND_FILE_IN
                            Pathname of input sound file
      -o SOUND_FILE_OUT, --out SOUND_FILE_OUT
                            Pathname of output sound file
      -r IR_FILE, --ir IR_FILE
                            Pathname of IR file
      -g GAIN, --gain GAIN  Gain multiplier applied to output (default: 1.0)
      -s SR, --sr SR        Sample rate (default: 96000)
      -v, --version         show program's version number and exit

Where:
- SOUND_FILE_IN is the name of the sound file to be convolved (assumed to be 96K 24-bit WAV)
- IR_FILE is a sound file consisting of an impulse response recording (WAV file assumed, should be 96K or 48K)
- GAIN is the amount by which the gain of the input file should be scaled (numeric, 0.1 means 10%)
- SOUND_FILE_OUT is the name of the output sound file (96k 24-bit WAV)

Notes:
- You must have Csound installed and on the path.
- The IR input file should 96K or an even divisor of 96K (e.g., 48K).
- The GAIN_ADJUST parameter is used to reduce the level of the input file to avoid clipping; depending on the IR, convolution can add a lot of gain.

Convolve.py requires the Csound script "convolver.csd", which must be located in the same directory as "convolve.py".

For more information on Csound, see http://www.csounds.com.

A good source for free IR files is http://www.openairlib.net.

Written by Dave Seidel, 2016.

Copyright (c) Dave Seidel, 2016, some rights reserved. The contents of this repository are available under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported license (http://creativecommons.org/licenses/by-nc-sa/3.0/). You are welcome to fork this project as long as you abide by the licensing terms.

