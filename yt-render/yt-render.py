#
# Dave Seidel, December 2016
# http://mysterybear.net
# http://github.com/music-tools/yt-render
#
# based on a script by Mike Gogins (http://www.michael-gogins.com/)
#

# YouTube accepts MOV, MP4 (MPEG4), AVI, WMV, FLV, 3GP, MPEGPS, WebM
# To use FFmpeg see https://bbs.archlinux.org/viewtopic.php?id=168433 and https://www.virag.si/2015/06/encoding-videos-for-youtube-with-ffmpeg/
# ffmpeg tags are documented here: http://jonhall.info/how_to/create_id3_tags_using_ffmpeg

# example of expected metadata format (section name "__track__" is mandatory, as are all of the fields)
'''
[__track__]
soundfile=hexany_catalog_part1_master.wav
album=Hexany Permutations
title=Part 1
year=2016
track=1
artist=Dave Seidel
composer=Dave Seidel
genre=Electroacoustic
publisher=Mysterybear Music, ASCAP
copyright=Copyright (c) 2016 by Dave Seidel, some rights reserved. Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0).
'''

import argparse
import datetime
import os
import os.path
import sys
import textwrap

import ConfigParser


VERSION="1.0"


def gen_spectrogram(meta, draw_raw_graph=False):
    basename = os.path.basename(meta["soundfile"])

    sox_spectrogram_command = 'sox %s' % ' '.join((
        '-S "%s"' % meta["soundfile"],
        '-n spectrogram',
        '-r' if draw_raw_graph else '',
        '-o "%s.png"' % basename,
        '-t "%s"' % "wav",
        '-c "%s"' % "%s Published by %s" % (meta["copyright"], meta["publisher"])
    ))

    return os.system(sox_spectrogram_command)


def gen_video(meta):
    cwd = os.getcwd()
    basename = os.path.basename(meta["soundfile"])

    # ffmpeg does not support the "publisher" field, we so append that datum to the copyright field
    mp4_metadata = ' '.join((
        '-metadata title="%s: %s"'                  % (meta["album"], meta["title"]),
        '-metadata album="%s"'                      % meta["album"],
        '-metadata date="%s"'                       % meta["year"],
        '-metadata track="%s"'                      % meta["track"],
        '-metadata genre="%s"'                      % meta["genre"],
        '-metadata copyright="%s Published by %s"'  % (meta["copyright"], meta["publisher"]),
        '-metadata composer="%s"'                   % meta["composer"],
        '-metadata artist="%s"'                     % meta["artist"]
    ))

    mp4_command = 'ffmpeg %s' % ' '.join((
        '-loglevel info',
        '-hide_banner',
        '-y',
        '-loop 1',
        '-framerate 2',
        '-i "%s"' % os.path.join(cwd, "%s.png" % basename),
        '-i "%s"' % os.path.join(cwd, meta["soundfile"]),
        '-c:v libx264',
        '-preset medium',
        '-tune stillimage',
        '-crf 18',
        '-codec:a aac',
        '-strict -2',
        '-b:a 384k',
        '-r:a 48000',
        '-shortest',
        '-pix_fmt yuv420p',
        '-vf "scale=trunc(iw/2)*2:trunc(ih/2)*2"',
        '-timestamp now',
        '%s' % mp4_metadata,
        '"%s"' % os.path.join(cwd, "%s.mp4" % basename)
    ))

    return os.system(mp4_command)
    
    
def print_blank_metadata():
    print textwrap.dedent('''\
        # all fields required
        [__track__]
        soundfile=
        album=
        title=
        year=
        track=
        artist=
        composer=
        genre=
        publisher=
        copyright=
        ''')

def read_metadata(metadata_file):
    config = ConfigParser.RawConfigParser()
    config.read(metadata_file)

    # convert list of tuples to dict
    return dict(config.items("__track__"))


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Build MP4 video, with static spectrogram, from WAV file.",
        prog="yt-render.py"
    )

    parser.add_argument("-m", help="Pathname of metadata file",
        action="store", dest="metadata_file", default=None)
    parser.add_argument("-r", help="Draw spectrograph without axes/legends",
        action="store_true", dest="draw_raw_graph", default=False)
    parser.add_argument("-p", help="Print a blank metadata form to the screen and exit",
        action="store_true", dest="print_blank_metadata", default=False)
    parser.add_argument('-v', action='version', version='%(prog)s ' + VERSION)

    return parser.parse_args(argv)
    

def main(argv):
    args = parse_args(argv)
    
    if args.print_blank_metadata:
        print_blank_metadata()
        return 0

    if not args.metadata_file:
        print "No metadata file, nothing to do"
        return 1

    meta = read_metadata(args.metadata_file)
    
    print "[[[ Generating spectrogram... ]]]"
    gen_spectrogram(meta, args.draw_raw_graph)

    print "[[[ Generating video... ]]]"
    gen_video(meta)
    
    print "[[[ Done! ]]]"
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

