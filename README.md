
# Open Muscle
Open-Source muscle contraction & detection system.

Open Muscle is designed to provide biometric machine learning training data for use in prosthetic technologies. Most problems in AI are solved using giant data sets. Open muscle aims to provide the hardware, software for a muscle contraction training data set with **target values** and/or **classification data** included.

Open Hand, Open Muscle's counterpart, is an open source finger movement **somatosensor** (It detects the physical movement of the fingers). **#better word for this needed**

## Why use hall sensors instead of EMG sensors?
Open Muscle was designed to be the least expensive, highest signal to noise ratio, and least complex deployment device that is able to detect forearm muscle contractions.
The physical movement of muscles detected by a hall sensor and sprung magnet fit these requirements.
We are working on a silicon nipple spring for the 6th version of Open Muscle to further reduce the cost, complexity, and bulkiness of version 5.

## **Roadmap**

 - [x] Create an open-source hardware forearm bracelet :OM12 
 - [x] create the open-source software to acquire the training data :UDPserver
 - [x] build a hand gesture detection device for data **target values** :LASK4
 - [ ] Create an open-source server to store training data and negotiate connections
 - [ ] Raise awareness and ask people to help by providing training data

## Current Open Muscle Prototype V5.3.0

 - Custom PCB:  Open Muscle V5.3.0 Microcontroller: ESP32-S2 mini by Wemos v1.0.0
 - Hall Sensors: Hall Effect Sensor 49E
 - Programming Language: MicroPython
 - Sample Rate: 1200 s/s across all 12 ADCs: 100 s/s for each sensor with UDP transmission..

## Current Needs:

1. Machine Learning Engineer / Nerual network
2. Electric Engineer
3. Audio Specialist
4. Mechanical Engineer
5. Students
6. Crowd Source Data Acquisition (wear the bracelet)

## Currently working on OM24
Open Muscle 24 suggested features
1. 24 Pressure sensors (hall effect / magnet) pairs
2. Dedicated ADCs sampled at ~ 100s/s each
3. Dedicated Analog ADO for the sensors
4. Programmed in C++ 
5. Bluetooth
6. Phone Application to gather biometric data
7. LASK system integration for HUD and
8. 1000mah battery or enough charge to last for 8-16hrs of use


