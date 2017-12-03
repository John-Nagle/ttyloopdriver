# Version log

## Version 1

Version 1 not successful.  The 555 timer can't produce
enough peak drive for the MOSFET, and only about 20V comes out.
Redesign underway.

## Update 2016-12-19

Redesign complete. SPICE model (in directory "circuitsim/ttydriver.asc") works.  Gil Smith is building up a prototype for
circuit testing.  If that works, a new PC board will be designed.

The next PC board will have switches, LEDs, and phone jacks on the board, so no external wiring harness
will be required.

## Update 2017-04-18

Board 2.0 will drive a Model 15 Teletype with a few changes to the board.  The keyboard side doesn't work.
Board 2.1 being built.

## Update 2017-04-21

Board 2.1 will drive a Model 15 Teletype with the following fixes:

- Bypass USB current limiter U2 by jumpering pins 1 to 6.  It's tripping at too low a current.  Check R16 value again.
Printer side is then OK. After further testing, the current limiter is working fine; it trips if the printeroutput
is shorted or there's no selector magnet plugged in. After about 10 seconds, U2 will cool down and re-enable power.

- Keyboard side needs a lower value resistor for R9 than 2.2K. Not enough pulldown.

- Jumpering R9 with a 1.5K resistor makes the keyboard side work. That's equivalent to an R9 value of about 
900 ohms.  4.5V/900 = 5mA there, for 0.03W. OK.  Try 1K for R9.

- Motor control LED is always on.  Probably a pullup resistor problem.  RTS is an active low. RTS signal
shows 3V for OFF, 0.2V for ON in current circuit, but U7 remains on even for the OFF condition.
R17 needs to be larger, or this needs a redesign.

## Update 2017-05-13

Board 2.2 not built; more pull-in energy is needed. The voltage decays too fast, and only
one of three Teletypes will work with the 1uf @ 120V cap.  Board 2.3 will have 2uf @ 120V. 
This should provide enough punch to pull in the selector fast enough. Github files are updated
to Board v2.3.0, but the board has not been sent to fab yet.

## Update 2017-05-15

Board 2.3 sent to fab.

## Update 2017-06-20

Board 2.3 can't charge its 2uf of capacitors in less than 40ms.
The LTSPICE model and the real board disagree in transformer current
by about 2x. Unclear why.  Possible transformer saturation.

Efficiency calc: 
    
2uf at 120V is  14.4mJ
    
400mA at 4.8V is 1.92W. 1.92W x 20ms = 0.0384 watt-seconds = 0.0384 joules = 38.4 mJ

Efficiency needed is 14.4 / 38.4 = 38%. Should be easily achieveable.

## Update 2017-08-25

Board 3.1, a completely new design using an LT3750 capacitor charging controller, works, except 
that the current limiter U2 keeps tripping. Successful typing with a Model 15 Teletype.
The capacitors charge to 122V in about 14ms, which is close to what simulation predicts.

The AP2553W6 current limiter trips for about half a second about twice a minute on average. 
If the current limiter is bypassed, it works fine.  Measured current through the current limiter,
with a 2.2 ohm current sense resistor placed in series for testing,  is I = E/R = 0.5/2.2 = 227mA.
This is well below the current limiter setpoint.  R1 at 56.3K ohms should result in a 400mA current
limit. Unclear why the limiter is tripping. 

(Turned out that the current limiter was tripping because the circuit for motor control was
back-feeding power into the U2 from the output side, which the current limiter detects as
a fault condition.)
    
## Update 2017-09-18

Board version 3.2 built and tested. Successfully drives
Teletype Model 15 with 220 ohm selector and Teletype Model
14 with 55 ohm selector. The current limit is too high, though;
the 55 ohm selector is getting 80mA instead of 60. This is also
the current if the output is shorted, so the current limiter is 
working. It just needs adjustment. Changing R5 to 22 ohms should
fix it. 

## Update 2017-10-12

Board version 3.3.  Fully working board. Drives Teletype Model 15 and 14 successfully, both
220 ohm and 55 ohm versions. Steve Garrison built a copy of the board and successfully drove a Model 28 with it.

# Development notes

New approach:
Five 5V to 24V power supplies in series to charge a 2uf cap.

Theoretical efficiency calc: 
    
2uf at 120V is14.4mJ
    
400mA at 4.8V is 1.92W. 1.92W x 20ms = 0.0384 watt-seconds = 0.0384 joules = 38.4 mJ

Efficiency needed is 14.4 / 38.4 = 38%. Should be easily achieveable.

Power budget:

Need 13.5mA at 120V to charge cap in 18ms
using circuit "dummy02.asc"

Each DC-DC converter must generate 13.5mA at
24V from 4.8V. Stated efficiency is 80%.

So that's 0.32W per converter out, 0.40W in,
2W total for all power supplies. 416mA.

Why so high?

2017-06-26

Beginning new board design with Linear Technology cap charger IC.

- Motor control jack shorts during plug pull. Change connector.
- Footprint for inverter may be wrong.

2017-06-28

