#!/usr/bin/env bash
#===============================================================================
# Csound CV Tools
# Dave Seidel
# v1.0 2020-12-21
#===============================================================================

function usage {
    echo "Usage: tuner [-f FREQ] [-n NOTE] [-t TUNING] [-c CV_OUTPUT_CHANNEL]" >&2
    exit 1
}

# defaults
_FREQ=0
_NOTE=69
_TUNING=1
_CHN=7

while getopts ":hf:n:t:c:" opt; do
    case $opt in
        h)  
            usage
            ;;
        f)
            _FREQ=$OPTARG
            ;;
        n)
            _NOTE=$OPTARG
            ;;
        t)
            _TUNING=$OPTARG
            ;;
        c)
            _CHN=$OPTARG
            ;;
        \?)
            echo "Invalid option -$OPTARG" >&2
            usage
            ;;
    esac
done

csound --omacro:FREQ=$_FREQ --omacro:NOTE=$_NOTE --omacro:TUNING=$_TUNING --omacro:CHN=$_CHN tuner.csd
exit $?
