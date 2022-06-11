# Csound CV Tools

Convenience functions for use with DC-coupled audio interfaces, such as the Expert Sleepers ES-8, to generate control signals for modular synths (or other such hardware).

On the ES-8, we have the ability to send DC voltages that range from -10V to 10V (20V peak to peak). From the Csound perspective, these correspond to output values of -1 to 1 (or, more safely, -0.99999 to 0.99999). A Csound output unit of 0.1 corresponds to 1V.

However, for typical CV usage, it's more useful to stay with the range -5V to 5V (bipolar) or 0V to 5V (unipolar). These ranges correspond to Csound outputs of -0.5 to 0.5, or 0 to 0.5.

The demo program (`cvt-demo.csd`), when used to produce a sound file, which will show the shapes of the emitted signals when viewed in an audio editor such as Audacity.

Dave Seidel
 - 11/29/2020 (initial version)
 - 12/5/2020 (latest update)

## UDOs

### Note on synchronous vs. asynchronous operation

All of these opcodes, with the exception of the LFO, are asynchounous, in the sense that they trigger a new instrument instance that will run on their own for the specifed overall duration, regardless of the duration of the instrument from which they were launched.

The LFO opcodes are synchronous, in the sense that they run for the lifetime of the enclosing instrument instance.

### Triggers and Gates

 * cvt_trigger
    ```
    cvt_trigger(i_channel[, i_duration[, i_value]])
    ```

    Emits a 5V impulse on the given output channel. Optionally, you can use `i_duration` to specify the duration of the impulse in seconds to override the default duration of 2ms (e.g., use `0.005` for 5ms). You can also optionally set the amplitude value of the impulse to override the default of 0.5 (5V).

 * cvt_gate_open

    ```
    cvt_gate_open(i_channel, i_gate_id[, i_value])
    ```

    Starts a 5V signal on the given output channel, using `i_gate_id` as the gate ID (this is used later to close the gate). There are 16 concurrent gates available, numbered 0-15. You can optionally use `i_value` to set the amplitude value of the impulse to override the default of 0.5 (5V).

 * cvt_gate_close

    ```
    cvt_gate_close(i_gate_id)
    ```

    Ends the specified gate signal.

### Ramps and Simple Envelopes

Acceptable range for start/middle/end values: -0.99999 to 0.99999; recommended range: -0.5 to 0.5 (-5V to 5V).

 * cvt_ramp
 * cvt_exp_ramp

    ```
    cvt_ramp(i_channel, i_duration, i_start, i_end)
    cvt_exp_ramp(i_channel, i_duration, i_start, i_end)
    ```

    Emits a ramp, specifying the duration, starting value, and ending value. The "exp" version uses a exponential ramp; the other version is linear.
 * cvt_ar_env_eq
 * cvt_ar_exp_env_eq

    ```
    cvt_ar_env_eq(i_channel, i_duration, i_start, i_middle, i_end)
    cvt_ar_exp_env_eq(i_channel, i_duration, i_start, i_middle, i_end)
    ```

    Emits an Attack/Release envelope with equal-length rise and fall, specifying the overall duration and starting, middle and ending values. The "exp" version uses a exponential ramp; the other version is linear.

 * cvt_ar_env
 * cvt_ar_exp_env

    ```
    cvt_ar_env(i_channel, i_duration, i_start, i_dur1, i_middle, i_end, i_dur2)
    cvt_ar_exp env(i_channel, i_duration, i_start, i_dur1, i_middle, i_end, i_dur2)
    ```

    Emits an Attack/Release envelope with control over each segment, specifying the overall duration, starting, middle and ending values, and relative length of each segment. The "exp" version uses a exponential ramp; the other version is linear.
    
    Segment durations are specified as a fraction of the total duration and should add up to 1. `i_dur1` is the relative legnth of the rise, and `i_dur2` is he relative length of the fall For example, use `i_dur1=0.5` and `i_dur2=0.5` for equal-length segments.

 * cvt_asr_env
 * cvt_asr_exp_env

    ```
    cvt_asr_env(i_channel, i_duration, i_start, i_dur1, i_middle, i_dur2, i_dur3, i_end)
    cvt_asr_exp_env(i_channel, i_duration, i_start, i_dur1, i_middle, i_dur2, i_dur3, i_end)
    ```

    Emits an Attack/Sustain/Release envelope with control over each segment, specifying the overall duration, starting, middle and ending values, and relative legnth of each segment. The "exp" version uses a exponential ramp; the other version is linear.
    
    Segment durations are specified as a fraction of the total duration and should add up to 1. `i_dur1` is the relative legnth of the rise, `i_dur2` is the relative length of the sustain, and `i_dur3` is he relative length of the fall. For example, use `i_dur1=0.5`, `i_dur2=0.3` and `i_dur3=0.2` for a long rise, shorter sustain, and even shorter fall.

### Simple LFOs

 * cvt_lfo

 ```
 cvt_lfo(ichn, kamp, kcps, itype)
 ```

 Emits a bipolar LFO, with selectable shape. See the Csound `lfo` opcode for an explanation of the `kamp`, `kcps`, and `itype` paramaters.

 * cvt_lfo_uni

 ```
 cvt_lfo_uni(ichn, kamp, kcps, itype)
 ```

 Same as `cvt_lfo` but unipolar (positive only).

### Pitch

* cvt_f2p
```
cvt_f2p(ifreq)
cvt_f2p(kfreq)
```

Given a frequency, returns a pitch voltage value.

* cvt_ft2p

```
cvt_ft2p(itab, indx)
```

Given a tuning table and an index, returns a pitch voltage value.

* cvt_ft2pt
```
cvt_ft2pt(iintab, iouttab)
```

Given a GEN51 tuning table, populates another table with corresponding pitch voltages.
The desination table is assumed to be the same size as the tuning table.

* cvt_pitch
```
cvt_pitch(ichn, idir. ival)
```

Given an output channel, a duration, and a pitch voltage value, outputs a pitch voltage.
