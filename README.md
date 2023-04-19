
# Open Muscle
## The Open-Source Forearm Muscle-Based Finger Tracking Device.

Open Muscle is designed to provide biometric machine learning training data for use in prosthetic technologies. Most problems in AI are solved using giant data sets. Open muscle aims to provide the hardware, software for a muscle contraction training data set with **target values** and/or **classification data** included.

LASK, Open Muscle's counterpart, is an open source finger movement **somatosensor** that provides the labels to the feature data provided by open muscle. Open Muscle was able to detect finger movement and pressure with only tens of minutes of training data.

<br />
<div align="center">
    <img src="images/OpenMuscle-FlowChart.jpg" alt="OpenMuscle Flow Chart" width="100%">
</div>

# Current Working Prototype Version of Open Muscle:
## OpenMuscle 12 or OM12
Open Muscle 12 uses the built in ADCs on an ESP32-S2 for all 12 sensors. It can send 1200 s/s over UDP to the UDP python server that picks it up. 
- 12 Hall Effect Sensors
- 6 Cells of 2 Sensors Each
- PCB 5.3.0
- ESP32-S2 Microcontroller
- MicroPython

## LASK4 or LASK4 Version 2
LASK4 is the labeling device that obtains the finger movement labels for the feature data obtained from OM12. It currently does not detect thumb movements. Next version to include the thumb for Version 3. Check out the LASK4 Repository for more info:
- 4 Piston Tubes
- OLED Screen
- 4 Push buttons
- ESP32-S2 Microcontroller
- MicroPython

## **Roadmap**

 - [x] Create an open-source hardware forearm bracelet :OM12 
 - [x] create the open-source software to acquire the training data :UDPserver
 - [x] build a hand gesture detection device for data **target values** :LASK4
 - [ ] Create an open-source server to store training data and negotiate connections
 - [ ] Raise awareness and ask people to help by providing training data
 - [ ] Create a 'pre-production' version of the bracelet and lask

## Current Open Muscle Prototype V5.3.0

 - Custom PCB:  Open Muscle V5.3.0 Microcontroller: ESP32-S2 mini by Wemos v1.0.0
 - Hall Sensors: Hall Effect Sensor 49E
 - Programming Language: MicroPython
 - Sample Rate: 1200 s/s across all 12 ADCs: 100 s/s for each sensor with UDP transmission..





