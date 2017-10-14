# CP2102 USB to serial converter programming

The USB to serial converter breakout board contains a Silicon Labs CP2102 USB to serial converter.
This needs some minor configuration.

## Configuration tool

This device is configured with Silicon Labs Simplicity Studio. This is a free download:

https://www.silabs.com/products/development-tools/software/simplicity-studio

It's a huge, complex package, which includes the full development environment for SiLabs processors. But all that's needed here
is the configuration tool for CP2102 devices.

Two configuration items have to be changed.

### Max Power (mA) 
Set to 400.

This tells the device to ask for up to 400mA of +5VDC power from the host device. USB devices get 100mA by default, and have to
ask if they want more. Low-powered devices, including many USB hubs, will refuse a request for 400mA. Desktop and laptop computers
will accept the request. If the request is refused, the power light on the TTY loop driver (the bottom green light) will not come on.

### Baud Rate Alias Configuration, 
Set the entry for 600 to 301 baud to 45 baud.

This causes the device to run at 45 baud if asked
to run at 600 baud.  (600 baud was never used for anything, so that's the value used for this purpose.)
Asking for 45 baud when opening the device won't work. 

### Serial number (optional)

If you have more than one of these devices, and want to run them off the same computer
at the same time, you may want to give them different serial numbers.

## Configuring the device

A folder, cp2102_gm, is provided. This contains a Simplicity Studio project for parts of type "CP2102-GM".
If you open this folder in Simplicity Studio, it will load the configuration paramerers above. (Or you can create a new Simplicity Studio
project for a "CP2102-GM" part and set the parameters yourself.)

Plug the USB device into the computer with Simplicity Studio running. Open the **cp2102_gm** project. 
The device parameters should appear on screen. Check for Max Power 400mA, and Baud Rate Alias for 600 to 301 set to 45 baud.
The serial number can also be set at this time.

Click on **PROGRAM TO DEVICE**.
This will bring up a menu of USB devices, usually just the CP2102 USB to UART Bridge Controller. Select that device, and it will be
programmed with the new parameters. 


