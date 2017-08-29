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

Top green LED (TxD) is not lighting up.

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
  