Some devices have 0.3mm pin width with 0.5mm pin spacing. So
inter-pin clearance is only 0.2mm. This is incompatible with
the old design rules.

It's a problem with GND and Vcc pins, because those traces
belong to class POWER, which is wide. Need to create a
dummy "device" which just narrows a trace to 0.3mm, and
a narrow trace type with 0.3mm width, 0.2mm clearance.
This is only needed in two places.

2017-08-26

U2, the AP2553W6, keeps shutting down randomly.
Bypassing it turns it on again for a while.

Observed: 
- when U2 is shut down, the voltage on the +5 rail is about 1V.

- when U2 is running, voltage is about 5V, but has about 1V of
noise at switcher cycle startup.

- adding 1uF ceramic cap between test points W1 and W2 reduces
noise by at least half. 

Possible explanation: if voltage on the +5 bus goes low,
the path from CTS through zener D2, backwards,
provides 1V to the +5 rail, even with the power switch off.
This triggers the reverse voltage detection in U2. 

The circuit around U7, to control the motor control
relay from the CTS line, needs work. CTS is an active
low, so there's a pull-up involving R17 and D2. But
does it put out a little voltage when it's high?
Measure this.

Unclear why U2 should turn off once on. There should be
no time when the input side to U2 goes that low with the
powe switch on. 

Possible fixes: 

- Another bypass cap on +5

- Additional diode to prevent reverse current flow between +5 and RTS.

- Test fix: remove D2 and see if that stops shutdowns.

2017-08-27

Observed:

About 0.5V is coming from CTS back into the +5 rail, even
with the power switch off.

U2 still goes into shutdown as if current limiting. Tried
putting a 100K resistor across R16, and that stopped.
Removed 100K resistor, and U2 went in and out of shutdown,
period about 30 seconds. 

Tried measuring current with 1.1 ohm resistor bypassing
U2 and S1, using scope and scope.
Big transient. At 0.5v/div, seeing 2 to 2.5 divisions of
oscillation.  I = E/R = 1.25/1.1 = 1.3A. There's the transient
overload. Need still more bypass caps.  The spikes are only
about 25ns, and after the first few, they're small.
Maybe a ferrite bead?

Top green LED (TxD) is not lighting up. (Was unsoldered pin;
fixed. Not a design problem.)

Notes:

100K in parallel with 53.6K is 34.9K. That, per
AP2553W6 data sheet, sets current limit to 600mA.
Normal current limit with 53.6K is suppposed
to be 400mA. Should not be drawing that much current.
Previously,  measured current through the current limiter,
with a 2.2 ohm current sense resistor placed in series for testing,
is I = E/R = 0.5/2.2 = 227mA.

Proposed changes:

- Add 1uh inductor after pin 6 of U2.
  DigiKey 1276-6207-1-ND 
  Samsung CIG22E1R0MNE
  FIXED IND 1UH 2.3A 48 MOHM SMD 
  SMD form factor 1008
  
- Add 0.1uf cap between pin 6 of U2 and GND.
  Same part as C10
  
- Add Shottky diode in series with D2 to prevent
  backflow. Reduce value of D2 Zener by voltage drop
  of new diode.  (Is there some easier way to get this
  pull-up?)
  
  Temporary workaround: 
  
  Jumper pin 1 of S1 to test point W2. This bypasses
  U2 completely. USB overcurrent protection is lost but
  the board will run Model 14 and 15 Teletypes. 
  
  2017-08-30
  
  Improve sustain current regulation
  
  - Use 15V power supply instead of 12V
     DigiKey 1470-1405-5-ND 
     XP Power part IE0515S
  - Use two current regulators in parallel to limit to 60mA
     ON Semiconductor NSI45030AT1G
     IC LED DRIVER LINEAR SOD-123 
     DigiKey NSI45030AT1GOSTR-ND
     $0.17ea.
     Needs diode for reverse protection, which we already have
     
Get rid of JP1 and R5. Current regulation now fully automatic.

2017-09-15

  Board version 3.2 built and tested. Successfully drives
  Teletype Model 15 with 220 ohm selector and Teletype Model
  14 with 55 ohm selector. The current limit is too high, though;
  the 55 ohm selector is getting 80mA instead of 60. This is also
  the current if the output is shorted, so the current limiter is 
  working. It just needs adjustment. Changing R5 to 22 ohms should
  fix it. 
  
2017-10-11

  Board version 3.3 built and tested. Input current limit U2 is tripping.
  Everything else works if U2 is bypassed. Looking at current on scope,
  there are spikes to 700mA about 25ns wide. Will try changing L1 to
  6.8uH to get spikes under contol.

2017-10-12

  Board works. Changed L1 to 6.8uH, but that wasn't the problem. The
  problem was a bad solder joint at pin 1-4 of U3.  This is the ENABLE
  signal that turns on the power. With the EN signal to U2 floating, 
  the +5 power would randomly be on, off, or current-limited. Touching
  a test probe to the board would change the situation. That's fixed.
  Looking good. Board drove a Model 15 Teletype correctly, including
  the motor control output.
