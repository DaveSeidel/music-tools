# Csound CV Tools

Convenience functions for use with DC-coupled audio interfaces, such as the Expert Sleepers ES-8, to generate control signals for modular synths (or other such hardware).

On the ES-8, we have the ability to send DC voltages that range from -10V to 10V (20V peak to peak). From the Csound perspective, these correspond to output values of -1 to 1 (or, more safely, -0.99999 to 0.99999). A Csound output unit of 0.1 corresponds to 1V.

However, for typical CV usage, it's more useful to stay with the range -5V to 5V (bipolar) or 0V to 5V (unipolar). These ranges correspond to Csound outputs of -0.5 to 0.5, or 0 to 0.5.

Dave Seidel, 11/29/2020 (first release)

## UDOs

This is an intial set, and will likely grow in the future to include LFOs and other functions.

 * cvt_trigger

    Usage: `cvt_trigger(i_channel)`

    Emits a 5V impulse with a duration of 2 ms on the given output channel.

 * cvt_gate_open

    Usage: `cvt_gate_open(i_channel, i_gate_id)`

    Starts a 5V signal on the given output channel, using `i_gate_id` as the gate ID (this is used later to close the gate). There are 16 concurrent gates available, numbered 0-15.

 * cvt_gate_close

    Usage: `cvt_gate_close(i_gate_id)`

    Ends the specified gate signal.

 * cvt_ramp

    Usage: `cvt_ramp(i_channel, i_duration, i_start, i_end)`

    Emits a linear ramp, specifying the duration, starting value, and ending value. Acceptable range: -0.99999 to 0.99999; recommended range: -0.5 to 0.5 (-5V to 5V).

 * cvt_ar_env

    Usage: `cvt_ar_env(i_channel, i_duration, i_start, i_middle, i_end)`

    Emits a linear Attack/Release evelope, specifying the duration and starting, middle and ending values. Acceptable range: -0.99999 to 0.99999; recommended range: -0.5 to 0.5 (-5V to 5V).
