## Demo Files

See Wiki

# Use the Demo folder for training your own model

# Quick Setup

1. Run train_model_time.py
2. Run demo_live_time_predictions.py
3. While the demo is running run virtual_sensor_transmitter.py to send virtual data packets to the demo

# Dependencies
scikit-learn
pandas
pygame

```
pip install scikit-learn
```

## train_model.py

Train-Model.py is setup to use the 'Trained-Demo-Model.pkl' pickle file as an export.

The input CSV file is 'Data-Captures/capture_11.csv'

When you run the program it will feed in the data from the csv file and train it with the 12 features and the 4 labels. These labels are also referred to as tokens, but they are supplying the model with the desired outputs from the system.

For the demo file it takes ~2 minutes to train the model.

It will also export the 20% of the test data with the predictions to a CSV file.

The model is stored inside of the pickle file to be used to make live predictions.

# Convert data to CSV Format
If you do not have the data in CSV format from open muscle you will need to use the 'Data-Captures' folder to take the raw text file json and convert it.

## sensor_data_filter.py
The convert training data program takes the raw text json file from the recorded session and pairs the LASK data with the Open Muscle data.

Since UDP packets come in one at a time, we will have to pair them by timestamps and throw out data that does not have a pair.

# Predicting Live Data

Live data can use the LASK system to show its accuracy or it can be used without the LASK system.

Since the movement that we trained is specific to the motion that the LASK mechanical design provides it is suggested to use the LASK system while it is turned off.

## virtual_lask_zero_values.py
Since the algorithm that filters the packets in the training phase, the same algorithm will have to be applied to the real-time data. For now we are suggesting to use the 'virtual_lask_zero_values.py' to send 'dummy' lask data if you plan on not using the LASK system during real-time predictions.

## demo_live_predictions.py

If you have trained your model and want to see live predictions use the live demo predictions program.

This will
1. Load the model
2. Great a GUI
3. Listen for Open Muscle and LASK packets
4. Filter the packets
5. Send data to the Model
6. Draw model predictions over actual or dummy data


## Using a Virtual Open Muscle and LASK

If you just want to see the model work in real-time we have supplied 2 short training files 11 and 12.

The model, by default, is trained on capture_11. 

### virtual_sensor_transmitter.py
You can use the 'virtual_sensor_transmitter.py' program to send the packets over UDP to yourself.
It takes capture_12, by default, and sends the raw packets as a virutal device(s)

This allows you to run both the mimic program and the Live Demo Predictions program at the same time to see the predictions from the precaptured dataset.

# Training Different Files
If you want to use one of the other two Data-Capture files instead of capture 9, you will just have to modify the 'Train-Model.py' code and rename the CSV file;
data = pd.read_csv('Data-Captures/capture_9.csv')
I have already used the 'filter-training-data-convert-CSV.py' on the three training files but you can also convert them into CSV by changing the code in the conversion file to the other txt file.





