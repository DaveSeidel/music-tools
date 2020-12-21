# Csound CV Tools

Convenience functions for use with DC-coupled audio interfaces, such as the Expert Sleepers ES-8, to generate control signals for modular synths (or other such hardware).

On the ES-8, we have the ability to send DC voltages that range from -10V to 10V (20V peak to peak). From the Csound perspective, these correspond to output values of -1 to 1 (or, more safely, -0.99999 to 0.99999). A Csound output unit of 0.1 corresponds to 1V.

However, for typical non-pitch CV usage, it's more useful to stay with the range -5V to 5V (bipolar) or 0V to 5V (unipolar). These ranges correspond to Csound outputs of -0.5 to 0.5, or 0 to 0.5. Pitch voltages may cover a wider ranger, depending on the device(s) to which you intend to send the pitch.

The demo program (`cvt-demo.csd`), when used to produce a sound file, will show the shapes of the emitted signals when viewed in an audio editor such as Audacity.

Dave Seidel, mysterybear.net
 - 11/29/2020 - initial version
 - 12/6/2020 - first update
 - 12/21/2020 - v1.0

## UDOs

### Note on synchronous vs. asynchronous operation

All of these opcodes, with the exception of the LFOs, are asynchounous, in the sense that they trigger a new instrument instance that will run on their own for the specifed overall duration, regardless of the duration of the instrument from which they were launched.

The LFO opcodes are synchronous: they run for the lifetime of the enclosing instrument instance.

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

   Emits a bipolar LFO with selectable shape. See the Csound `lfo` opcode for an explanation of the `kamp`, `kcps`, and `itype` paramaters.

 * cvt_lfo_uni

   ```
   cvt_lfo_uni(ichn, kamp, kcps, itype)
   ```

   Same as `cvt_lfo` but unipolar (positive only).

### Tuning

 * cvt_f2p
   ```
   ipitch = cvt_f2p(440)
   ```

   Given a frequency value (in Hz), returns a suitable pitch voltage value.

 * cvt_pitch
   ```
   cvt_pitch(ichn, idur, ipitch)
   ```

   Given an output channel, a duration, and a pitch value, emits a pitch voltage for the specified duration.

 * cvt_ft2pt
   ```
   ; GEN51 tuning table
   ituning_table = ftgen(0, 0, 128, -51, 12, 2, cpsoct(8), 60, ...)

   ; table to hold pitch voltages
   ipitch_table = ftgen(0, 0, -128, -2, 0, 0)
   
   ; populate pitch table
   cvt_ft2pt(ituning_table, ipitch_table)
   ```

   Given a GEN51 tuning table and an empty table of the same size, populates the ermpty table with ptch voltage values that correspond to the frequencies in the tuning table.

## Tuner Utility

We include a utility program called `tuner.csd` that emits two signals: an audio signal at a specified pitch, and a CV signal at a correspsonding pitch voltage. You can use this to tune any oscillator with a 1v/oct input by ear.

To make it easier to use, we also include a Linux shell script called `tuner.sh`.


```
Usage: tuner [-f FREQ] [-n NOTE] [-t TUNING] [-c CV_OUTPUT_CHANNEL]
```
Where:
 * FREQ is a frequency value in Hz
 * NOTE is a MIDI note number (e.g., 69 for A440, which is the default)
 * TUNING is either 1 for standard 12-TET tuning (the default) or 2 for the Grady Centaur just intonation tuning
 * CV_OUTPUT_CHANNEL is the output channel on your audio interface when you wwant to emit the pitch voltage (default: 7)

Running with no arguments is equivalent to executing
```
./tuner.sh -n 69 -t 1 -c 7
```
which emits a 440 Hz tone on output channel 1 and an equivalent pitch voltage on output channel 7.

### Notes
 * If you use the `-c` to specify a pitch by frequency (e.g., 440), the `-n` and `-t` options are ignored.
 * The files `tuner.csd` and `tuner.sh` must be in the same directory, and Csound must be on the path.
 * I intend to eventually provide a Windows command file that's equivalent in function to `tuner.sh`.