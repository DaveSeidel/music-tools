;===============================================================================
; Csound CV Tools
; Dave Seidel, 11/29/2020 (initial release)
;===============================================================================

<CsoundSynthesizer>
<CsOptions>
; ES-8
--format=long -odac:hw:1,0 -m4
</CsOptions>

<CsInstruments>

sr = 96000
ksmps = 32
nchnls =  16
; nchnls_i = 8
0dbfs = 1.0

#include "cvtools.orc"

opcode timer, 0, 0
    prints("%d: <%f>\n", p1, times())
endop

instr Trigger_Demo
    ichn = p4
    timer()
    cvt_trigger(ichn)
endin

instr Gate_Open_Demo
    ichn = p4
    igate = p5
    ktrig init 1

    timer()
    cvt_gate_open(ichn, igate)
    ktrig = 0
endin

instr Gate_Close_Demo
    igate = p4
    ktrig init 1

    timer()
    cvt_gate_close(igate)
    ktrig = 0
endin

instr Ramp_Demo
    ichn = p4
    idur = p5
    ibeg = p6
    iend = p7

    timer()
    cvt_ramp(ichn, idur, ibeg, iend)
endin

instr AR_Demo_1
    ichn  = p4
    idur  = p5

    ibeg  = p6
    imid  = p7
    iend  = p8

    timer()
    cvt_ar_env_eq(ichn, idur, ibeg, imid, iend)
endin

instr AR_Demo_2
    ichn  = p4
    idur  = p5

    ibeg  = p6
    idur1 = p7
    
    imid  = p8
    
    iend  = p9
    idur2 = p10

    timer()
    cvt_ar_env(ichn, idur, ibeg, idur1, imid, iend, idur2)
endin

instr ASR_Demo
    ichn  = p4
    idur  = p5

    ibeg  = p6
    idur1 = p7
    
    imid  = p8
    idur2 = p9
    
    idur3 = p10
    iend  = p11

    timer()
    cvt_asr_env(ichn, idur, ibeg, idur1, imid, idur2, idur3, iend)
endin

instr LFO_Demo_1
    ichn = p4
    kamp = p5
    kcps = p6
    itype = p7

    timer()
    cvt_lfo(ichn, kamp, kcps, itype)
endin

instr LFO_Demo_2
    ichn = p4
    kamp = p5
    kcps = p6
    itype = p7

    timer()
    cvt_lfo_uni(ichn, kamp, kcps, itype)
endin

</CsInstruments>
<CsScore>

i "Ramp_Demo"         0  1      2  5  0 0.5
i "Ramp_Demo"        10  1      2  5  0.5 0

i "Trigger_Demo"     20  1      2

i "Gate_Open_Demo"   25  1      2 0
i "Gate_Close_Demo"  30  1      0

i "Gate_Open_Demo"   27  1      3 1
i "Gate_Close_Demo"  32  1      1

i "AR_Demo_1"        35  1      2 10  0 0.5 0
i "AR_Demo_2"        50  1      2 10  0 0.5 0.6 0.3 0
i "ASR_Demo"         65  1      2 10  0 0.3 0.6 0.4 0.3 0

i "LFO_Demo_1"       80 10      2 0.3 0.5  0   ; bipolar sine
i "LFO_Demo_2"       95 10      2 0.3 0.25 1   ; unipolar triangle

e
</CsScore>
</CsoundSynthesizer>