####Install Arduino 1.6.x

####Non blocking stepper motor on arduino
accelstepper library
http://www.airspayce.com/mikem/arduino/AccelStepper/index.html


####Rotary encoder
I have a 'Honeywell 600-128-cbl'. Looking at wires as they come out of encoder
green - Ground
yellow -  'A' out -->> arduino 0
orange - 'B' out -->> arduino 1
red - 5 Vdc

pinouts are in .pdf on farnell website
http://www.farnell.com/datasheets/1712854.pdf

mount with nut and lockwasher
    Hex Mount Nut: 3/8 in x 32
    Internal Tooth Lockwasher
    
####Rotary encoder library
http://www.pjrc.com/teensy/td_libs_Encoder.html

####Setting arbitrary interrupts on Arduino

http://www.geertlangereis.nl/Electronics/Pin_Change_Interrupts/PinChange_en.html


####Gotchas
 - Don't connect pin 0 on Arduino, you will get arduino error
    avrdude stk500_getsync(): not in sync
 
 ####Put Arduino libraries in
    /usr/share/arduino/libraries/
  
####Links
  
nice turorial
http://www.schmalzhaus.com/EasyDriver/Examples/EasyDriverExamples.html

http://bildr.org/2012/11/big-easy-driver-arduino/
http://bildr.org/2012/11/big-easy-driver-arduino/


A small fork of AccelStepper v1.3 with AF_motor (Adafruit motor shield) support
https://github.com/adafruit/AccelStepper