;===============================================================================
; Csound CV Tools
; Dave Seidel
; v1.0 2020-12-21
; v1.1 2022-06-11
;===============================================================================


;-------------------------------------------------------------------------------
; macros
;-------------------------------------------------------------------------------

; voltage scaling
#define CVT_SCALING_FACTOR  #0.1#

; 2ms trigger
#define CVT_TRIG_DUR    #0.002#

; 5V impulse
#define CVT_IMP_VAL     #5 * $CVT_SCALING_FACTOR#

; gate IDs
gk_cvt_gates[] init 16

; tuning base / freq0
; oct value 4.0 => C0 (MIDI note 12)
#ifndef CVT_TUNING_BASE
#define CVT_TUNING_BASE #4.0#
#endif
gi_cvt_f0 = cpsoct($CVT_TUNING_BASE)


; frequency-to-pitch-voltage conversion 
#define CVT_F2P(FREQ)  #log2($FREQ / gi_cvt_f0) * $CVT_SCALING_FACTOR#


;-------------------------------------------------------------------------------
; instrument definitions, used by the UDOs
;-------------------------------------------------------------------------------

instr +_impulse
    ichn = p4
    ival = p5
    outch(ichn, a(ival))
endin

instr +_ramp
    idur = p3
    ichn = p4
    ibeg = p5
    iend = p6    
    outch(ichn, line:a(ibeg, idur, iend))
endin

instr +_exp_ramp
    idur = p3
    ichn = p4
    ibeg = p5
    iend = p6

    if ibeg == 0 then
        ibeg = 0.001
    endif
    if iend == 0 then
        iend = 0.001
    endif
    outch(ichn, expon:a(ibeg, idur, iend))
endin

instr +_ar_env_eq
    idur  = p3
    ichn  = p4

    ibeg  = p5
    imid  = p6
    iend  = p7
    
    outch(ichn, linseg:a(ibeg, idur*0.5, imid, idur*0.5, iend))
endin

instr +_ar_exp_env_eq
    idur  = p3
    ichn  = p4

    ibeg  = p5
    imid  = p6
    iend  = p7
    
    if ibeg == 0 then
        ibeg = 0.001
    endif
    if imid == 0 then
        imid = 0.001
    endif
    if iend == 0 then
        iend = 0.001
    endif
    outch(ichn, expseg:a(ibeg, idur*0.5, imid, idur*0.5, iend))
endin

instr +_ar_env
    idur  = p3
    ichn  = p4

    ibeg  = p5
    idur1 = p6
    
    imid  = p7
    idur2 = p8
    
    iend  = p9
    
    outch(ichn, linseg:a(ibeg, idur*idur1, imid, idur*idur2, iend))
endin

instr +_ar_exp_env
    idur  = p3
    ichn  = p4

    ibeg  = p5
    idur1 = p6
    
    imid  = p7
    idur2 = p8
    
    iend  = p9
    
    if ibeg == 0 then
        ibeg = 0.001
    endif
    if iend == 0 then
        iend = 0.001
    endif
    outch(ichn, expseg:a(ibeg, idur*idur1, imid, idur*idur2, iend))
endin

instr +_asr_env
    idur  = p3
    ichn  = p4

    ibeg  = p5
    idur1 = p6
    
    imid  = p7
    idur2 = p8
    
    idur3 = p9
    iend  = p10
    outch(ichn, linseg:a(ibeg, idur*idur1, imid, idur*idur2, imid, idur*idur3, iend))
endin

instr +_asr_exp_env
    idur  = p3
    ichn  = p4

    ibeg  = p5
    idur1 = p6
    
    imid  = p7
    idur2 = p8
    
    idur3 = p9
    iend  = p10

    if ibeg == 0 then
        ibeg = 0.001
    endif
    if imid == 0 then
        imid = 0.001
    endif
    if iend == 0 then
        iend = 0.001
    endif
    outch(ichn, expseg:a(ibeg, idur*idur1, imid, idur*idur2, imid, idur*idur3, iend))
endin


;-------------------------------------------------------------------------------
; UDOs
;-------------------------------------------------------------------------------

;;;;; Triggers & gates

opcode cvt_trigger, 0, ijj
    ichn, idur, ival xin

    if (idur == -1) then
        idur = $CVT_TRIG_DUR
    endif
    if (ival == -1) then
        ival = $CVT_IMP_VAL
    endif
    schedule("_impulse", 0, idur, ichn, ival)
endop

opcode cvt_gate_open, 0, iij
    ichn, igate, ival xin

    if (ival == -1) then
        ival = $CVT_IMP_VAL
    endif
    iinst = nstrnum("_impulse") + (unirand(256) * 0.001)
    schedule(iinst, 0, -1, ichn, ival)
    gk_cvt_gates[igate] = k(iinst)
endop

opcode cvt_gate_open, 0, iiJ
    ichn, igate, kval xin

    if (kval == -1) then
        kval = $CVT_IMP_VAL
    endif
    iinst = nstrnum("_impulse") + (unirand(256) * 0.001)
    schedule(iinst, 0, -1, ichn, kval)
    gk_cvt_gates[igate] = k(iinst)
endop

opcode cvt_gate_close, 0, i
    igate xin

    kinst = gk_cvt_gates[igate]
    turnoff2(kinst, 4+8, 0)
    gk_cvt_gates[igate] = 0
