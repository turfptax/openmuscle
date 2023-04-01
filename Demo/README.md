## Demo Files

See Wiki

# Use the Demo folder for training your own model

## Train-Model.py

Train-Model.py is setup to use the 'Trained-Demo-Model.pkl' pickle file as an export.

The input CSV file is 'Data-Captures/training_file9_USED TO TRAIN MODEL.csv'

When you run the program it will feed in the data from the csv file and train it with the 12 features and the 4 labels. These labels are also referred to as tokens, but they are supplying the model with the desired outputs from the system.

For the demo file it takes ~2 minutes to train the model.

It will also export the 20% of the test data with the predictions to a CSV file.

The model is stored inside of the pickle file to be used to make live predictions.

## Convert data to CSV Format
If you do not have the data in CSV format from open muscle you will need to use the 'Data-Captures' folder to take the raw text file json and convert it.

# filter-training-data-convert-CSV.py
The convert training data program takes the raw text json file from the recorded session and pairs the LASK data with the Open Muscle data.

Since UDP packets come in one at a time, we will have to pair them by timestamps and throw out data that does not have a pair.

## Predicting Live Data

Live data can use the LASK system to show its accuracy or it can be used without the LASK system.

Since the movement that we trained is specific to the motion that the LASK mechanical design provides it is suggested to use the LASK system while it is turned off.

Since the algorithm that filters the packets in the training phase, the same algorithm will have to be applied to the real-time data. For now we are suggesting to use the 'Mimic-Lask-Packets-0Data.py' to send 'dummy' lask data if you plan on not using the LASK system during real-time predictions.

# Using Live-Demo-Predictions.py

If you have trained your model and want to see live predictions use the live demo predictions program.

This will
1. Load the model
2. Great a GUI
3. Listen for Open Muscle and LASK packets
4. Filter the packets
5. Send data to the Model
6. Draw model predictions over actual or dummy data

## Using a Virtual Open Muscle and LASK

If you just want to see the model work in real-time we have supplied 3 short training files 8, 9, and 10.

The model, by default, is trained on file 9. 

You can use the 'OM-Mimic-DATA-SEND.py' program to send the packets over UDP to yourself.

This allows you to run both the mimic program and the Live Demo Predictions program at the same time to see the predictions from the precaptured dataset.

## Training Different Files
If you want to use one of the other two Data-Capture files instead of capture 9, you will just have to modify the 'Train-Model.py' code and rename the CSV file;
data = pd.read_csv('Data-Captures/training_file9_USED TO TRAIN MODEL.csv')
I have already used the 'filter-training-data-convert-CSV.py' on the three training files but you can also convert them into CSV by changing the code in the conversion file to the other txt file.





