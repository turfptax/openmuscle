# openmuscle
Prosthetic sensor suite for the forearm and other muscle groups

The main objective of this project is to create a muscle detection band for the forearm that is inexpensive to make and able to be produced at a cost lower than $200 if possible.

#Current hardware for ADC and main computation is the ESP32-S2
#Prototype developed on the WaveShare RP2040 Zero chip: https://www.waveshare.com/rp2040-zero.htm

#Current sensors are the Hall Effect Sensor 49E & SMB component research 


Current Needs:
1. Machine Learning Engineer / Nerual network
2. Electric Engineer to help develop safety circuitry
3. Audio Specialist for noise reduction in signals
4. Mechanical Engineer for armband mechanism to help the pistons make contact with the skin on different diameter forearms
5. Battery module design


For the first prototype we are using micropython to make a proof of concept.

The micropython code can sample at 1200 s/s across all 12 ADCs which is 100 s/s for each sensor.


Version 5.3.0 is now available STL files have been uploaded. Also using Fusion360 now for main CAD software.
Any suggested file formats requested will be considered.

For a list of the components needed to build the Open Muscle band visit: https://oprosthetics.org/open-muscle/open-muscle-components
This is out of date but should be updated soon ETA 10-25-2022

<img url='images/OpenMuscleV530Pinout-01.jpg'>
