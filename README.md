
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

## What ChatGPT says we need to do:
To label machine learning regression training data with target values, you will need to follow these steps:

1.  Identify the input variables that you will use to train your model. These are also known as the features or predictors.
    
2.  Collect the training data for these input variables. This may involve collecting data from a variety of sources, such as sensors, databases, or user input.
    
3.  Determine the target variable that you want to predict with your model. This is the variable that you will be trying to predict based on the input variables.
    
4.  For each training example, assign a target value to the target variable. This value should correspond to the value of the target variable that you want your model to predict for that example.
    
5.  Split your training data into a training set and a validation set. The training set will be used to train your model, while the validation set will be used to evaluate the model's performance.
    
6.  Use your training data to train your machine learning model. There are many different algorithms and approaches that you can use for this, including linear regression, decision trees, and neural networks.
    
7.  Use your validation set to evaluate the performance of your model. This will allow you to determine how well the model is able to predict the target values for the validation data.
    
8.  If the model's performance is not satisfactory, you may need to go back and adjust your model or collect more training data.

<img url='images/OpenMuscleV530Pinout-01.jpg'>
