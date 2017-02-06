# ttyloopdriver
Hardware device for driving antique Teletype machines

![Prototype board](board/images/boardpopulatedv1.0.jpg)

WORK IN PROGRESS. 
## Status 

version 1 not successful.  The 555 timer can't produce
enough peak drive for the MOSFET, and only about 20V comes out.
Redesign underway.

### Update 2016-12-19

Redesign complete. SPICE model (in directory "circuitsim/ttydriver.asc") works.  Gil Smith is building up a prototype for
circuit testing.  If that works, a new PC board will be designed.

The next PC board will have switches, LEDs, and phone jacks on the board, so no external wiring harness
will be required.

# What it is

This is a board to allow connecting antique Teletype machines to a computer through
a USB port. It's for Teletype Model 14 and 15 machines, which use 60mA current
loops.   This board needs no external power supply other than the USB port.
This approach uses only about 1 watt of power, drawing 200mA from the USB port. 


# How it works

With a switching power supply, of course.

## Output to the Teletype

At the USB end is a CP2012 breakout board U3.  The Silicon Labs CP2102 is a USB
to serial converter, one of the few which can be reprogrammed for 45 baud
operation.  We reprogram it to map a request for 600 baud to 45 baud.
We also reprogram it to request 500mA from the USB port.

There are two power supplies for the output. One is a custom switching
power supply which, during SPACE, charges up a 1uF capacitor C2 to
120V. This provides the initial power to pull in the selector magnet,
pushing 60mA through the huge 4H inductance of the magnet coils.
The other is a 12V supply U8 which provides sustaining current at 60mA
once C2 has discharged.  Both power supplies feed, through diodes D6
and D5, a solid-state relay U4. The relay is controlled by the transmit
data line TxD from U3.

The switching power supply consists of an oscillator and a
switcher. The oscillator, U1, is a classic 555 timer, set
up for approximately 100KHz, 50% duty cycle.

The switcher is an isolated boost supply, consisting of
U9, T1, C2, and some passives.  The oscillator signal
turns the FET in U9 on and off. Turning Q1 off produces an inductive
kick in T1, which has a 1:15 turns ratio.  This can produce
over 120VDC, which is used to charge C2.  To limit the
charge, D7, a 120V Zener diode, clamps the voltage
to 120V. 

C2 charging occurs only during SPACE. During MARK, TxD goes high,
and, through diode D9, forces the TR pin of U1 high. This
stops the oscillator during MARK, when it's not needed. 
The FET in U9 is thus turned off during MARK. 

The sustain supply U8 is always on, but there is no load on it
during SPACE, because U4 is turned off.  So the two power
supplies take turns drawing
power from the USB port, which keeps the peak current down.

## Input from the keyboard

On the keyboard side, U6, a very small 5V to 24V DC-DC
converter, produces enough voltage for Teletype keyboard
contacts, which may have oil or dirt on them.  A 5V
logic level is known to be too weak for this.  Another
opto-isolator, U5, isolates the keyboard from the logic
level circuitry.  There's a BREAK button, SW2, so that
a BREAK can be sent even if no keyboard is present.

## Motor control

A standard 5V solid state relay, such as a Crydom CSW2410-10 can 
be plugged into jack J3 for Teletype motor control.  This will
turn on when the USB serial port raises Request to Send and power is on.
The middle green light of D13 will also turn on.
The "Baudotrss" software package supports this function.

## Power management

This board is powered entirely from a USB port.  There are
strict rules about drawing power from a USB port, and most
modern laptop computers have a USB port controller wihich strictly
enforces them.  If a device draws too much current, even for a 
millisecond, the port turns off power, and usually won't
turn back on again until the laptop is turned off.  Devices
must negotiate with the power source for how much power they
want, and the power source can say no.  This happens when the
device is plugged into the USB port, or when the laptop turns
the port on.

USB devices are guaranteed 100mA, but if you want 
more than that, you have to ask. We ask for 500mA, the maximum
for USB versions 1 and 2, by programming a register in the CP2102
USB interface.  If the host device says yes, the
CP2012 turns on /SUSPEND after successful completion of the
power handshake.  Turning off the device in software (as when
the host computer goes to sleep) will turn off /SUSPEND.

U2 is a AP2553W6 power control IC intended for USB ports.  When
/SUSPEND goes high, it turns on and lets power into the rest of
the board.  It also has a built-in power limit, set to 400mA by
resistor R16, which limits the inrush current as C1 charges at power
up.  If turn-on is successful, and SW1 is on, the VPWR line comes
up and everything on the board gets power, including the top
LED of D13.

With some operating systems, this won't happen until
the USB port is opened by software.  If the computer goes to sleep,
everything will turn off.  Most USB hubs and some "smart" USB
extension cables will reject a request for 500mA, and the
light won't come on. If the light will come on when the USB cable
is directly plugged into a computer, but won't come on when plugged
in through a long cable or hub, that's the reason.

## Circuit protection

R1 and C3 are a filter for the inductive spikes from
the Teletype selector magnet. The back to back 120V Zeners
D10 and D11 protect against the inductive kickback spikes
from the selector magnet.

On the input side, C9, C1, C5, and L3 keep the inductive
kickback from T1 from getting back into the USB power supply.

The AP2553W6 provides overload protection to the USB port.
The CPC1510G solid state relays also provide current limiting,
in case the printer output is shorted.

On the Teletype side, everything is isolated from ground and from the USB side.

## Connectors

J1 is the 1/4" Teletype printer jack, supplying 120VDC at 60mA for a Teletype Model
14 or 15.  Only one printer can be driven; there is not enoug power to drive a whole chain
of machines.

J2 is the 1/4" Teletype keyboard jack, supplying power for a Model 14/15 keyboard.
If nothing is plugged in, the jack shorts and the BREAK button still works.

P1 is a jumper for Teletypes wired with the selector magnets in series.

 220 ohm selector magnet (series) -> jumper IN
    
 55 ohm selector magnet (parallel) -> jumper OUT

P2 is a connection for a current meter.  A 100mA meter
is suggested. If a meter is not used, this plug must
be jumpered.

J3 is a smalll jack for a solid state relay (5V in) to
turn on the Teletype motor.  Use of this is optional.

## Controls and indicators

SW1 is the main power switch.

SW2 is a BREAK button, interrupting the keyboard circuit.  This works even if no keyboard is present.

D13 is a 3-high set of green LEDs.

 Top - Power ON
 Middle - Motor ON
 Bottom - Data output
 
 The data output LED shows current flowing in the selector magnet circuit. It won't come on until
 there's a printer plugged in.  It will flicker as data goes to the printer, and light steadily
 when the printer is on and idle.
 
## Computer interface

This unit appears to most computers as a serial port. No special driver should be required.
The port should be opened and set to 600 baud to request
45 baud output.  (The CP2102 is programmed for this, because many systems can't request 45 baud. 600 baud is used
because that speed was never used for any historical devices.)  When power is on,
Data Set Ready will turn on. When power is on and the motor is running, Clear to Send will turn on.
Power management works; if the computer goes to sleep or suspends, the board will turn off.

## Packaging

The board is 75mm x 120mm, and will fit in a Hammond 1455K1202 box.

