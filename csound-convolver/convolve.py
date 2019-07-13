#!/usr/bin/env python3

import argparse
import os
import sys
import textwrap


VERSION = "1.1"
CSD_NAME = "convolver.csd"


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Convolve a stereo audio file with a stereo IR",
        prog="convolve.py"
    )

    parser.add_argument("-i", "--in", help="Pathname of input sound file",
        action="store", dest="sound_file_in", default=None, required=True)
    parser.add_argument("-o", "--out", help="Pathname of output sound file",
        action="store", dest="sound_file_out", default=None, required=True)
    parser.add_argument("-1", "--ir1", help="Pathname of IR file 1",
        action="store", dest="ir_file1", default=None, required=True)
    parser.add_argument("-2", "--ir2", help="Pathname of IR file 2 (optional)",
        action="store", dest="ir_file2", default=None)
    parser.add_argument("-g", "--gain", help="Gain multiplier applied to output (default: %(default)s)",
        action="store", dest="gain", type=float, default=1.0)
    parser.add_argument("-s", "--sr", help="Sample rate (default: %(default)s)",
        action="store", dest="sr", type=int, default=48000)
    parser.add_argument('-v', "--version", action='version', version='%(prog)s ' + VERSION)

    return parser.parse_args(argv)


def main(argv):
    args = parse_args(argv)

    csd_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), CSD_NAME)
    if not os.path.exists(csd_file):
        print("Can't find CSD file: {}".format(csd_file))
        return 1

    ir_file1 = args.ir_file1
    if hasattr(args, "ir_file2"):
        ir_file2 = ir_file1
    else:
        ir_file2 = args.ir_file2

    csound_cmd = 'csound -m0 -d --sample-rate={} --ksmps={} --omacro:INFILE="{}" --omacro:IRFILE1="{}" --omacro:IRFILE2="{}" --omacro:GAIN={} -W -3 -o "{}" "{}"'\
        .format(args.sr, 1, args.sound_file_in, ir_file1, ir_file2, args.gain, args.sound_file_out, csd_file)

    print(textwrap.dedent('''
    input file: {}
    gain adjustment: {}
    impulse response file 1: {}
    impulse response file 2: {}
    output file: {}

    Csound command: {}\n
    ''').format(args.sound_file_in, args.gain, args.ir_file1, args.ir_file2, args.sound_file_out, csound_cmd))

    return os.system(csound_cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
