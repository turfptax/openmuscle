# openmuscle
Prosthetic sensor suite for the forearm and other muscle groups

The main objective of this project is to create a muscle detection band for the forearm that is inexpensive to make and able to be produced at a cost lower than $200 if possible.

#Current hardware for ADC and main computation is the RP2040 on the raspberry pi pico
#Prototype developed on the WaveShare RP2040 Zero chip: https://www.waveshare.com/rp2040-zero.htm

#Current sensors are the Hall Effect Sensor 49E 


Current Needs:
1. Machine Learning Engineer / Nerual network
2. Electric Engineer to help develop safety circuitry
3. Audio Specialist for noise reduction in signals
4. Mechanical Engineer for armband mechanism to help the pistons make contact with the skin on different diameter forearms
5. Battery module design


For the first prototype we are using micropython to make a proof of concept.

The micropython code provided by Jeremy P Bentham on his blog https://github.com/pimoroni/pimoroni-pico/releases/tag/v0.2.6  is amazing and is used for the basis test code for the ADCs.

Version 1.3 of the CELL0 units is out and Version 1.0 of the Compute Module are being manufactured currently.
