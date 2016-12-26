import argparse
import os
import sys
import textwrap


VERSION = "1.0"
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
    parser.add_argument("-r", "--ir", help="Pathname of IR file",
        action="store", dest="ir_file", default=None, required=True)
    parser.add_argument("-g", "--gain", help="Gain multiplier applied to output (default: %(default)s)",
        action="store", dest="gain", type=float, default=1.0)
    parser.add_argument("-s", "--sr", help="Sample rate (default: %(default)s)",
        action="store", dest="sr", type=int, default=96000)
    parser.add_argument('-v', "--version", action='version', version='%(prog)s ' + VERSION)

    return parser.parse_args(argv)
    

def main(argv):
    args = parse_args(argv)

    csd_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), CSD_NAME)
    if not os.path.exists(csd_file):
        print "Can't find CSD file: %s" % csd_file
        return 1

    csound_cmd = 'csound -m0 -d --sample-rate=%s --ksmps=%s --omacro:INFILE="%s" --omacro:IRFILE="%s" --omacro:GAIN=%s -W -R -3 -o "%s" "%s"' %\
        (args.sr, 1, args.sound_file_in, args.ir_file, args.gain, args.sound_file_out, csd_file)

    print textwrap.dedent('''
    input file: %s
    gain adjustment: %s
    impulse response file: %s
    output file: %s
    
    Csound command: %s\n
    ''') % (args.sound_file_in, args.gain, args.ir_file, args.sound_file_out, csound_cmd)

    return os.system(csound_cmd)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