endop

;;;;; Ramps

; i-rate version
opcode cvt_ramp, 0, iiii
    ichn, idur, ibeg, iend xin
    schedule("_ramp", 0, idur, ichn, ibeg, iend)
endop

; k-rate version
opcode cvt_ramp, 0, kkkk
    kchn, kdur, kbeg, kend xin
    schedulek("_ramp", 0, kdur, kchn, kbeg, kend)
endop

; i-rate version
opcode cvt_exp_ramp, 0, iiii
    ichn, idur, ibeg, iend xin
    schedule("_exp_ramp", 0, idur, ichn, ibeg, iend)
endop

; k-rate version
opcode cvt_exp_ramp, 0, kkkk
    kchn, kdur, kbeg, kend xin
    schedulek("_exp_ramp", 0, kdur, kchn, kbeg, kend)
endop

;;;;; Simple envelopes

; attack-release envelope (equal rise/fall)
; args:
; - output channel
; - overall duration
; - starting value
; - max value
; - end value
;
opcode cvt_ar_env_eq, 0, iiiii
    ichn, idur, ibeg, imid, iend xin
    schedule("_ar_env_eq", 0, idur, ichn, ibeg, imid, iend)
endop

opcode cvt_ar_exp_env_eq, 0, iiiii
    ichn, idur, ibeg, imid, iend xin
    schedule("_ar_exp_env_eq", 0, idur, ichn, ibeg, imid, iend)
endop

; attack-release envelope (adjustable rise/fall)
; args:
; - output channel
; - overall duration
; - starting value
; - duration from starting value to max value
; - max value
; - duration from max value to end
; - end value
;
opcode cvt_ar_env, 0, iiiiiii
    ichn, idur, ibeg, idur1, imid, iend, idur2 xin
    schedule("_ar_env", 0, idur, ichn, ibeg, idur1, imid, iend, idur2)
endop

opcode cvt_ar_exp_env, 0, iiiiiii
    ichn, idur, ibeg, idur1, imid, iend, idur2 xin
    schedule("_ar_exp_env", 0, idur, ichn, ibeg, idur1, imid, iend, idur2)
endop

; attack-sustain-release
; args:
; - output channel
; - overall duration
; - starting value
; - duration from starting value to max value
; - max (sustain) value
; - duration of sustain
; - duration from max value to end
; - end value
;
opcode cvt_asr_env, 0, iiiiiiii
    ichn, idur, ibeg, idur1, imid, idur2, iend, idur3 xin
    schedule("_asr_env", 0, idur, ichn, ibeg, idur1, imid, idur2, iend, idur3)
endop

opcode cvt_asr_exp_env, 0, iiiiiiii
    ichn, idur, ibeg, idur1, imid, idur2, iend, idur3 xin
    schedule("_asr_exp_env", 0, idur, ichn, ibeg, idur1, imid, idur2, iend, idur3)
endop

;;;;; Simple LFOs

; bipolar LFO, see lfo opcode for args
opcode cvt_lfo, 0, ikki
    ichn, kamp, kcps, itype xin
    outch(ichn, lfo:a(kamp, kcps, itype))
endop

; unipolar LFO, see lfo opcode for args
opcode cvt_lfo_uni, 0, ikki
    ichn, kamp, kcps, itype xin
    outch(ichn, lfo:a(kamp, kcps, itype) + a(kamp))
endop

;;;;; Pitch

; Given a frequency, return a pitch voltage value.
; args:
;  - i/kfreq (frequency)
; returns:
;  - pitch voltage
opcode cvt_f2p, i, i
    ifreq xin
    ; xout log2(ifreq / gi_cvt_f0) * $CVT_SCALING_FACTOR
    xout $CVT_F2P(ifreq)
endop

opcode cvt_f2p, k, k
    kfreq xin
    ; xout log2(kfreq / gi_cvt_f0) * $CVT_SCALING_FACTOR
    xout $CVT_F2P(kfreq)
endop

; Given a tuning table and an index, return a pitch voltage value.
; args:
;  - itab (table)
;  - indx (table index of frequency)
; returns:
;  - pitch voltage
opcode cvt_ft2p, i, ii
    indx, itab xin
    ifreq = table(indx, itab)
    ipv = $CVT_F2P(ifreq)
    ; ipv = log2(ifreq / gi_cvt_f0) * $CVT_SCALING_FACTOR
    xout ipv
endop

; Given a GEN51 tuning table, populate another table with corresponding pitch voltages.
; The desination table is assumed to be the same size as the tuning table.
; args:
;  - iintab (input table, GEN51)
;  - iouttab (output tabel, must be same size as input table)
; returns:
;  - nothing
opcode cvt_ft2pt, 0, ii
    iintab, iouttab xin
    indx init 0
    ilen = tableng(iintab)

    until indx == ilen do
        iorig = table(indx, iintab)
        ipv = $CVT_F2P(iorig)
        tablew(ipv, indx, iouttab)
        indx += 1
    od
endop

; Outputs a pitch voltage.
; args:
;  - ichn (output channel)
;  - idur (duration of output)
;  - ival (pitch voltage value) 
; returns:
;  - nothing
opcode cvt_pitch, 0, iii
    ichn, idur, ival xin
    schedule("_impulse", 0, idur, ichn, ival)
endop
