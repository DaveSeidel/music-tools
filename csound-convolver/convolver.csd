;
; Convolver tool, applies an IR file to a sound file.
;
; This is intended to be driven by the "convolve.py" script,
; and should reside in the same directory.
;
; by Dave Seidel, 2013 (revised 2019)
;

<CsoundSynthesizer>

<CsInstruments>
;sr      = 48000
;ksmps   = 1
nchnls  = 2
0dbfs   = 1


; Borrowed from the Blue Share repository and adapted for use in this context.
; The original comment states:
;  Convolution Effect using pconvolve opcode by Matt Ingalls.
;  The code for this effect is based on code by Matt Ingalls found in the Csound Manual;
;  please see the manual for more information regarding pconvolve.
opcode convolver, aa, aai
  ; get input
  ain1,ain2,iwet xin

  ; dry vs. wet
  idry = 1 - iwet

  ; size of each convolution partion
  ipartsize = 1024

  ; calculate latency of pconvolve opcode
  idel = (ksmps < ipartsize ? ipartsize + ksmps : ipartsize) / sr

  prints("Convolving with a latency of %f seconds\n", idel)

  ; process left/right channels separately
  awetL1, awetR1 pconvolve iwet*ain1, "$IRFILE1", ipartsize
  awetL2, awetR2 pconvolve iwet*ain2, "$IRFILE2", ipartsize

  awetL = awetL1 + awetL2
  awetR = awetR1 + awetR2

  if (idry > 0) then
    ; Delay dry signal, to align it with the convolved sig
    adryL = delay(idry * ain1, idel)
    adryR = delay(idry * ain2, idel)

    ; mix
    aout1 = adryL+awetL
    aout2 = adryR+awetR
  else
    ; wet only, just pass it through
    aout1 = awetL
    aout2 = awetR
  endif

  ; send output
  xout(aout1,aout2)
endop


instr 1
  ;Soutfile getcfg 3
  ;prints "\n==========\ninput file: $INFILE\ngain adjustment: $GAIN\nimpulse response file: $IRFILE\noutput file: "
  ;prints Soutfile
  ;prints "\n==========\n\n"

  ; get length of file, use to set duration of instrument
  p3 = filelen("$INFILE")

; read in sound file tobe convolved
  aL, aR diskin2 "$INFILE", 1, 0, 0, 0, 9

  ; convolve it
  aLc, aRc convolver aL*$GAIN, aR*$GAIN, 1

  ; write it out
  outs(aLc, aRc)
endin

</CsInstruments>
<CsScore>

i1 0 1
e

</CsScore>

</CsoundSynthesizer>
