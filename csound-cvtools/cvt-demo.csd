;===============================================================================
; Csound CV Tools
; Dave Seidel, 11/29/2020 (initial release)
;===============================================================================

<CsoundSynthesizer>
<CsOptions>
; ES-8
--format=long -odac:hw:1,0
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
    printarray(gk_gates, ktrig, "%0.2f", "before open")
    cvt_gate_open(ichn, igate)
    printarray(gk_gates, ktrig, "%0.2f", "after open")
    ktrig = 0
endin

instr Gate_Close_Demo
    igate = p4
    ktrig init 1

    timer()
    printarray(gk_gates, ktrig, "%0.2f", "before close")
    cvt_gate_close(igate)
    printarray(gk_gates, ktrig, "%0.2f", "after close")
    ktrig = 0
endin

instr Ramp_Demo
    ichn = p4
    idur = p5
    ibeg = p6
    iend = p7

    cvt_ramp(ichn, idur, ibeg, iend)
endin

instr AR_Demo
    ichn = p4
    idur = p5
    ibeg = p6
    imid = p7
    iend = p8

    cvt_ar_env(ichn, idur, ibeg, imid, iend)
endin

</CsInstruments>
<CsScore>

i "Ramp_Demo" 0   1  2  5  0 0.5
i "Ramp_Demo" 10  1  2  5  0.5 0

i "Trigger_Demo" 35  1  2

i "Gate_Open_Demo"  40  1  2 0
i "Gate_Close_Demo" 45  1  0

i "Gate_Open_Demo"  42  1  3 1
i "Gate_Close_Demo" 47  1  1

i "AR_Demo" 50 1 2 10 0 0.5 0

e
</CsScore>
</CsoundSynthesizer>