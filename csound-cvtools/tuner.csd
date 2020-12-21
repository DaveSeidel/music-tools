;===============================================================================
; Csound CV Tools
; Dave Seidel
; v1.0 2020-12-21
;===============================================================================

<CsoundSynthesizer>
<CsOptions>
-d -m4 -+rtaudio=alsa --format=long -odac:hw:1,0
</CsOptions>

<CsInstruments>

sr = 44100
ksmps = 1
nchnls =  16
; nchnls_i = 8
0dbfs = 1.0

#include "cvtools.orc"

#ifndef FREQ
#define FREQ #0#
#endif

#ifndef TUNING
#define TUNING #1#
#endif

#ifndef NOTE
#define NOTE #69#
#endif

#ifndef CHN
#define CHN #7#
#endif

; standard 12-TET tuning
gi_12tet = ftgen(1, 0, 128, -51,
                 12, 2, cpsoct(8), 60,
                 1, 2^(1/12), 2^(2/12), 2^(3/12), 2^(4/12), 2^(5/12),
                 2^(6/12), 2^(7/12), 2^(8/12), 2^(9/12), 2^(10/12), 2^(11/12), 2^(12/12))

; Grady Centaur tuning (just intonation)
gi_cent = ftgen(2, 0, 128, -51,
                12, 2, cpsoct(8), 60,
                1.0, 21/20, 9/8, 7/6, 5/4, 4/3, 7/5, 3/2, 14/9, 5/3, 7/4, 15/8, 2.0)

instr Tuner
    idur = p3

    ifreq = $FREQ
    ituning = $TUNING
    inote = $NOTE
    ichn = $CHN

    if ituning == gi_12tet then
        Stuning = "12TET"
    elseif ituning == gi_cent then
        Stuning = "Centaur"
    else
        prints("*** Error: unknown tuning %d, exiting ***\n", ituning)
        exitnow()
    endif

    if ifreq > 0 then
        icps = ifreq
    else
        icps = table(inote, ituning)
    endif
    outch(1, vco2(ampdb(-4), icps))

    ipch = cvt_f2p(icps)
    cvt_pitch(ichn, idur, ipch)

    prints("\n=====\n")
    if ifreq > 0 then
        prints("Freq:%f pv:%f\n", icps, ipch)
    else
        prints("Tuning=%s(%d) Note=%d f:%f pv:%f\n",
            Stuning, ituning, inote, icps, ipch)
    endif
    prints("CV channel:%d\n", ichn)
    prints("=====\n\n")
endin

</CsInstruments>
<CsScore>
i "Tuner" 0 1440
e
</CsScore>
</CsoundSynthesizer>