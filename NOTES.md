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
