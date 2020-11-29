;===============================================================================
; Csound CV Tools
; Dave Seidel, 11/29/2020 (initial release)
;===============================================================================

#define CVT_TRIG_DUR    #0.002#
#define CVT_IMP_VAL     #0.5#

gk_gates[] init 16

;;;;;

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

instr +_ar_env
    idur = p3
    ichn = p4
    ibeg = p5
    imid = p6
    iend = p7
    
    outch(ichn, linseg:a(ibeg, idur/2, imid, idur/2, iend))
endin

;;;;;

opcode cvt_trigger, 0, i
    ichn xin

    prints("[Trigger <%d>]\n", ichn)
    schedule("_impulse", 0, $CVT_TRIG_DUR, ichn, $CVT_IMP_VAL)
endop

opcode cvt_gate_open, 0, ii
    ichn, igate xin

    iinst = nstrnum("_impulse") + (unirand(256) * 0.001)
    prints("[Opening gate %d -> %f <%d>]\n", igate, iinst, ichn)
    schedule(iinst, 0, -1, ichn, $CVT_IMP_VAL)
    gk_gates[igate] = k(iinst)
endop

opcode cvt_gate_close, 0, i
    igate xin

    prints("[Closing gate %d]\n", igate)
    kinst = gk_gates[igate]
    turnoff2(kinst, 4+8, 0)
    gk_gates[igate] = 0
endop

opcode cvt_ramp, 0, iiii
    ichn, idur, ibeg, iend xin
    prints("[Ramp %f -> %f (%fs) <%d>]\n", ibeg, iend, idur, ichn)
    schedule("_ramp", 0, idur, ichn, ibeg, iend)
endop

opcode cvt_ar_env, 0, iiiii
    ichn, idur, ibeg, imid, iend xin
    prints("[AR %f -> %f -> %f (%fs) <%d>]\n", ibeg, imid, iend, idur, ichn)
    schedule("_ar_env", 0, idur, ichn, ibeg, imid, iend)
endop

